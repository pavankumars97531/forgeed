# ForgeEd - AI-Enhanced Learning Management System

An AI-powered Learning Management System built with Flask and OpenAI GPT integration, designed for Saint Louis University's MS in Information Systems students.

## Features

### Core Features
- **Student Dashboard**: Track GPA, completion rate, Career Quiz performance, Academic Quiz performance, and Wellbeing scores
- **Career Learning System**: 90-day personalized learning roadmap with day-locking mechanism, AI-generated theory content, and curated external resources
- **Dual Quiz System**: 
  - Career Learning Quiz (10 questions on daily roadmap topic)
  - Academic Quiz (15 questions from enrolled courses)
  - AI-powered auto-scoring with personalized feedback
- **Wellbeing Tracking**: Daily mental health assessments with emoji sliders (happiness, stress, energy, motivation, sleep) and AI-generated motivational insights
- **Performance Analytics**: Interactive Chart.js line graphs tracking Career Quiz, Academic Quiz, and Wellbeing scores over time
- **SLU GPT Chat Assistant**: Context-aware conversational AI with rich text formatting (headers, bold, lists, code blocks) that understands enrolled courses and career goals
- **Course Management**: Enrollment tracking, progress monitoring, and AI-powered course recommendations based on actual university courses
- **Admin Dashboard**: Comprehensive administrative interface for managing students, courses, and monitoring student performance

### AI-Powered Features
- Performance analysis and personalized insights
- Context-aware chat assistant (SLU GPT)
- Course recommendations based on career goals and educational background
- 90-day roadmap generation
- Theory content generation for each roadmap topic
- Career Quiz auto-generation (10 questions per day)
- Academic Quiz auto-generation (15 questions from 3 courses)
- Quiz auto-scoring with personalized feedback
- Wellbeing insights and motivational support

### Admin Features
- **Manage Students**: Add/delete students with automatic roadmap generation
- **Manage Courses**: Add/delete courses from the catalog
- **Student Monitoring**: View comprehensive student performance metrics including GPA, wellbeing scores, and risk levels

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **AI**: OpenAI GPT API
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Authentication**: Flask Sessions

## Installation & Setup

### Prerequisites
- Python 3.x
- OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/forgeed.git
cd forgeed
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- Flask-Login
- Flask-WTF
- OpenAI
- python-dotenv

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
SESSION_SECRET=your_secret_key_here
```

### 4. Initialize Database

```bash
python database.py
```

### 5. (Optional) Load Sample Data

```bash
python seed_sample_data.py
```

This will create:
- 10 diverse student profiles with varying performance levels
- Sample course catalog
- Historical quiz and wellbeing data

### 6. Run the Application

```bash
python app.py
```

The app will run on `http://localhost:5000`

## Default Login Credentials

### Admin Access
- **Email**: `admin@edu`
- **Password**: `Password@123`

### Sample Student Accounts
After running `seed_sample_data.py`, you can log in as any student:
- **Emails**: `ullasgowda@slu.edu`, `alice.johnson@slu.edu`, `bob.smith@slu.edu`, etc.
- **Password**: `password123` (for all sample students)

## Database Schema

The application uses SQLite with the following tables:

- **students**: User credentials, GPA, completion rates, career goals, educational background, admin status
- **courses**: Catalog of available courses with course codes, names, descriptions, faculty names, intake terms
- **enrolled_courses**: Junction table linking students to courses with progress tracking and grades
- **daily_roadmap**: 90-day personalized career learning topics with theory content, resources, completion tracking
- **career_quiz_history**: Records of Career Learning Quiz attempts with scores, answers, and AI feedback
- **academic_quiz_history**: Records of Academic Quiz attempts with scores, answers, and AI feedback
- **wellbeing_assessments**: Daily wellbeing check-ins with happiness/stress/energy scores and AI insights

## Project Structure

```
forgeed/
├── app.py                      # Flask application with routes and AI logic
├── database.py                 # Database initialization script
├── analytics_service.py        # Performance analytics and risk calculation
├── generate_roadmap.py         # AI-powered 90-day roadmap generator
├── seed_sample_data.py         # Sample data generator
├── insert_sample_data.py       # Legacy sample data insertion
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── forgeed.db                  # SQLite database (created after running database.py)
├── static/
│   └── style.css              # ForgeEd UI styling with color-coordinated design
├── templates/
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard with stats and insights
│   ├── courses.html           # Course management and AI recommendations
│   ├── career_learning.html   # 90-day roadmap interface
│   ├── quiz.html              # Dual quiz system (Career + Academic)
│   ├── wellbeing.html         # Daily wellbeing assessment
│   ├── analytics.html         # Student performance analytics
│   ├── slu_gpt.html          # AI chat interface
│   └── admin.html             # Admin dashboard
└── README.md                  # This file
```

