from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import get_db, init_db
import os
from datetime import datetime, date
import json
from openai import OpenAI
from dotenv import load_dotenv
import analytics_service

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("WARNING: OPENAI_API_KEY not set. AI features will not work.")
    print("Please set your OpenAI API key as an environment variable.")
    client = None
else:
    client = OpenAI(api_key=api_key)

# Set OpenAI client for analytics service
analytics_service.set_openai_client(client)

init_db()

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'ForgeEd LMS'}), 200

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
        session['is_admin'] = bool(student['is_admin'])
        
        if student['is_admin']:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'student_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    return render_template('admin.html')

@app.route('/api/admin/students', methods=['GET'])
def get_all_students():
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    students = conn.execute('''
        SELECT s.id, s.email, s.first_name, s.last_name, s.gpa, s.educational_background, 
               s.career_goal, s.created_at,
               (SELECT AVG(total_score) FROM wellbeing_assessments WHERE student_id = s.id) as avg_wellbeing
        FROM students s
        WHERE s.is_admin = 0
        ORDER BY s.created_at DESC
    ''').fetchall()
    
    students_data = []
    for student in students:
        student_dict = dict(student)
        avg_wellbeing = student_dict.get('avg_wellbeing', 0)
        
        # Use the same risk level calculation as analytics page
        risk_level = analytics_service.calculate_risk_level(student['id'])
        
        student_dict['avg_wellbeing'] = round(avg_wellbeing, 1) if avg_wellbeing else 0
        student_dict['risk_level'] = risk_level
        students_data.append(student_dict)
    
    conn.close()
    return jsonify(students_data)

@app.route('/api/admin/students', methods=['POST'])
def add_student():
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    conn = get_db()
    student_id = None
    
    try:
        cursor = conn.execute('''
            INSERT INTO students (email, password, first_name, last_name, educational_background, career_goal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['email'], data['password'], data['first_name'], data['last_name'], 
              data.get('educational_background', ''), data.get('career_goal', '')))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        try:
            from generate_roadmap import generate_90day_roadmap
            generate_90day_roadmap(student_id)
        except Exception as roadmap_error:
            conn2 = get_db()
            conn2.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn2.commit()
            conn2.close()
            return jsonify({'success': False, 'error': f'Failed to generate roadmap: {str(roadmap_error)}'}), 400
        
        return jsonify({'success': True, 'student_id': student_id})
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/admin/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    conn.execute('DELETE FROM students WHERE id = ? AND is_admin = 0', (student_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/admin/courses', methods=['GET'])
def get_all_courses():
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    courses = conn.execute('''
        SELECT * FROM courses ORDER BY course_code
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(course) for course in courses])

@app.route('/api/admin/courses', methods=['POST'])
def add_course():
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    conn = get_db()
    
    try:
        conn.execute('''
            INSERT INTO courses (course_code, course_name, credits, description, faculty_name, intake_term, semester)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['course_code'], data['course_name'], data.get('credits', 3), 
              data.get('description', ''), data.get('faculty_name', ''), 
              data.get('intake_term', ''), data.get('semester', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/admin/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if 'student_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

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
    
    # Calculate Career Ready percentage based on roadmap completion
    created_at = datetime.fromisoformat(student['created_at'])
    current_day = min((datetime.now() - created_at).days + 1, 90)
    career_ready_percentage = int((current_day / 90) * 100)
    
    # Get recent wellbeing score
    recent_wellbeing = conn.execute('''
        SELECT total_score FROM wellbeing_assessments 
        WHERE student_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (student_id,)).fetchone()
    wellbeing_score = recent_wellbeing['total_score'] if recent_wellbeing else 0
    
    # Check if quizzes taken today
    today = datetime.now().strftime('%Y-%m-%d')
    career_quiz_today = conn.execute('''
        SELECT * FROM career_quiz_history 
        WHERE student_id = ? AND quiz_date = ? AND completed = 1
        ORDER BY created_at DESC LIMIT 1
    ''', (student_id, today)).fetchone()
    
    academic_quiz_today = conn.execute('''
        SELECT * FROM academic_quiz_history 
        WHERE student_id = ? AND quiz_date = ? AND completed = 1
        ORDER BY created_at DESC LIMIT 1
    ''', (student_id, today)).fetchone()
    
    conn.close()
    
    insights = generate_dashboard_insights(student_id, student['gpa'], career_ready_percentage, wellbeing_score)
    
    return render_template('dashboard.html', 
                         student=student,
                         enrolled_count=enrolled_count,
                         career_ready_percentage=career_ready_percentage,
                         wellbeing_score=wellbeing_score,
                         insights=insights,
                         career_quiz_today=career_quiz_today,
                         academic_quiz_today=academic_quiz_today)

