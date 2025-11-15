import sqlite3
from datetime import date, timedelta
import json

def seed_sample_data():
    """
    Seeds the database with 7 days of sample quiz and wellbeing data
    for the demo student (ID=1) to showcase dashboard trends.
    """
    conn = sqlite3.connect('forgeed.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get the first student
    student = cursor.execute('SELECT * FROM students LIMIT 1').fetchone()
    if not student:
        print("No students found in database. Please create a student first.")
        conn.close()
        return
    
    student_id = student['id']
    student_name = f"{student['first_name']} {student['last_name']}"
    print(f"Seeding data for student: {student_name} (ID: {student_id})")
    
    # Sample data for the past 7 days
    career_scores = [7, 8, 6, 9, 8, 7, 9]  # Out of 10
    academic_scores = [11, 13, 10, 14, 12, 13, 15]  # Out of 15
    wellbeing_scores = [65, 72, 68, 80, 75, 78, 85]  # 0-100 scale
    
    today = date.today()
    
    print("\nInserting Career Quiz history...")
    for i in range(7):
        quiz_date = (today - timedelta(days=6-i)).isoformat()
        score = career_scores[i]
        
        # Check if entry already exists
        existing = cursor.execute(
            'SELECT id FROM career_quiz_history WHERE student_id = ? AND quiz_date = ?',
            (student_id, quiz_date)
        ).fetchone()
        
        if existing:
            print(f"  Skipping {quiz_date} - already exists")
            continue
        
        # Sample quiz questions
        questions = {
            "questions": [
                {"q": f"Question {j+1}", "correct": "A", "options": ["A", "B", "C", "D"]}
                for j in range(10)
            ]
        }
        
        # Sample answers (some correct, some wrong)
        answers = ["A"] * score + ["B"] * (10 - score)
        
        cursor.execute('''
            INSERT INTO career_quiz_history 
            (student_id, day_number, topic, questions, answers, score, total_questions, quiz_date, completed, ai_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            i + 1,
            f"Career Topic Day {i+1}",
            json.dumps(questions),
            json.dumps(answers),
            score,
            10,
            quiz_date,
            1,
            f"Good job! You scored {score}/10 on this topic."
        ))
        print(f"  Added Career Quiz: {quiz_date} - Score: {score}/10")
    
    print("\nInserting Academic Quiz history...")
    for i in range(7):
        quiz_date = (today - timedelta(days=6-i)).isoformat()
        score = academic_scores[i]
        
        # Check if entry already exists
        existing = cursor.execute(
            'SELECT id FROM academic_quiz_history WHERE student_id = ? AND quiz_date = ?',
            (student_id, quiz_date)
        ).fetchone()
        
        if existing:
            print(f"  Skipping {quiz_date} - already exists")
            continue
        
        # Sample quiz questions
        questions = {
            "questions": [
                {
                    "q": f"Question {j+1}",
                    "correct": "A",
                    "options": ["A", "B", "C", "D"],
                    "subject": ["Database Systems", "Web Development", "Data Analytics"][j % 3]
                }
                for j in range(15)
            ]
        }
        
        # Sample answers (some correct, some wrong)
        answers = ["A"] * score + ["B"] * (15 - score)
        
        cursor.execute('''
            INSERT INTO academic_quiz_history 
            (student_id, questions, answers, score, total_questions, quiz_date, completed, ai_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            json.dumps(questions),
            json.dumps(answers),
            score,
            15,
            quiz_date,
            1,
            f"You scored {score}/15. Great work across all subjects!"
        ))
        print(f"  Added Academic Quiz: {quiz_date} - Score: {score}/15")
    
    print("\nInserting Wellbeing assessments...")
    for i in range(7):
        assessment_date = (today - timedelta(days=6-i)).isoformat()
        score = wellbeing_scores[i]
        
        # Check if entry already exists
        existing = cursor.execute(
            'SELECT id FROM wellbeing_assessments WHERE student_id = ? AND assessment_date = ?',
            (student_id, assessment_date)
        ).fetchone()
        
        if existing:
            print(f"  Skipping {assessment_date} - already exists")
            continue
        
        # Calculate happiness, stress, energy based on the overall score
        happiness = min(100, score + 5)
        stress = max(0, 100 - score - 10)
        energy = score
        motivation = min(100, score + 3)
        sleep_quality = min(100, score - 5)
        
        cursor.execute('''
            INSERT INTO wellbeing_assessments 
            (student_id, happiness_score, stress_score, energy_score, motivation_score, sleep_quality, 
             responses, total_score, ai_insights, assessment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            happiness,
            stress,
            energy,
            motivation,
            sleep_quality,
            json.dumps({"note": f"Sample responses for day {i+1}"}),
            score,
            f"Your overall wellbeing score is {score}. Keep up the positive momentum!",
            assessment_date
        ))
        print(f"  Added Wellbeing: {assessment_date} - Score: {score}")
    
    conn.commit()
    conn.close()
    print("\n✅ Sample data seeding completed successfully!")
    print("Refresh your dashboard to see the trend lines populated with data.")

if __name__ == '__main__':
    seed_sample_data()
