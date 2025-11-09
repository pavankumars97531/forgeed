# ForgeEd - Deployment Guide for PyCharm (localhost)

This guide will help you deploy the ForgeEd application on your local machine using PyCharm.

## Prerequisites

- Python 3.11 or higher
- PyCharm IDE (Community or Professional)
- OpenAI API Key (you've already provided this)

## Step-by-Step Deployment

### 1. Download the Project Files

Download all the project files to your local machine. The project structure should look like this:

```
forgeed/
├── app.py                    # Main Flask application
├── database.py               # Database initialization
├── insert_sample_data.py     # Sample data insertion script
├── insert_data.sql           # SQL commands reference
├── forgeed.db               # SQLite database (will be created)
├── README.md                # Project documentation
├── DEPLOYMENT_GUIDE.md      # This file
├── static/
│   └── style.css            # Application styling
└── templates/
    ├── login.html           # Login page
    ├── dashboard.html       # Dashboard
    ├── courses.html         # Courses page
    ├── slu_gpt.html        # SLU GPT chat
    └── quiz.html            # Daily quiz
```

### 2. Open Project in PyCharm

1. Launch PyCharm
2. Click **File → Open**
3. Navigate to the `forgeed` folder and click **OK**
4. PyCharm will detect it's a Python project

### 3. Set Up Python Interpreter

1. Go to **File → Settings** (or **PyCharm → Preferences** on Mac)
2. Navigate to **Project: forgeed → Python Interpreter**
3. Click the **⚙️ icon** → **Add**
4. Select **Virtualenv Environment** → **New environment**
5. Choose Python 3.11 as base interpreter
6. Click **OK**

### 4. Install Dependencies

Open the Terminal in PyCharm (View → Tool Windows → Terminal) and run:

```bash
pip install flask openai python-dotenv
```

Or create a `requirements.txt` file with these contents:
```
flask
openai
python-dotenv
```

Then run:
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# In PyCharm Terminal
touch .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=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
```

**IMPORTANT**: Never commit the `.env` file to version control. Add it to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 6. Initialize the Database

In PyCharm Terminal, run:

```bash
python database.py
```

You should see:
```
Database initialized successfully!
```

### 7. Insert Sample Data

Run the sample data script:

```bash
python insert_sample_data.py
```

You should see:
```
Sample data inserted successfully!

Login credentials:
Email: ullasgowda@slu.edu
Password: password123
```

**To customize the data**:
- Edit `insert_sample_data.py` to change student info, courses, career goals
- Or use the SQL commands in `insert_data.sql` as a reference

### 8. Run the Application

In PyCharm Terminal, run:

```bash
python app.py
```

You should see output like:
```
Database initialized successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 9. Access the Application

1. Open your web browser
2. Navigate to: **http://localhost:5000**
3. You should see the ForgeEd login page

### 10. Log In and Explore

Use the demo credentials:
- **Email**: `ullasgowda@slu.edu`
- **Password**: `password123`

After logging in, explore:
- **Dashboard**: View stats, AI insights, and upcoming classes
- **My Courses**: See enrolled courses and AI-recommended courses
- **Daily Quiz**: Take a 10-question AI-generated quiz
- **SLU GPT**: Chat with the AI academic assistant

## Customizing Your Data

### Add Your Own Student

Edit `insert_sample_data.py` and modify the student data:

```python
cursor.execute('''
    INSERT INTO students (email, password, first_name, last_name, gpa, completion_rate, slu_gpt_sessions, career_goal) 
    VALUES ('your.email@slu.edu', 'your_password', 'Your', 'Name', 3.8, 85, 10, 'Your career goal here')
''')
```

### Add Your Own Courses

Modify the `courses_data` list in `insert_sample_data.py`:

```python
courses_data = [
    ('COURSE_CODE', 'Course Name', 3, 'Description', 'Instructor', 'Semester'),
    # Add more courses...
]
```

### Enroll in Different Courses

Modify the `enrolled_data` list (student_id, course_id, progress, grade, modules, assignments):

```python
enrolled_data = [
    (1, 1, 75, 'A', 6, 2),  # Student 1 enrolled in Course 1
    # Add more enrollments...
]
```

## Running in PyCharm (Alternative Method)

Instead of using the terminal, you can configure PyCharm to run the app:

1. Right-click on `app.py` in the Project view
2. Select **Run 'app'**
3. PyCharm will create a run configuration and start the server

## Troubleshooting

### Issue: "No module named 'flask'"
**Solution**: Install dependencies using `pip install flask openai python-dotenv`

### Issue: "OPENAI_API_KEY not set"
**Solution**: Make sure you created the `.env` file with your API key

### Issue: "Database not found"
**Solution**: Run `python database.py` to initialize the database first

### Issue: Port 5000 already in use
**Solution**: Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

### Issue: AI features not working
**Solution**: 
1. Verify your OpenAI API key is correct
2. Check your internet connection
3. Ensure you have API credits in your OpenAI account

## Production Deployment Notes

**For production deployment, you should:**

1. **Use a production WSGI server** (not Flask's built-in server):
   ```bash
   pip install gunicorn
   gunicorn app:app --bind 0.0.0.0:5000
   ```

2. **Hash passwords** (never use plaintext in production):
   - Use `bcrypt` or `argon2` to hash passwords
   - Update the login logic to verify hashed passwords

3. **Set a secure session secret**:
   - Generate a random secret key
   - Set it in the `.env` file as `SESSION_SECRET`

4. **Enable HTTPS** for secure communication

5. **Use a production database** (PostgreSQL, MySQL) instead of SQLite

6. **Add error logging** and monitoring

7. **Set up backups** for the database

## Next Steps

Once the app is running:

1. Test all features (login, dashboard, courses, chat, quiz)
2. Customize the data to match your needs
3. Explore the AI features and see how they respond
4. Review the code in `app.py` to understand how it works
5. Check `README.md` for more detailed documentation

## Support

If you encounter any issues:

1. Check the console output for error messages
2. Review the logs in PyCharm's Run window
3. Verify all files are in the correct locations
4. Ensure Python 3.11+ is being used
5. Make sure all dependencies are installed

Enjoy using ForgeEd! 🎓