@app.route('/analytics')
def analytics():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    
    # Calculate metrics
    current_gpa = student['gpa']
    predicted_gpa = analytics_service.calculate_predicted_gpa(student_id, current_gpa)
    confidence_level = analytics_service.calculate_confidence_level(student_id)
    risk_level = analytics_service.calculate_risk_level(student_id)
    
    # Get chart data
    gpa_history = analytics_service.get_gpa_history(student_id)
    performance_data = analytics_service.get_subject_performance(student_id)
    
    # Get AI analysis
    ai_analysis = analytics_service.generate_ai_analysis(
        student_id, current_gpa, predicted_gpa, confidence_level, risk_level
    )
    
    # Get AI predictions
    ai_predictions = analytics_service.generate_ai_predictions(
        student_id, current_gpa, predicted_gpa, confidence_level
    )
    
    return render_template('analytics.html',
                         current_gpa=current_gpa,
                         predicted_gpa=predicted_gpa,
                         confidence_level=confidence_level,
                         risk_level=risk_level,
                         gpa_history=gpa_history,
                         performance_data=performance_data,
                         strengths=ai_analysis.get('strengths', []),
                         improvements=ai_analysis.get('improvements', []),
                         recommendations=ai_analysis.get('recommendations', []),
                         ai_predictions=ai_predictions)

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
        LIMIT 3
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
    
    if not client:
        return jsonify({'error': 'AI service not configured'}), 503
    
    student_id = session['student_id']
    message = request.json.get('message') if request.json else None
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
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
    
    student_id = session['student_id']
    conn = get_db()
    
    # Check if quizzes taken today
    today = datetime.now().strftime('%Y-%m-%d')
    career_quiz_today = conn.execute('''
        SELECT * FROM career_quiz_history 
        WHERE student_id = ? AND quiz_date = ? AND completed = 1
        ORDER BY created_at DESC LIMIT 1
    ''', (student_id, today)).fetchone()
    
    academic_quiz_today = conn.execute('''
        SELECT * FROM academic_quiz_history 
        WHERE student_id = ? AND quiz_date = ? AND completed = 1
        ORDER BY created_at DESC LIMIT 1
    ''', (student_id, today)).fetchone()
    
    conn.close()
    
    return render_template('quiz.html', 
                         career_quiz_today=career_quiz_today,
                         academic_quiz_today=academic_quiz_today)

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not client:
        return jsonify({'error': 'AI service not configured'}), 503
    
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
    answers = request.json.get('answers') if request.json else None
    
    if not answers:
        return jsonify({'error': 'No answers provided'}), 400
    
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

def generate_dashboard_insights(student_id, gpa, career_ready_percentage, wellbeing_score):
    """Generate personalized AI insights based on current scores"""
    if not client:
        return [
            {"type": "academic", "text": f"Your {gpa:.2f} GPA shows strong academic performance. Keep it up!"},
            {"type": "career", "text": f"You're {career_ready_percentage}% through your career roadmap. Stay consistent!"},
            {"type": "wellbeing", "text": f"Wellbeing score of {wellbeing_score} is good. Remember to balance study and rest."}
        ]
    
    prompt = f"""Generate 3 brief, personalized insights for a student with these metrics:
- GPA: {gpa:.2f}/4.0
- Career Ready: {career_ready_percentage}% (90-day learning roadmap progress)
- Recent Wellbeing Score: {wellbeing_score}/100

Provide 3 specific, actionable insights - one for each category:
1. Academic insight about their GPA (type: "academic")
2. Career insight about their roadmap progress (type: "career") 
3. Wellbeing insight about their mental health score (type: "wellbeing")

Format as JSON array of objects with 'type' and 'text' fields.
Keep each insight under 120 characters."""

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
        
        insights = json.loads(insights_json)
        
        # Normalize types to lowercase and validate
        for insight in insights:
            if 'type' in insight:
                insight['type'] = insight['type'].lower()
                # Fallback to 'academic' if type is not recognized
                if insight['type'] not in ['academic', 'career', 'wellbeing']:
                    insight['type'] = 'academic'
        
        return insights
    except:
        return [
            {"type": "academic", "text": f"Your {gpa:.2f} GPA shows strong academic performance. Keep it up!"},
            {"type": "career", "text": f"You're {career_ready_percentage}% through your career roadmap. Stay consistent!"},
            {"type": "wellbeing", "text": f"Wellbeing score of {wellbeing_score} is good. Remember to balance study and rest."}
        ]

