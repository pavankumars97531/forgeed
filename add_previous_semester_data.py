import sqlite3
from datetime import datetime, timedelta
import json
import random

# Connect to database
conn = sqlite3.connect('forgeed.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get student ID
student = cursor.execute('SELECT id FROM students WHERE email = ?', ('ullasgowda@slu.edu',)).fetchone()
student_id = student['id']

# Get enrolled course IDs and names
courses = cursor.execute('''
    SELECT c.id, c.course_name 
    FROM enrolled_courses ec
    JOIN courses c ON ec.course_id = c.id
    WHERE ec.student_id = ?
''', (student_id,)).fetchall()

print(f"Adding previous semester data for student ID: {student_id}")
print(f"Courses: {[c['course_name'] for c in courses]}")

# Career topics for previous semester
career_topics = [
    "Cloud Computing Fundamentals",
    "DevOps Best Practices",
    "Microservices Architecture",
    "API Design Principles",
    "Database Optimization",
    "Security in Software Development",
    "Agile Project Management",
    "System Design Patterns",
    "Performance Monitoring",
    "CI/CD Pipelines",
    "Containerization Basics",
    "Infrastructure as Code"
]

# Add academic quiz history for previous semester (4-6 months ago)
# Create 12 weekly academic quizzes over last semester
quiz_count = 0
for week in range(12):
    quiz_date = (datetime.now() - timedelta(days=180 - week*7)).strftime('%Y-%m-%d')
    
    # Generate quiz with 5 questions per course (15 total)
    questions_data = {"questions": []}
    
    for course in courses:
        for i in range(5):
            questions_data["questions"].append({
                "subject": course['course_name'],
                "question": f"Sample question {i+1} for {course['course_name']}",
                "correct_answer": "Sample answer",
                "student_answer": "Sample answer"
            })
    
    # Random score between 11-14 out of 15 (good performance)
    score = random.randint(11, 14)
    total_questions = 15
    
    cursor.execute('''
        INSERT INTO academic_quiz_history 
        (student_id, quiz_date, score, total_questions, questions, completed, ai_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id,
        quiz_date,
        score,
        total_questions,
        json.dumps(questions_data),
        1,
        f"Great work! You scored {score}/{total_questions}. Keep up the excellent effort."
    ))
    quiz_count += 1
    
print(f"✅ Added {quiz_count} academic quiz records")

# Add career quiz history for previous semester
career_quiz_count = 0
for week in range(12):
    quiz_date = (datetime.now() - timedelta(days=180 - week*7)).strftime('%Y-%m-%d')
    day_number = week + 1  # Days 1-12 from previous semester
    topic = career_topics[week]
    
    questions_data = {"questions": []}
    for i in range(10):
        questions_data["questions"].append({
            "question": f"Career question {i+1} about {topic}",
            "correct_answer": "Sample answer",
            "student_answer": "Sample answer"
        })
    
    # Random score between 7-9 out of 10
    score = random.randint(7, 9)
    total_questions = 10
    
    cursor.execute('''
        INSERT INTO career_quiz_history 
        (student_id, day_number, topic, quiz_date, score, total_questions, questions, completed, ai_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id,
        day_number,
        topic,
        quiz_date,
        score,
        total_questions,
        json.dumps(questions_data),
        1,
        f"Excellent progress on {topic}! You scored {score}/{total_questions}."
    ))
    career_quiz_count += 1

print(f"✅ Added {career_quiz_count} career quiz records")

# Add wellbeing assessments for previous semester
wellbeing_count = 0
for week in range(12):
    assessment_date = (datetime.now() - timedelta(days=180 - week*7)).strftime('%Y-%m-%d')
    
    # Random wellbeing scores (generally positive)
    happiness = random.randint(65, 90)
    stress = random.randint(30, 60)
    energy = random.randint(60, 85)
    motivation = random.randint(70, 90)
    sleep_quality = random.randint(60, 85)
    total_score = int((happiness + (100-stress) + energy + motivation + sleep_quality) / 5)
    
    responses_data = {
        "happiness": happiness,
        "stress": stress,
        "energy": energy,
        "motivation": motivation,
        "sleep_quality": sleep_quality
    }
    
    cursor.execute('''
        INSERT INTO wellbeing_assessments 
        (student_id, assessment_date, happiness_score, stress_score, energy_score, motivation_score, 
         sleep_quality, responses, total_score, ai_insights)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id,
        assessment_date,
        happiness,
        stress,
        energy,
        motivation,
        sleep_quality,
        json.dumps(responses_data),
        total_score,
        f"You're maintaining good balance with happiness at {happiness}% and manageable stress at {stress}%."
    ))
    wellbeing_count += 1

print(f"✅ Added {wellbeing_count} wellbeing assessment records")

# Commit changes
conn.commit()
conn.close()

print("\n🎉 Previous semester data added successfully!")
print(f"   - {quiz_count} academic quizzes")
print(f"   - {career_quiz_count} career quizzes")  
print(f"   - {wellbeing_count} wellbeing assessments")
print("   - Data spans approximately 12 weeks (one semester)")
