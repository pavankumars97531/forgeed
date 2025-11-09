# ForgeEd - AI-Enhanced Learning Management System

An AI-powered student learning management system built with Flask and OpenAI ChatGPT integration for Saint Louis University MS in Information Systems students.

## Features

- **Student Dashboard**: Track GPA, completion rate, enrolled courses, and SLU GPT sessions
- **AI-Powered Insights**: ChatGPT analyzes your performance and provides personalized recommendations
- **SLU GPT Chat**: Context-aware AI assistant trained on Saint Louis University and your specific courses
- **Course Management**: View enrolled courses with progress tracking and grades
- **AI Course Recommendations**: Get 3 personalized course suggestions based on your career goals
- **Daily AI Quiz**: 10 auto-generated questions tailored to your courses and career goals
- **Auto-Scoring**: Quiz results are automatically scored and stored
- **Online Resource Suggestions**: AI recommends external learning resources when needed

## Installation & Setup

### 1. Install Dependencies

The required packages are already installed:
- Flask
- OpenAI Python SDK
- SQLite3 (built-in)

### 2. Initialize Database

Run the database initialization script:

```bash
python database.py
```

### 3. Insert Your Data

Edit `insert_data.sql` with your student information, courses, and available courses, then run:

```bash
sqlite3 forgeed.db < insert_data.sql
```

**Important**: Update these sections in `insert_data.sql`:
- **Student Information**: Your email, password, name, GPA, career goal
- **Courses**: Your university's course catalog
- **Enrolled Courses**: Courses you're currently taking
- **Available Courses**: Courses available for next semester

### 4. Set OpenAI API Key

The API key is already configured in the environment.

### 5. Run the Application

```bash
python app.py
```

The app will run on `http://localhost:5000`

## Default Login Credentials

After inserting the sample data from `insert_data.sql`:
- **Email**: `ullasgowda@slu.edu`
- **Password**: `password123`

## Database Schema

The application uses SQLite with the following tables:

- `students`: Student information, GPA, career goals
- `courses`: University course catalog
- `enrolled_courses`: Student course enrollments with progress
- `available_courses`: Courses available for enrollment
- `chat_history`: SLU GPT conversation history
- `quiz_history`: Daily quiz questions, answers, and scores

## SQL Commands for Data Management

### View All Students
```sql
SELECT * FROM students;
```

### View All Courses
```sql
SELECT * FROM courses;
```

### View Student's Enrolled Courses
```sql
SELECT c.course_code, c.course_name, ec.progress, ec.grade
FROM enrolled_courses ec
JOIN courses c ON ec.course_id = c.id
WHERE ec.student_id = 1;
```

### Update Student's Career Goal
```sql
UPDATE students 
SET career_goal = 'Your new career goal here'
WHERE id = 1;
```

### Add New Available Course
```sql
INSERT INTO available_courses (course_code, course_name, credits, description, semester, prerequisites)
VALUES ('IS 7000', 'Advanced AI', 3, 'Deep dive into AI concepts', 'Spring 2026', 'IS 6100');
```

## How AI Features Work

### 1. SLU GPT Chat
- Every message includes context about Saint Louis University, MS in Information Systems program
- AI knows your enrolled courses and career goal
- Conversation history is saved to database

### 2. Course Recommendations
- AI analyzes your career goal
- Compares with available courses
- Recommends top 3 most relevant courses
- Considers prerequisites and course descriptions

### 3. Daily Quiz
- AI generates 10 unique questions daily
- Questions are based on your current courses and career goal
- Returned in structured JSON format for proper UI rendering
- Auto-scored when submitted
- One quiz per day (resets at midnight)

### 4. AI Insights
- Dashboard shows 3 AI-generated insights
- Based on your GPA, completion rate, and course progress
- Provides positive feedback, warnings, and recommendations

## Project Structure

```
forgeed/
├── app.py                 # Flask application with routes and AI logic
├── database.py            # Database initialization script
├── insert_data.sql        # SQL commands to insert your data
├── forgeed.db            # SQLite database (created after running database.py)
├── static/
│   └── style.css         # ForgeEd UI styling (blue gradient theme)
├── templates/
│   ├── login.html        # Login page
│   ├── dashboard.html    # Main dashboard with stats and insights
│   ├── courses.html      # Course management and AI recommendations
│   ├── slu_gpt.html      # AI chat interface
│   └── quiz.html         # Daily quiz page
└── README.md             # This file
```

## Deploying to PyCharm

1. Open PyCharm and create a new project
2. Copy all files to your project directory
3. Open Terminal in PyCharm
4. Run: `python database.py`
5. Edit and run: `sqlite3 forgeed.db < insert_data.sql`
6. Run: `python app.py`
7. Open browser to `http://localhost:5000`

## Customization

### Change UI Colors
Edit `static/style.css` - look for color values like `#4a5fc1` (main blue)

### Add More Pages
1. Create new route in `app.py`
2. Create new template in `templates/`
3. Add navigation link in sidebar

### Modify AI Prompts
Edit the system prompts in `app.py`:
- `chat()` function: SLU GPT context
- `generate_ai_insights()`: Dashboard insights
- `get_ai_course_recommendations()`: Course recommendations
- `generate_quiz()`: Quiz generation

## Troubleshooting

**Database not found**: Run `python database.py` first

**No courses showing**: Make sure you ran `sqlite3 forgeed.db < insert_data.sql`

**AI not responding**: Verify OpenAI API key is set correctly

**Login fails**: Check that student data was inserted into database

## Future Enhancements

- Assignment tracking and deadline management
- Progress analytics with charts
- Schedule/calendar view
- Profile editing
- Quiz history and performance trends
- Email notifications
- Mobile responsive design improvements
