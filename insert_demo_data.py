import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('forgeed.db')
cursor = conn.cursor()

# Clear existing demo data (keep admin and any existing students)
print("Setting up demo data...")

# Student profiles with diverse backgrounds
students = [
    {
        'email': 'alice.chen@slu.edu',
        'password': 'Alice@123',
        'first_name': 'Alice',
        'last_name': 'Chen',
        'gpa': 3.95,
        'educational_background': 'Bachelor of Science in Computer Science from MIT',
        'career_goal': 'Machine Learning Engineer at Google',
        'wellbeing_avg': 85,
        'quiz_performance': 'excellent'  # 85-95%
    },
    {
        'email': 'bob.martinez@slu.edu',
        'password': 'Bob@123',
        'first_name': 'Bob',
        'last_name': 'Martinez',
        'gpa': 2.3,
        'educational_background': 'Associate Degree in General Studies from Community College',
        'career_goal': 'IT Support Specialist',
        'wellbeing_avg': 45,
        'quiz_performance': 'poor'  # 40-55%
    },
    {
        'email': 'carol.wang@slu.edu',
        'password': 'Carol@123',
        'first_name': 'Carol',
        'last_name': 'Wang',
        'gpa': 3.0,
        'educational_background': 'Bachelor of Arts in Business Administration from State University',
        'career_goal': 'Business Analyst',
        'wellbeing_avg': 65,
        'quiz_performance': 'average'  # 65-75%
    },
    {
        'email': 'david.patel@slu.edu',
        'password': 'David@123',
        'first_name': 'David',
        'last_name': 'Patel',
        'gpa': 3.6,
        'educational_background': 'Bachelor of Engineering in Information Technology from IIT Delhi',
        'career_goal': 'Cloud Solutions Architect',
        'wellbeing_avg': 75,
        'quiz_performance': 'good'  # 75-85%
    },
    {
        'email': 'emma.johnson@slu.edu',
        'password': 'Emma@123',
        'first_name': 'Emma',
        'last_name': 'Johnson',
        'gpa': 2.8,
        'educational_background': 'Bachelor of Science in Mathematics from Liberal Arts College',
        'career_goal': 'Data Scientist',
        'wellbeing_avg': 58,
        'quiz_performance': 'below_average'  # 55-65%
    }
]

# Create students with accounts created 120 days ago (so they have access to 90+ days of roadmap)
created_at = (datetime.now() - timedelta(days=120)).isoformat()

