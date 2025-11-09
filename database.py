import sqlite3
from datetime import datetime

def get_db():
    conn = sqlite3.connect('forgeed.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gpa REAL DEFAULT 0.0,
            completion_rate INTEGER DEFAULT 0,
            slu_gpt_sessions INTEGER DEFAULT 0,
            career_goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            description TEXT,
            instructor TEXT,
            semester TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrolled_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            progress INTEGER DEFAULT 0,
            grade TEXT,
            modules_completed INTEGER DEFAULT 0,
            pending_assignments INTEGER DEFAULT 0,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE(student_id, course_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS available_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            description TEXT,
            semester TEXT,
            prerequisites TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            quiz_date DATE NOT NULL,
            questions TEXT NOT NULL,
            answers TEXT,
            score INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