def get_ai_course_recommendations(student_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    available_courses = conn.execute('SELECT * FROM courses').fetchall()
    
    enrolled_codes = conn.execute('''
        SELECT c.course_code
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    enrolled_codes_list = [c['course_code'] for c in enrolled_codes]
    available_list = [f"{c['course_code']}: {c['course_name']} ({c['faculty_name'] or 'TBD'}) - {c['description'] or ''} [Intake: {c['intake_term'] or 'TBD'}]" 
                      for c in available_courses if c['course_code'] not in enrolled_codes_list]
    
    if not available_list:
        return []
    
    not_enrolled_courses = [c for c in available_courses if c['course_code'] not in enrolled_codes_list]
    
    if not client:
        return [dict(c) for c in not_enrolled_courses[:3]]
    
    prompt = f"""Based on this career goal: "{student['career_goal']}"
Student's educational background: "{student['educational_background'] if student['educational_background'] else 'Not specified'}"

Available courses at the university:
{chr(10).join(available_list[:20])}

Recommend exactly 3 courses that best align with the career goal and educational background.
Consider the faculty expertise and intake terms.
Return ONLY a JSON array of course codes, e.g., ["CS-5100", "IS-6200", "DS-6300"]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        recs_json = response.choices[0].message.content.strip()
        if recs_json.startswith('```'):
            recs_json = recs_json.split('```')[1]
            if recs_json.startswith('json'):
                recs_json = recs_json[4:]
            recs_json = recs_json.strip()
        
        recommended_codes = json.loads(recs_json)
        
        recommended_courses = [dict(c) for c in available_courses if c['course_code'] in recommended_codes]
        return recommended_courses[:3]
    except:
        return [dict(c) for c in not_enrolled_courses[:3]]

@app.route('/career-learning')
def career_learning():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    # Get current day number (days since account creation)
    from datetime import datetime
    created_at = datetime.fromisoformat(student['created_at'])
    days_elapsed = (datetime.now() - created_at).days + 1
    current_day = min(days_elapsed, 90)  # Cap at 90 days
    
    # Get all roadmap days
    roadmap = conn.execute('''
        SELECT * FROM daily_roadmap 
        WHERE student_id = ? 
        ORDER BY day_number
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    return render_template('career_learning.html', 
                         student=student,
                         roadmap=roadmap,
                         current_day=current_day)

@app.route('/api/get-day-content/<int:day_number>')
def get_day_content(day_number):
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    conn = get_db()
    
    # Server-side day-locking validation
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    created_at = datetime.fromisoformat(student['created_at'])
    current_day = min((datetime.now() - created_at).days + 1, 90)
    
    # Prevent access to future days
    if day_number > current_day:
        conn.close()
        return jsonify({'error': 'This day is locked. Complete previous days first.'}), 403
    
    # Get the day's topic from roadmap
    day_topic = conn.execute('''
        SELECT * FROM daily_roadmap 
        WHERE student_id = ? AND day_number = ?
    ''', (student_id, day_number)).fetchone()
    
    if not day_topic:
        conn.close()
        return jsonify({'error': 'Day not found'}), 404
    
    # Generate detailed theory content using ChatGPT if not already generated
    if not day_topic['theory_content'] or len(day_topic['theory_content']) < 100:
        if client:
            try:
                prompt = f"""You are creating a 2-hour learning session for Day {day_number} of a 90-day career roadmap.

Career Goal: {student['career_goal']}
Today's Topic: {day_topic['topic']}

Create comprehensive learning content with:
1. Introduction (what and why this topic matters)
2. Key Concepts (main points to understand)
3. Practical Applications (how it's used in the real world)
4. Learning Objectives (what you'll know after 2 hours)

Format the response with proper HTML formatting using <h3>, <h4>, <p>, <ul>, <li>, <strong> tags.
Make it engaging and suitable for 2 hours of study.
Keep it under 800 words."""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )
                
                theory_content = response.choices[0].message.content.strip()
                
                # Update database with generated content
                conn.execute('''
                    UPDATE daily_roadmap 
                    SET theory_content = ?
                    WHERE student_id = ? AND day_number = ?
                ''', (theory_content, student_id, day_number))
                conn.commit()
                
            except Exception as e:
                theory_content = day_topic['theory_content'] or "Content generation failed. Please try again."
        else:
            theory_content = day_topic['theory_content'] or "AI service not configured."
    else:
        theory_content = day_topic['theory_content']
    
    # Get external resource links
    default_resources = [
        {"title": "MDN Web Docs", "url": "https://developer.mozilla.org"},
        {"title": "W3Schools", "url": "https://www.w3schools.com"},
        {"title": "FreeCodeCamp", "url": "https://www.freecodecamp.org"}
    ]
    
    if day_topic['resources']:
        try:
            resources = json.loads(day_topic['resources'])
            if not resources:
                resources = default_resources
        except:
            resources = default_resources
    else:
        resources = default_resources
    
    conn.close()
    
    return jsonify({
        'day_number': day_number,
        'topic': day_topic['topic'],
        'theory': theory_content,
        'resources': resources,
        'study_duration': day_topic['study_duration'],
        'is_completed': bool(day_topic['is_completed'])
    })

@app.route('/api/complete-day', methods=['POST'])
def complete_day():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    day_number = request.json.get('day_number') if request.json else None
    
    if not day_number:
        return jsonify({'error': 'Day number required'}), 400
    
    conn = get_db()
    
    # Server-side validation - only allow completing current or past days
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    created_at = datetime.fromisoformat(student['created_at'])
    current_day = min((datetime.now() - created_at).days + 1, 90)
    
    # Prevent marking future days as complete
    if day_number > current_day:
        conn.close()
        return jsonify({'error': 'Cannot complete future days'}), 403
    
    conn.execute('''
        UPDATE daily_roadmap 
        SET is_completed = 1, completed_at = CURRENT_TIMESTAMP
        WHERE student_id = ? AND day_number = ?
    ''', (student_id, day_number))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/wellbeing')
def wellbeing():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    student_id = session['student_id']
    conn = get_db()
    
    # Check if today's assessment already exists
    today = date.today().isoformat()
    existing = conn.execute('''
        SELECT * FROM wellbeing_assessments 
        WHERE student_id = ? AND assessment_date = ?
    ''', (student_id, today)).fetchone()
    
    # Get recent assessments for context
    recent_assessments = conn.execute('''
        SELECT * FROM wellbeing_assessments 
        WHERE student_id = ?
        ORDER BY assessment_date DESC
        LIMIT 7
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    return render_template('wellbeing.html', 
                         existing_assessment=existing,
                         recent_assessments=recent_assessments)

@app.route('/api/submit-wellbeing', methods=['POST'])
def submit_wellbeing():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    data = request.json
    
    # Calculate total score (average of all scores)
    scores = [
        data.get('happiness_score', 50),
        data.get('stress_score', 50),
        data.get('energy_score', 50),
        data.get('motivation_score', 50),
        data.get('sleep_quality', 50)
    ]
    total_score = int(sum(scores) / len(scores))
    
    # Store all responses as JSON
    responses = json.dumps({
        'feelings': data.get('feelings', ''),
        'challenges': data.get('challenges', ''),
        'achievements': data.get('achievements', ''),
        'support_needed': data.get('support_needed', '')
    })
    
    # Generate AI insights
    ai_insights = ""
    if client:
        try:
            prompt = f"""Analyze this student's daily wellbeing assessment:

Happiness: {data.get('happiness_score', 50)}/100
Stress: {data.get('stress_score', 50)}/100  
Energy: {data.get('energy_score', 50)}/100
Motivation: {data.get('motivation_score', 50)}/100
Sleep Quality: {data.get('sleep_quality', 50)}/100

Today's Feelings: {data.get('feelings', 'Not specified')}
Challenges: {data.get('challenges', 'None mentioned')}
Achievements: {data.get('achievements', 'None mentioned')}

Provide brief, personalized insights (2-3 sentences):
- If scores are good, provide motivation and encouragement
- If scores are low, provide supportive suggestions for improvement
- Acknowledge their achievements and challenges

Keep it warm, supportive, and under 150 words."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            
            ai_insights = response.choices[0].message.content.strip()
        except:
            ai_insights = "Keep focusing on your wellbeing. Small daily improvements lead to great long-term results!"
    
    # Save to database
    conn = get_db()
    today = date.today().isoformat()
    
    # Check if today's assessment exists
    existing = conn.execute('''
        SELECT id FROM wellbeing_assessments 
        WHERE student_id = ? AND assessment_date = ?
    ''', (student_id, today)).fetchone()
    
    if existing:
        # Update existing
        conn.execute('''
            UPDATE wellbeing_assessments
            SET happiness_score = ?, stress_score = ?, energy_score = ?,
                motivation_score = ?, sleep_quality = ?, responses = ?,
                total_score = ?, ai_insights = ?
            WHERE student_id = ? AND assessment_date = ?
        ''', (data.get('happiness_score', 50), data.get('stress_score', 50),
              data.get('energy_score', 50), data.get('motivation_score', 50),
              data.get('sleep_quality', 50), responses, total_score, ai_insights,
              student_id, today))
    else:
        # Insert new
        conn.execute('''
            INSERT INTO wellbeing_assessments 
            (student_id, assessment_date, happiness_score, stress_score, energy_score,
             motivation_score, sleep_quality, responses, total_score, ai_insights)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, today, data.get('happiness_score', 50),
              data.get('stress_score', 50), data.get('energy_score', 50),
              data.get('motivation_score', 50), data.get('sleep_quality', 50),
              responses, total_score, ai_insights))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'total_score': total_score,
        'ai_insights': ai_insights
    })