for student_data in students:
    # Insert student
    cursor.execute('''
        INSERT INTO students (email, password, first_name, last_name, gpa, 
                            educational_background, career_goal, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_data['email'], student_data['password'], student_data['first_name'],
          student_data['last_name'], student_data['gpa'], student_data['educational_background'],
          student_data['career_goal'], created_at))
    
    student_id = cursor.lastrowid
    print(f"Created student: {student_data['first_name']} {student_data['last_name']} (ID: {student_id})")
    
    # Create 90-day roadmap (simplified version)
    topics = [
        "Introduction to Programming", "Variables and Data Types", "Control Structures",
        "Functions and Scope", "Data Structures", "Object-Oriented Programming",
        "Algorithms Basics", "Sorting and Searching", "Trees and Graphs",
        "Database Fundamentals", "SQL Queries", "Normalization",
        "Web Development Basics", "HTML and CSS", "JavaScript Fundamentals",
        "Frontend Frameworks", "Backend Development", "RESTful APIs",
        "Cloud Computing Basics", "AWS Services", "Containerization",
        "DevOps Practices", "CI/CD Pipelines", "Monitoring and Logging",
        "Security Fundamentals", "Authentication", "Authorization",
        "Testing Strategies", "Unit Testing", "Integration Testing",
        "Design Patterns", "SOLID Principles", "Clean Code",
        "Agile Methodologies", "Scrum Framework", "Sprint Planning",
        "Version Control", "Git Workflows", "Collaboration Tools",
        "System Design Basics", "Scalability", "Load Balancing",
        "Microservices", "Message Queues", "Caching Strategies",
        "Performance Optimization", "Code Profiling", "Debugging",
        "Mobile Development", "iOS Basics", "Android Fundamentals",
        "React Native", "Cross-platform Tools", "Mobile UI/UX",
        "Machine Learning Intro", "Supervised Learning", "Unsupervised Learning",
        "Neural Networks", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Model Training", "Model Deployment",
        "Big Data Concepts", "Hadoop Ecosystem", "Spark Processing",
        "Data Warehousing", "ETL Processes", "Data Pipelines",
        "Business Intelligence", "Data Visualization", "Analytics Tools",
        "Project Management", "Requirements Gathering", "Stakeholder Communication",
        "Documentation", "Code Reviews", "Technical Writing",
        "Soft Skills", "Team Collaboration", "Leadership",
        "Career Development", "Resume Building", "Interview Preparation",
        "Networking", "Personal Branding", "Professional Growth",
        "Industry Trends", "Emerging Technologies", "Continuous Learning",
        "Ethics in Tech", "Data Privacy", "Responsible AI",
        "Open Source", "Contributing to Projects", "Community Building",
        "Freelancing", "Consulting", "Entrepreneurship",
        "Final Project Planning", "Implementation", "Presentation"
    ]
    
    for day in range(1, 91):
        topic = topics[day - 1] if day <= len(topics) else f"Advanced Topic {day}"
        completed = 1 if day <= 15 else 0  # First 15 days completed
        cursor.execute('''
            INSERT INTO daily_roadmap (student_id, day_number, topic, theory_content, 
                                      is_completed, study_duration)
            VALUES (?, ?, ?, ?, ?, 120)
        ''', (student_id, day, topic, f"Learn about {topic} fundamentals and applications", completed))
    
    # Enroll in 3 courses (completed 1 semester)
    courses = cursor.execute('SELECT id FROM courses LIMIT 3').fetchall()
    
    for course in courses:
        # Calculate grade based on student performance
        if student_data['quiz_performance'] == 'excellent':
            grade = random.uniform(90, 98)
            progress = random.randint(95, 100)
        elif student_data['quiz_performance'] == 'good':
            grade = random.uniform(80, 89)
            progress = random.randint(85, 95)
        elif student_data['quiz_performance'] == 'average':
            grade = random.uniform(70, 79)
            progress = random.randint(75, 85)
        elif student_data['quiz_performance'] == 'below_average':
            grade = random.uniform(60, 69)
            progress = random.randint(65, 75)
        else:  # poor
            grade = random.uniform(50, 59)
            progress = random.randint(50, 65)
        
        cursor.execute('''
            INSERT INTO enrolled_courses (student_id, course_id, progress, grade, 
                                         modules_completed, pending_assignments)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, course[0], progress, f"{grade:.1f}", 
              random.randint(8, 12), random.randint(0, 3)))
    
    # Generate Career Quiz History (15 attempts for 15 completed days)
    for day in range(1, 16):
        quiz_date = (datetime.now() - timedelta(days=15-day)).date().isoformat()
        
        if student_data['quiz_performance'] == 'excellent':
            score = random.randint(85, 95)
        elif student_data['quiz_performance'] == 'good':
            score = random.randint(75, 85)
        elif student_data['quiz_performance'] == 'average':
            score = random.randint(65, 75)
        elif student_data['quiz_performance'] == 'below_average':
            score = random.randint(55, 65)
        else:  # poor
            score = random.randint(40, 55)
        
        topic = topics[day - 1] if day <= len(topics) else f"Advanced Topic {day}"
        
        cursor.execute('''
            INSERT INTO career_quiz_history (student_id, day_number, topic, score, total_questions,
                                            quiz_date, questions, answers, ai_feedback, completed)
            VALUES (?, ?, ?, ?, 10, ?, '[]', '[]', 'Good effort!', 1)
        ''', (student_id, day, topic, score, quiz_date))
    
    # Generate Academic Quiz History (10 attempts)
    for i in range(10):
        quiz_date = (datetime.now() - timedelta(days=30-i*3)).date().isoformat()
        
        if student_data['quiz_performance'] == 'excellent':
            score = random.randint(88, 97)
        elif student_data['quiz_performance'] == 'good':
            score = random.randint(78, 88)
        elif student_data['quiz_performance'] == 'average':
            score = random.randint(68, 78)
        elif student_data['quiz_performance'] == 'below_average':
            score = random.randint(58, 68)
        else:  # poor
            score = random.randint(42, 58)
        
        cursor.execute('''
            INSERT INTO academic_quiz_history (student_id, score, total_questions,
                                              quiz_date, questions, answers, ai_feedback, completed)
            VALUES (?, ?, 15, ?, '[]', '[]', 'Keep practicing!', 1)
        ''', (student_id, score, quiz_date))
    
    # Generate Wellbeing Assessments (30 days of data)
    for i in range(30):
        assessment_date = (datetime.now() - timedelta(days=29-i)).date().isoformat()
        
        # Vary around average with some randomness
        base_score = student_data['wellbeing_avg']
        happiness = max(10, min(100, base_score + random.randint(-15, 15)))
        stress = max(10, min(100, 100 - base_score + random.randint(-10, 10)))  # Inverse
        energy = max(10, min(100, base_score + random.randint(-10, 10)))
        motivation = max(10, min(100, base_score + random.randint(-12, 12)))
        sleep = max(10, min(100, base_score + random.randint(-8, 8)))
        total_score = int((happiness + (100 - stress) + energy + motivation + sleep) / 5)
        
        cursor.execute('''
            INSERT INTO wellbeing_assessments (student_id, assessment_date, happiness_score,
                                              stress_score, energy_score, motivation_score,
                                              sleep_quality, total_score, responses, ai_insights)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '{}', ?)
        ''', (student_id, assessment_date, happiness, stress, energy, motivation, sleep,
              total_score, "Keep maintaining your wellbeing routine!"))

conn.commit()
conn.close()

print("\n✅ Demo data created successfully!")
print("\n📋 Student Credentials:")
print("="*70)
for s in students:
    print(f"\n{s['first_name']} {s['last_name']} - {s['quiz_performance'].upper()} PERFORMER")
    print(f"  Email: {s['email']}")
    print(f"  Password: {s['password']}")
    print(f"  GPA: {s['gpa']}")
    print(f"  Background: {s['educational_background']}")
    print(f"  Career Goal: {s['career_goal']}")
