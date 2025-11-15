import sqlite3
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from database import get_db

load_dotenv()

def generate_90day_roadmap(student_id):
    """Generate a 90-day learning roadmap based on student's career goal using ChatGPT"""
    
    # Get student's career goal
    conn = get_db()
    cursor = conn.cursor()
    
    student = cursor.execute('SELECT career_goal, first_name FROM students WHERE id = ?', (student_id,)).fetchone()
    
    if not student:
        print(f"Student with ID {student_id} not found")
        return
    
    career_goal = student['career_goal']
    student_name = student['first_name']
    
    print(f"Generating 90-day roadmap for {student_name}'s career goal: {career_goal}")
    
    # Use OpenAI to generate roadmap
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""Create a 90-day learning roadmap for: {career_goal}

Generate day-by-day topics (1-90) that progress from basics to advanced. Each day = 2 hours of study.

Return ONLY a JSON array with 90 objects:
[{{"day": 1, "topic": "Introduction to Machine Learning", "description": "Learn ML basics and terminology"}}, ...]

Keep descriptions under 15 words. Focus on: fundamentals → tools → projects → advanced topics."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer. Return only valid JSON array with 90 learning topics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=6000
        )
        
        roadmap_json = response.choices[0].message.content.strip()
        
        # Clean up the response (remove markdown code blocks if present)
        if roadmap_json.startswith('```json'):
            roadmap_json = roadmap_json[7:]
        if roadmap_json.startswith('```'):
            roadmap_json = roadmap_json[3:]
        if roadmap_json.endswith('```'):
            roadmap_json = roadmap_json[:-3]
        roadmap_json = roadmap_json.strip()
        
        roadmap = json.loads(roadmap_json)
        
        print(f"Successfully generated roadmap with {len(roadmap)} days")
        
        # Insert into database
        for day_data in roadmap:
            day_number = day_data['day']
            topic = day_data['topic']
            description = day_data.get('description', '')
            
            # Check if roadmap entry already exists
            existing = cursor.execute(
                'SELECT id FROM daily_roadmap WHERE student_id = ? AND day_number = ?',
                (student_id, day_number)
            ).fetchone()
            
            if existing:
                # Update existing entry
                cursor.execute('''
                    UPDATE daily_roadmap 
                    SET topic = ?, theory_content = ?
                    WHERE student_id = ? AND day_number = ?
                ''', (topic, description, student_id, day_number))
            else:
                # Insert new entry
                cursor.execute('''
                    INSERT INTO daily_roadmap (student_id, day_number, topic, theory_content, study_duration)
                    VALUES (?, ?, ?, ?, 120)
                ''', (student_id, day_number, topic, description))
        
        conn.commit()
        print(f"✓ 90-day roadmap successfully saved to database for {student_name}!")
        
        # Display first 5 days as preview
        print("\nPreview of first 5 days:")
        for i, day in enumerate(roadmap[:5], 1):
            print(f"Day {day['day']}: {day['topic']}")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response: {roadmap_json[:500]}")
    except Exception as e:
        print(f"Error generating roadmap: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # Generate roadmap for student ID 1 (Ullas Gowda)
    generate_90day_roadmap(1)