@app.route('/api/generate-career-quiz', methods=['POST'])
def generate_career_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not client:
        return jsonify({'error': 'AI service not configured'}), 503
    
    student_id = session['student_id']
    conn = get_db()
    
    today = date.today().isoformat()
    
    # Check if quiz already exists
    existing = conn.execute('''
        SELECT * FROM career_quiz_history 
        WHERE student_id = ? AND quiz_date = ?
    ''', (student_id, today)).fetchone()
    
    if existing and existing['completed']:
        conn.close()
        return jsonify({
            'quiz': json.loads(existing['questions']),
            'answers': json.loads(existing['answers']) if existing['answers'] else None,
            'score': existing['score'],
            'ai_feedback': existing['ai_feedback'],
            'completed': True
        })
    
    # Get today's roadmap topic
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    created_at = datetime.fromisoformat(student['created_at'])
    current_day = min((datetime.now() - created_at).days + 1, 90)
    
    day_topic = conn.execute('''
        SELECT * FROM daily_roadmap 
        WHERE student_id = ? AND day_number = ?
    ''', (student_id, current_day)).fetchone()
    
    if not day_topic:
        conn.close()
        return jsonify({'error': 'No roadmap topic found for today'}), 404
    
    topic = day_topic['topic']
    
    prompt = f"""Generate a 10-question multiple choice quiz on this topic: {topic}

Career Goal: {student['career_goal']}

Questions should test understanding of today's learning topic.
Return ONLY valid JSON:
{{
  "questions": [
    {{"id": 1, "question": "...", "options": ["A", "B", "C", "D"], "correct": 0}}
  ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        
        quiz_json = response.choices[0].message.content.strip()
        if quiz_json.startswith('```'):
            quiz_json = quiz_json.split('```')[1]
            if quiz_json.startswith('json'):
                quiz_json = quiz_json[4:]
            quiz_json = quiz_json.strip()
        
        quiz_data = json.loads(quiz_json)
        
        if existing:
            conn.execute('UPDATE career_quiz_history SET questions = ?, topic = ?, day_number = ? WHERE id = ?',
                        (json.dumps(quiz_data), topic, current_day, existing['id']))
        else:
            conn.execute('''
                INSERT INTO career_quiz_history 
                (student_id, quiz_date, day_number, topic, questions, total_questions)
                VALUES (?, ?, ?, ?, ?, 10)
            ''', (student_id, today, current_day, topic, json.dumps(quiz_data)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'quiz': quiz_data, 'topic': topic, 'completed': False})
    
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-career-quiz', methods=['POST'])
def submit_career_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    data = request.json
    answers = data.get('answers', [])
    
    conn = get_db()
    today = date.today().isoformat()
    
    quiz = conn.execute('''
        SELECT * FROM career_quiz_history 
        WHERE student_id = ? AND quiz_date = ?
    ''', (student_id, today)).fetchone()
    
    if not quiz:
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404
    
    quiz_data = json.loads(quiz['questions'])
    score = 0
    wrong_answers = []
    
    for i, answer in enumerate(answers):
        if i < len(quiz_data['questions']):
            if answer == quiz_data['questions'][i]['correct']:
                score += 1
            else:
                wrong_answers.append({
                    'question': quiz_data['questions'][i]['question'],
                    'correct_answer': quiz_data['questions'][i]['options'][quiz_data['questions'][i]['correct']],
                    'your_answer': quiz_data['questions'][i]['options'][answer] if answer is not None else 'Not answered'
                })
    
    # Generate AI feedback
    ai_feedback = ""
    if client and wrong_answers:
        try:
            wrong_list = '\n'.join([f"Q: {w['question']}\nYour answer: {w['your_answer']}\nCorrect: {w['correct_answer']}" 
                                   for w in wrong_answers[:3]])
            
            prompt = f"""Student scored {score}/10 on a quiz about: {quiz['topic']}