## Key Features Explained

### 90-Day Career Learning Roadmap
- Personalized learning path based on career goals
- Day-locking mechanism ensures sequential progression
- AI-generated theory content for each topic
- External resource links for further learning
- Automatic completion on quiz submission

### Dual Quiz System
- **Career Quiz**: 10 questions on the current day's roadmap topic
- **Academic Quiz**: 15 questions (5 from each of 3 enrolled courses)
- AI auto-scoring with personalized feedback
- Historical tracking and performance graphs

### Wellbeing Tracking
- Daily assessments with 5 emoji sliders (1-100 scale)
- Metrics: Happiness, Stress, Energy, Motivation, Sleep Quality
- AI-generated motivational insights
- Performance correlation analysis

### Color-Coordinated Design
- **Blue (#2196F3)**: Academic/GPA metrics
- **Purple (#9b7fd7)**: Career learning metrics
- **Orange (#f4a261)**: Wellbeing metrics

### Admin Dashboard
- Add/delete students with automatic roadmap generation
- Manage course catalog
- Monitor student performance and risk levels
- Risk calculation based on quiz performance

## Risk Level Calculation

Student risk levels are calculated based on quiz performance:
- **High Risk**: Average quiz score < 50%
- **Medium Risk**: Average quiz score 50-79%
- **Low Risk**: Average quiz score ≥ 80%

## API Endpoints

### Student Endpoints
- `GET /dashboard` - Main dashboard
- `GET /courses` - Course management
- `GET /career-learning` - 90-day roadmap
- `GET /quiz` - Dual quiz system
- `GET /wellbeing` - Daily wellbeing assessment
- `GET /analytics` - Performance analytics
- `GET /slu-gpt` - AI chat interface

### API Endpoints
- `POST /api/submit-career-quiz` - Submit Career Quiz
- `POST /api/submit-academic-quiz` - Submit Academic Quiz
- `POST /api/submit-wellbeing` - Submit wellbeing assessment
- `POST /api/chat` - SLU GPT chat
- `GET /api/get-day-content/<day>` - Get roadmap day content
- `POST /api/complete-day` - Mark roadmap day as complete
- `GET /api/dashboard-graph-data` - Dashboard graph data
- `GET /api/analytics-data` - Student analytics data

### Admin Endpoints
- `GET /admin/dashboard` - Admin interface
- `POST /api/admin/add-student` - Add new student
- `POST /api/admin/delete-student` - Delete student
- `POST /api/admin/add-course` - Add new course
- `POST /api/admin/delete-course` - Delete course

## Customization

### Modify AI Prompts
Edit prompts in `app.py`:
- SLU GPT context: `/api/chat` route
- Dashboard insights: `generate_ai_insights()` function
- Course recommendations: `get_ai_course_recommendations()` function
- Quiz generation: `/api/generate-career-quiz` and `/api/generate-academic-quiz` routes

### Change UI Colors
Edit CSS variables in `static/style.css`:
- `--color-academic`: Academic metrics color
- `--color-career`: Career metrics color
- `--color-wellbeing`: Wellbeing metrics color

### Add New Features
1. Create new route in `app.py`
2. Create new template in `templates/`
3. Add navigation link in sidebar
4. Update database schema if needed

## Deployment

See `DEPLOYMENT_GUIDE.md` for deployment instructions.

## Security Notes

- Current implementation stores passwords in plain text (development only)
- For production: Implement password hashing (bcrypt/argon2)
- Use strong SESSION_SECRET in production
- Secure OpenAI API key using environment variables

## Troubleshooting

**Database not found**: Run `python database.py` first

**No courses showing**: Run `python seed_sample_data.py` to load sample data

**AI not responding**: Verify OPENAI_API_KEY is set correctly in `.env`

**Login fails**: Check that student data exists in database

**External links not showing**: Resources fallback to default links (MDN, W3Schools, FreeCodeCamp)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Credits

Built for Saint Louis University's MS in Information Systems program.

## Support

For questions or issues, please open an issue on GitHub.
