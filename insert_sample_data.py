import sqlite3

conn = sqlite3.connect('forgeed.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO students (email, password, first_name, last_name, gpa, completion_rate, slu_gpt_sessions, career_goal) 
    VALUES ('ullasgowda@slu.edu', 'password123', 'Ullas', 'Gowda', 3.85, 89, 47, 'Data Scientist specializing in Machine Learning and AI')
''')

courses_data = [
    ('IS 5000', 'Enterprise Architecture', 3, 'Fundamental concepts of enterprise architecture and system design', 'Dr. Mitchell', 'Fall 2025'),
    ('IS 5100', 'IS Strategy & Management', 3, 'Strategic planning and management of information systems', 'Dr. Johnson', 'Fall 2025'),
    ('IS 5200', 'Software Development', 3, 'Advanced software development methodologies and practices', 'Dr. Smith', 'Fall 2025'),
    ('IS 5400', 'Managing a Secure Enterprise', 3, 'Enterprise security management and cybersecurity strategies', 'Dr. Brown', 'Fall 2025'),
    ('IS 5600', 'Mobile & Web App Dev', 3, 'Modern mobile and web application development', 'Dr. Davis', 'Fall 2025'),
    ('IS 5800', 'Cloud Computing', 3, 'Cloud infrastructure, services, and deployment strategies', 'Dr. Wilson', 'Fall 2025')
]

for course in courses_data:
    cursor.execute('''
        INSERT INTO courses (course_code, course_name, credits, description, instructor, semester) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', course)

enrolled_data = [
    (1, 1, 78, 'A-', 6, 2),
    (1, 2, 85, 'A', 8, 1),
    (1, 3, 72, 'B+', 5, 3),
    (1, 4, 94, 'B', 7, 2),
    (1, 5, 92, 'A-', 9, 1),
    (1, 6, 82, 'A', 6, 2)
]

for enrollment in enrolled_data:
    cursor.execute('''
        INSERT INTO enrolled_courses (student_id, course_id, progress, grade, modules_completed, pending_assignments) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', enrollment)

available_courses_data = [
    ('IS 6100', 'Machine Learning Fundamentals', 3, 'Introduction to machine learning algorithms and applications', 'Spring 2026', 'IS 5200'),
    ('IS 6200', 'Deep Learning', 3, 'Advanced neural networks and deep learning techniques', 'Spring 2026', 'IS 6100'),
    ('IS 6300', 'Natural Language Processing', 3, 'Text processing and language understanding with AI', 'Spring 2026', 'IS 6100'),
    ('IS 6400', 'Big Data Analytics', 3, 'Processing and analyzing large-scale datasets', 'Spring 2026', 'IS 5200'),
    ('IS 6500', 'Data Visualization', 3, 'Creating effective data visualizations and dashboards', 'Spring 2026', 'None'),
    ('IS 6600', 'Advanced Database Systems', 3, 'Advanced database design and optimization', 'Spring 2026', 'IS 5000'),
    ('IS 6700', 'Computer Vision', 3, 'Image processing and computer vision applications', 'Spring 2026', 'IS 6100'),
    ('IS 6800', 'AI Ethics and Governance', 3, 'Ethical considerations in AI development and deployment', 'Spring 2026', 'None')
]

for course in available_courses_data:
    cursor.execute('''
        INSERT INTO available_courses (course_code, course_name, credits, description, semester, prerequisites) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', course)

conn.commit()
conn.close()

print("Sample data inserted successfully!")
print("\nLogin credentials:")
print("Email: ullasgowda@slu.edu")
print("Password: password123")