Wrong answers:
{wrong_list}

Provide brief feedback (2-3 sentences) on what they should review and how to improve. Be supportive and specific."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            ai_feedback = response.choices[0].message.content.strip()
        except:
            ai_feedback = f"You scored {score}/10. Review the questions you missed and study {quiz['topic']} more deeply."
    else:
        ai_feedback = f"Great job! You scored {score}/10 on {quiz['topic']}."
    
    conn.execute('''
        UPDATE career_quiz_history 
        SET answers = ?, score = ?, total_questions = ?, ai_feedback = ?, completed = 1
        WHERE id = ?
    ''', (json.dumps(answers), score, 10, ai_feedback, quiz['id']))
    
    # Also mark the roadmap day as complete
    day_number = quiz['day_number']
    conn.execute('''
        UPDATE daily_roadmap 
        SET is_completed = 1, completed_at = CURRENT_TIMESTAMP
        WHERE student_id = ? AND day_number = ?
    ''', (student_id, day_number))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'score': score,
        'total': 10,
        'ai_feedback': ai_feedback,
        'day_completed': True
    })

@app.route('/api/generate-academic-quiz', methods=['POST'])
def generate_academic_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not client:
        return jsonify({'error': 'AI service not configured'}), 503
    
    student_id = session['student_id']
    conn = get_db()
    
    today = date.today().isoformat()
    
    # Check if quiz already exists
    existing = conn.execute('''
        SELECT * FROM academic_quiz_history 
        WHERE student_id = ? AND quiz_date = ?
    ''', (student_id, today)).fetchone()
    
    if existing and existing['completed']:
        conn.close()
        return jsonify({
            'quiz': json.loads(existing['questions']),
            'answers': json.loads(existing['answers']) if existing['answers'] else None,
            'score': existing['score'],
            'ai_feedback': existing['ai_feedback'],
            'completed': True
        })
    
    # Get 3 current semester courses
    courses = conn.execute('''
        SELECT c.course_name 
        FROM enrolled_courses ec
        JOIN courses c ON ec.course_id = c.id
        WHERE ec.student_id = ?
        LIMIT 3
    ''', (student_id,)).fetchall()
    
    if len(courses) < 3:
        conn.close()
        return jsonify({'error': 'Need at least 3 enrolled courses'}), 400
    
    courses_list = [c['course_name'] for c in courses]
    
    prompt = f"""Generate a 15-question multiple choice quiz (5 questions from each subject):

Subject 1: {courses_list[0]}
Subject 2: {courses_list[1]}
Subject 3: {courses_list[2]}

Return ONLY valid JSON:
{{
  "questions": [
    {{"id": 1, "subject": "{courses_list[0]}", "question": "...", "options": ["A", "B", "C", "D"], "correct": 0}}
  ]
}}

Generate exactly 15 questions (5 per subject)."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.7
        )
        
        quiz_json = response.choices[0].message.content.strip()
        if quiz_json.startswith('```'):
            quiz_json = quiz_json.split('```')[1]
            if quiz_json.startswith('json'):
                quiz_json = quiz_json[4:]
            quiz_json = quiz_json.strip()
        
        quiz_data = json.loads(quiz_json)
        
        if existing:
            conn.execute('UPDATE academic_quiz_history SET questions = ? WHERE id = ?',
                        (json.dumps(quiz_data), existing['id']))
        else:
            conn.execute('''
                INSERT INTO academic_quiz_history 
                (student_id, quiz_date, questions, total_questions)
                VALUES (?, ?, ?, 15)
            ''', (student_id, today, json.dumps(quiz_data)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'quiz': quiz_data, 'courses': courses_list, 'completed': False})
    
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-academic-quiz', methods=['POST'])
def submit_academic_quiz():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    data = request.json
    answers = data.get('answers', [])
    
    conn = get_db()
    today = date.today().isoformat()
    
    quiz = conn.execute('''
        SELECT * FROM academic_quiz_history 
        WHERE student_id = ? AND quiz_date = ?
    ''', (student_id, today)).fetchone()
    
    if not quiz:
        conn.close()
        return jsonify({'error': 'Quiz not found'}), 404
    
    quiz_data = json.loads(quiz['questions'])
    score = 0
    subject_scores = {}
    
    for i, answer in enumerate(answers):
        if i < len(quiz_data['questions']):
            q = quiz_data['questions'][i]
            subject = q.get('subject', 'Unknown')
            
            if subject not in subject_scores:
                subject_scores[subject] = {'correct': 0, 'total': 0}
            
            subject_scores[subject]['total'] += 1
            
            if answer == q['correct']:
                score += 1
                subject_scores[subject]['correct'] += 1
    
    # Generate AI feedback
    ai_feedback = ""
    if client:
        try:
            subject_analysis = '\n'.join([f"{subj}: {scores['correct']}/{scores['total']}" 
                                        for subj, scores in subject_scores.items()])
            
            prompt = f"""Student scored {score}/15 on academic quiz covering 3 subjects:

Performance by subject:
{subject_analysis}

Provide brief, actionable feedback (2-3 sentences) highlighting strengths and areas to focus on."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            ai_feedback = response.choices[0].message.content.strip()
        except:
            ai_feedback = f"You scored {score}/15 across all subjects. Review areas where you scored lower."
    
    conn.execute('''
        UPDATE academic_quiz_history 
        SET answers = ?, score = ?, total_questions = ?, ai_feedback = ?, completed = 1
        WHERE id = ?
    ''', (json.dumps(answers), score, 15, ai_feedback, quiz['id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'score': score,
        'total': 15,
        'subject_scores': subject_scores,
        'ai_feedback': ai_feedback
    })

@app.route('/api/dashboard-graph-data')
def dashboard_graph_data():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    student_id = session['student_id']
    conn = get_db()
    
    # Get last 30 days of career quiz scores
    career_scores = conn.execute('''
        SELECT quiz_date, score, total_questions 
        FROM career_quiz_history 
        WHERE student_id = ? AND completed = 1
        ORDER BY quiz_date DESC
        LIMIT 30
    ''', (student_id,)).fetchall()
    
    # Get last 30 days of academic quiz scores
    academic_scores = conn.execute('''
        SELECT quiz_date, score, total_questions 
        FROM academic_quiz_history 
        WHERE student_id = ? AND completed = 1
        ORDER BY quiz_date DESC
        LIMIT 30
    ''', (student_id,)).fetchall()
    
    # Get last 30 days of wellbeing scores
    wellbeing_scores = conn.execute('''
        SELECT assessment_date, total_score 
        FROM wellbeing_assessments 
        WHERE student_id = ?
        ORDER BY assessment_date DESC
        LIMIT 30
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'career_quiz': [{'date': r['quiz_date'], 'score': r['score'], 'total': r['total_questions']} 
                       for r in reversed(career_scores)],
        'academic_quiz': [{'date': r['quiz_date'], 'score': r['score'], 'total': r['total_questions']} 
                         for r in reversed(academic_scores)],
        'wellbeing': [{'date': r['assessment_date'], 'score': r['total_score']} 
                     for r in reversed(wellbeing_scores)]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
