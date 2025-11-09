from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import get_db, init_db
import os
from datetime import datetime, date
import json
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

init_db()

@app.route('/')
def index():
    if 'student_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE email = ? AND password = ?', 
                          (email, password)).fetchone()
    conn.close()
    
    if student:
        session['student_id'] = student['id']
        session['student_name'] = student['first_name']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    enrolled_count = conn.execute(
        'SELECT COUNT(*) as count FROM enrolled_courses WHERE student_id = ?', 
        (student_id,)
    ).fetchone()['count']
    
    enrolled_courses = conn.execute('''
        SELECT c.course_name, c.instructor, ec.progress 
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
        ORDER BY ec.enrolled_at DESC
        LIMIT 3
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    insights = generate_ai_insights(student_id)
    
    return render_template('dashboard.html', 
                         student=student,
                         enrolled_count=enrolled_count,
                         insights=insights,
                         upcoming_classes=enrolled_courses)

@app.route('/courses')
def courses():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    
    enrolled = conn.execute('''
        SELECT c.*, ec.progress, ec.grade, ec.modules_completed, ec.pending_assignments
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
        ORDER BY ec.enrolled_at DESC
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    recommended = get_ai_course_recommendations(student_id)
    
    return render_template('courses.html', 
                         enrolled_courses=enrolled,
                         recommended_courses=recommended)

@app.route('/slu-gpt')
def slu_gpt():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    chat_history = conn.execute('''
        SELECT message, response, created_at 
        FROM chat_history 
        WHERE student_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    return render_template('slu_gpt.html', 
                         student=student,
                         chat_history=list(reversed(chat_history)))

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    message = request.json.get('message')
    
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    enrolled_courses = conn.execute('''
        SELECT c.course_code, c.course_name
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
    ''', (student_id,)).fetchall()
    
    courses_list = ', '.join([f"{c['course_code']} ({c['course_name']})" for c in enrolled_courses])
    
    system_prompt = f"""You are SLU GPT, an AI academic assistant for Saint Louis University.
You are helping {student['first_name']} {student['last_name']}, a Master's student in Information Systems.
Their career goal is: {student['career_goal']}
Their current enrolled courses are: {courses_list}

Provide helpful, accurate, and encouraging responses related to:
- Course content and concepts
- Assignment guidance
- Study strategies
- Career and research questions
- Saint Louis University MS in Information Systems program

Keep responses concise, supportive, and academically focused."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        conn.execute('INSERT INTO chat_history (student_id, message, response) VALUES (?, ?, ?)',
                    (student_id, message, ai_response))
        
        conn.execute('UPDATE students SET slu_gpt_sessions = slu_gpt_sessions + 1 WHERE id = ?',
                    (student_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'response': ai_response})
    
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/quiz')
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('quiz.html')

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    conn = get_db()
    
    today = date.today().isoformat()
    existing_quiz = conn.execute(
        'SELECT * FROM quiz_history WHERE student_id = ? AND quiz_date = ?',
        (student_id, today)
    ).fetchone()
    
    if existing_quiz and existing_quiz['completed']:
        conn.close()
        return jsonify({
            'quiz': json.loads(existing_quiz['questions']),
            'answers': json.loads(existing_quiz['answers']) if existing_quiz['answers'] else None,
            'score': existing_quiz['score'],
            'completed': True
        })
    
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    enrolled_courses = conn.execute('''
        SELECT c.course_code, c.course_name
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
    ''', (student_id,)).fetchall()
    
    courses_list = ', '.join([c['course_name'] for c in enrolled_courses])
    
    prompt = f"""Generate a 10-question multiple choice quiz for a Master's student in Information Systems.
Career goal: {student['career_goal']}
Current courses: {courses_list}

Create questions that test knowledge relevant to their career goal and current subjects.

Return ONLY a valid JSON object in this exact format (no markdown, no extra text):
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0
    }}
  ]
}}

The "correct" field should be the index (0-3) of the correct option.
Generate exactly 10 questions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.8
        )
        
        quiz_json = response.choices[0].message.content.strip()
        
        if quiz_json.startswith('```'):
            quiz_json = quiz_json.split('```')[1]
            if quiz_json.startswith('json'):
                quiz_json = quiz_json[4:]
            quiz_json = quiz_json.strip()
        
        quiz_data = json.loads(quiz_json)
        
        if existing_quiz:
            conn.execute('UPDATE quiz_history SET questions = ? WHERE id = ?',
                        (json.dumps(quiz_data), existing_quiz['id']))
        else:
            conn.execute(
                'INSERT INTO quiz_history (student_id, quiz_date, questions) VALUES (?, ?, ?)',
                (student_id, today, json.dumps(quiz_data))
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({'quiz': quiz_data, 'completed': False})
    
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    answers = request.json.get('answers')
    
    conn = get_db()
    today = date.today().isoformat()
    
    quiz = conn.execute(
        'SELECT * FROM quiz_history WHERE student_id = ? AND quiz_date = ?',
        (student_id, today)
    ).fetchone()
    
    if not quiz:
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404
    
    quiz_data = json.loads(quiz['questions'])
    score = 0
    
    for i, answer in enumerate(answers):
        if i < len(quiz_data['questions']):
            if answer == quiz_data['questions'][i]['correct']:
                score += 1
    
    conn.execute(
        'UPDATE quiz_history SET answers = ?, score = ?, completed = 1 WHERE id = ?',
        (json.dumps(answers), score, quiz['id'])
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'score': score, 'total': len(quiz_data['questions'])})

def generate_ai_insights(student_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    enrolled_courses = conn.execute('''
        SELECT c.course_name, ec.progress, ec.grade
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    courses_info = ', '.join([f"{c['course_name']} ({c['progress']}% complete, Grade: {c['grade']})" 
                              for c in enrolled_courses])
    
    prompt = f"""Generate 3 brief AI-powered insights for a student with:
GPA: {student['gpa']}
Completion Rate: {student['completion_rate']}%
Courses: {courses_info}
Career Goal: {student['career_goal']}

Provide 3 specific, actionable insights (one positive, one suggestion, one recommendation).
Format as JSON array of objects with 'type' (success/warning/info) and 'text' fields.
Keep each insight under 100 characters."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        insights_json = response.choices[0].message.content.strip()
        if insights_json.startswith('```'):
            insights_json = insights_json.split('```')[1]
            if insights_json.startswith('json'):
                insights_json = insights_json[4:]
            insights_json = insights_json.strip()
        
        return json.loads(insights_json)
    except:
        return [
            {"type": "success", "text": "Great progress! Your performance in Machine Learning has improved by 15% this month."},
            {"type": "warning", "text": "You might need extra support in Statistical Methods. Consider scheduling a tutoring session."},
            {"type": "info", "text": "Based on your interests, we recommend taking 'Deep Learning Fundamentals' next semester."}
        ]

def get_ai_course_recommendations(student_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    available_courses = conn.execute('SELECT * FROM available_courses').fetchall()
    
    enrolled_codes = conn.execute('''
        SELECT c.course_code
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    enrolled_codes_list = [c['course_code'] for c in enrolled_codes]
    available_list = [f"{c['course_code']}: {c['course_name']} - {c['description']}" 
                      for c in available_courses if c['course_code'] not in enrolled_codes_list]
    
    if not available_list:
        return []
    
    prompt = f"""Based on this career goal: "{student['career_goal']}"

Available courses:
{chr(10).join(available_list[:15])}

Recommend exactly 3 courses that best align with the career goal.
Return ONLY a JSON array of course codes, e.g., ["IS 6100", "IS 6200", "IS 6300"]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        
        recs_json = response.choices[0].message.content.strip()
        if recs_json.startswith('```'):
            recs_json = recs_json.split('```')[1]
            if recs_json.startswith('json'):
                recs_json = recs_json[4:]
            recs_json = recs_json.strip()
        
        recommended_codes = json.loads(recs_json)
        
        recommended_courses = [c for c in available_courses if c['course_code'] in recommended_codes]
        return recommended_courses[:3]
    except:
        return list(available_courses[:3])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
