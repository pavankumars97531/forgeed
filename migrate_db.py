import sqlite3

def migrate_database():
    conn = sqlite3.connect('forgeed.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN educational_background TEXT")
        print("Added educational_background column to students")
    except sqlite3.OperationalError:
        print("educational_background column already exists")
    
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        print("Added is_admin column to students")
    except sqlite3.OperationalError:
        print("is_admin column already exists")
    
    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN faculty_name TEXT")
        print("Added faculty_name column to courses")
    except sqlite3.OperationalError:
        print("faculty_name column already exists")
    
    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN intake_term TEXT")
        print("Added intake_term column to courses")
    except sqlite3.OperationalError:
        print("intake_term column already exists")
    
    cursor.execute("SELECT COUNT(*) FROM students WHERE email = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO students (email, password, first_name, last_name, is_admin, career_goal)
            VALUES ('admin', 'admin123', 'System', 'Administrator', 1, 'System Administration')
        """)
        print("Created admin account (admin/admin123)")
    else:
        cursor.execute("UPDATE students SET is_admin = 1 WHERE email = 'admin'")
        print("Updated existing admin account")
    
    conn.commit()
    conn.close()
    print("\nDatabase migration completed successfully!")

if __name__ == '__main__':
    migrate_database()
