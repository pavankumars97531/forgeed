# 🎓 ForgeEd - AI-Enhanced Learning Management System

![ForgeEd Logo](https://forgeed.replit.app/static/logo.png)

**An AI-powered Learning Management System built with Flask and OpenAI GPT integration, designed for Saint Louis University's MS in Information Systems students.**

---

## 📋 Table of Contents
1. [Team & Project Overview](#team--project-overview)
2. [Executive Summary](#executive-summary)
3. [Problem Context & Stakeholders](#problem-context--stakeholders)
4. [Research & Insights](#research--insights)
5. [Proposed Solution](#proposed-solution)
6. [Project Charter](#project-charter)
7. [Architecture & Data Design](#architecture--data-design)
8. [Dashboard & Data Analysis](#dashboard--data-analysis)
9. [Ethical & Social Considerations](#ethical--social-considerations)
10. [Lessons Learned & Team Reflection](#lessons-learned--team-reflection)
11. [Core Features](#core-features)
12. [Tech Stack](#tech-stack)
13. [Installation & Setup](#installation--setup)
14. [API Endpoints](#api-endpoints)
15. [Appendix](#appendix)

---

## 🎯 Team & Project Overview

**Project Title:** ForgeEd - AI-Enhanced Learning Management System

**Team Members (MRP Team 1):**
- Ullas Giddegowda Gowda
- Pavan Kumar Suresh
- Pranay Reddy Shashidhar Reddy
- Ruthvik Ajit Chiniwal
- Harshith Shivaswamy

**Institution:** Saint Louis University - MS in Information Systems Program

**Live URL:** https://forgeed.replit.app/

**GitHub Repository:** [ForgeEd Repository]

---

## 📊 Executive Summary

The rapid evolution of Generative AI is reshaping expectations in higher education, yet most university systems remain fragmented—separating academics, wellbeing, and career development into disconnected platforms. Through our Master's Research Project, Team Forge examined this critical gap and identified the core challenge: **students lack a unified, personalized support system that can guide them academically, emotionally, and professionally.**

This fragmentation results in:
- Inconsistent academic performance
- Poor course selection and planning
- Disconnected mental health support
- Limited career preparedness

To address this systemic problem, our team developed **ForgeEd**, an AI-enhanced Learning Management System specifically designed for Saint Louis University. ForgeEd integrates traditional LMS capabilities with advanced GenAI features, including:

✅ **Personalized Tutoring** (SLU GPT) - 24/7 AI academic support  
✅ **AI-Generated Learning Pathways** - 90-day career learning roadmaps  
✅ **Dual-Quiz Assessments** - Career and academic performance tracking  
✅ **Wellbeing Monitoring** - Daily mental health indicators  
✅ **Predictive Analytics** - Early risk detection and intervention  
✅ **Dynamic Recommendations** - Personalized learning and course suggestions  

**Expected Impact:** Improved GPA outcomes, early detection of academic risk, increased student engagement, better career alignment, and reduced faculty workload through intelligent automation.

---

## 🔍 Problem Context & Stakeholders

### The Challenge
Higher education is undergoing significant transformation as universities attempt to integrate emerging GenAI technologies into traditional academic structures. Despite rapid innovation across learning platforms, most institutions—including Saint Louis University—continue to rely on fragmented systems that separately manage courses, wellbeing services, and career support.

**Core Problem:** Students do not receive integrated, timely, and personalized support across academics, wellbeing, and career development, leading to:
- Irregular academic performance
- Unnecessary stress
- Inefficient course planning
- Limited preparedness for industry roles

### Key Stakeholders

**Students (Primary)**
- Struggle with navigating multiple systems for assignments, grades, and career resources
- Lack actionable insights into academic trajectory and skill gaps
- Need early warning systems and predictive insights for timely intervention

**Faculty Members**
- Face pressure to provide individualized feedback while managing grading and administration
- Have limited visibility into student challenges and engagement patterns
- Cannot deliver targeted support without consolidated data

**Academic Advisors & Program Coordinators**
- Require holistic student views for course selection and progress monitoring
- Currently piece together information manually, increasing workload
- Need data-driven systems for personalized academic planning

**University Administration**
- Aim to enhance retention rates and support student wellbeing
- Lack consolidated dashboards or predictive analytics
- Need resource allocation insights and program-level risk identification

**Industry & Education Partners**
- Expect graduates with strong technical skills, adaptability, and emotional resilience
- Require evidence of career readiness and non-academic growth

---

## 🔬 Research & Insights

### Industry Trends Identified

Our research highlighted several industry-wide trends relevant to SLU's environment:

1. **GenAI-Driven Adaptive Learning** - Personalized, dynamic learning experiences
2. **AI Copilots for Research & Tutoring** - 24/7 academic support systems
3. **Integrated Dashboards** - Combined academic and wellbeing data visualization
4. **Early-Risk Detection Models** - Proactive student retention strategies
5. **Holistic Student Profiles** - Unified data across academic, social, and emotional dimensions

### Key Findings

- **Existing LMS Limitations:** Current platforms (Canvas, Blackboard, etc.) are primarily administrative—handling assignments, grades, and scheduling—but lack deep personalization and behavioral insights

- **Holistic Data Importance:** Combining academic metrics (GPA, quiz performance, course progress) with wellbeing indicators (motivation, energy, stress, sleep) creates significantly more accurate representations of student experience

- **Early Intervention Value:** Research confirms that academic performance, wellbeing, and engagement are interdependent. Students benefit significantly from early warnings, personalized recommendations, and clear learning pathways

- **Market Demand:** Strong evidence supports demand for adaptive learning tools, mental health-aware systems, and AI-powered academic coaching

---

## 💡 Proposed Solution

ForgeEd is a unified, AI-enhanced Learning Management System designed to support students holistically across academics, wellbeing, and career development. The platform combines traditional LMS features with advanced GenAI capabilities to create a personalized, data-driven mentoring environment.

### Core Functional Modules

**1. AI-Powered Learning & Tutoring (SLU GPT)**
- 24/7 academic support and personalized explanations
- Study strategies and contextual guidance
- Based on enrolled courses and career goals
- Rich text formatting (headers, lists, code blocks)

**2. 90-Day Career Learning Roadmap**
- Structured, day-locked learning plan
- AI-produced content and theory explanations
- Curated external resources
- Automated daily proficiency checks

**3. Dual Quiz System**
- **Academic Quiz:** 15 questions from active courses
- **Career Learning Quiz:** 10 questions on current roadmap topic
- AI auto-scoring with personalized feedback
- Historical tracking and performance trends

**4. Wellbeing & Engagement Tracking**
- Daily wellbeing indicators via intuitive slider interface
- Metrics: Happiness, Stress, Energy, Motivation, Sleep Quality
- Early pattern detection for disengagement or academic risk
- AI-generated motivational insights

**5. Predictive Analytics & Performance Dashboard**
- Consolidated GPA, risk levels, quiz metrics, and course progress
- Interactive charts tracking performance trends
- Actionable insights for student improvement
- Personalized recommendations

**6. Admin Management Tools**
- Manage courses and generate roadmaps
- Monitor at-risk students
- Aggregated academic and wellbeing data visualization
- Program-level analytics

---

## 📋 Project Charter

**Project Name:** ForgeEd - AI-Enhanced Learning Management System

**Sponsor:** Saint Louis University

**Duration:** 12-Week Master's Research Project

**Budget:** Development Only (Academic Project)

**Objectives:**
- Design and implement a unified AI-enhanced LMS
- Integrate academic, wellbeing, and career development features
- Create predictive analytics for early intervention
- Validate system effectiveness with synthetic data
- Demonstrate GenAI application in higher education

**Success Criteria:**
- ✅ Functional prototype with all core features
- ✅ Database with synthetic student data
- ✅ Interactive dashboard with real-time analytics
- ✅ OpenAI API integration for personalized content
- ✅ Admin management capabilities
- ✅ Responsive UI across devices

**Deliverables:**
- Fully functional Flask-based application
- SQLite database with schema
- Sample data and documentation
- Technical implementation guide
- Research report and insights

---

## 🏗️ Architecture & Data Design

### Enterprise Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                       │
│  (HTML/CSS/JS Frontend - Dashboard, Quiz, Chat, Analytics)   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Flask Application Layer                          │
│  (Routes, Session Management, Business Logic)                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼──────────┐
│  Data Layer      │    │  AI Integration   │
│  (SQLite DB)     │    │  (OpenAI API)     │
│                  │    │                   │
│ • Students       │    │ • SLU GPT Chat    │
│ • Courses        │    │ • Content Gen     │
│ • Quizzes        │    │ • Scoring         │
│ • Wellbeing      │    │ • Insights        │
│ • Analytics      │    │ • Recommendations │
└──────────────────┘    └───────────────────┘
```

### Database Schema (ER Diagram)

```
STUDENTS
├─ student_id (PK)
├─ first_name
├─ last_name
├─ email (UNIQUE)
├─ password
├─ gpa
├─ completion_rate
├─ career_goal
├─ educational_background
├─ is_admin
└─ slu_gpt_sessions

COURSES
├─ course_id (PK)
├─ course_code
├─ course_name
├─ description
├─ credits
├─ faculty_name
└─ intake_term

ENROLLED_COURSES (Student ↔ Course)
├─ enrollment_id (PK)
├─ student_id (FK)
├─ course_id (FK)
├─ progress
├─ grade
├─ modules_completed
└─ pending_assignments

DAILY_ROADMAP (Student's Career Path)
├─ roadmap_id (PK)
├─ student_id (FK)
├─ day_number
├─ topic
├─ theory_content
├─ resources
├─ is_completed
└─ study_duration

CAREER_QUIZ_HISTORY
├─ quiz_id (PK)
├─ student_id (FK)
├─ date_taken
├─ score
├─ total_questions
├─ questions
├─ answers
└─ ai_feedback

ACADEMIC_QUIZ_HISTORY
├─ quiz_id (PK)
├─ student_id (FK)
├─ date_taken
├─ score
├─ total_questions
├─ course_id (FK)
├─ questions
├─ answers
└─ ai_feedback

WELLBEING_ASSESSMENTS
├─ assessment_id (PK)
├─ student_id (FK)
├─ date_assessed
├─ happiness (1-100)
├─ stress (1-100)
├─ energy (1-100)
├─ motivation (1-100)
├─ sleep_quality (1-100)
├─ total_score (1-100)
├─ feelings_description
├─ challenges_description
└─ ai_insights

SLU_GPT_CHAT_HISTORY
├─ chat_id (PK)
├─ student_id (FK)
├─ message
├─ response
└─ created_at
```

### Data Flow

1. **Student Login Flow**
   - Credentials validated against STUDENTS table
   - Session created with student context

2. **Dashboard Data Flow**
   - Aggregate queries across ENROLLED_COURSES, *_QUIZ_HISTORY, WELLBEING_ASSESSMENTS
   - Calculate risk scores, GPA trends, completion rates
   - Generate AI insights via OpenAI API
   - Render interactive charts with Chart.js

3. **Quiz Submission Flow**
   - Quiz answers submitted → Database storage
   - OpenAI API auto-scores → AI feedback generation
   - Results stored in *_QUIZ_HISTORY tables
   - Dashboard updated in real-time

4. **Career Roadmap Flow**
   - OpenAI API generates 90-day roadmap on student creation
   - Daily content retrieved from DAILY_ROADMAP
   - Completion marks unlock next day's content
   - Quiz results influence recommendations

5. **Wellbeing Tracking Flow**
   - Daily assessment submitted → WELLBEING_ASSESSMENTS storage
   - AI generates motivational insights
   - Risk indicators trigger admin alerts
   - Trends analyzed for early intervention

---

## 📈 Dashboard & Data Analysis

### Key Dashboard Features

**Performance Metrics Dashboard**
- Real-time GPA tracking
- Career Quiz performance (7-day trend)
- Academic Quiz performance (7-day trend)
- Wellbeing Score (7-day trend)
- Career readiness percentage
- Completion rate tracking

### Interactive Visualizations

The ForgeEd dashboard uses Chart.js to render:

1. **Combined Performance Graph** (Line Chart)
   - Tracks Career Quiz, Academic Quiz, and Wellbeing over 7 days
   - Color-coded by category (Purple, Blue, Orange)
   - Responsive and real-time updating

2. **GPA Progression** (Line Chart)
   - Historical GPA trends
   - Semester-over-semester comparison
   - Predictive trend analysis

3. **Current vs Predicted Performance** (Bar Chart)
   - Current GPA by subject area
   - Predicted GPA with current trajectory
   - Visual gap analysis for intervention

4. **Risk Level Distribution** (Status Indicator)
   - High/Medium/Low risk calculation
   - Based on recent quiz average scores
   - Real-time risk assessment

### Key Insights Generated by AI

ForgeEd's AI system analyzes dashboard data to produce:

**Academic Insights**
- Performance patterns and anomalies
- Course difficulty assessments
- Study recommendations based on quiz performance
- Early warning signs of academic struggle

**Career Development Insights**
- Career learning progress tracking
- Skill gap identification
- Course recommendations for career goals
- Industry-relevant competency assessments

**Wellbeing Insights**
- Mental health trend analysis
- Stress correlation with academic performance
- Motivational support based on engagement patterns
- Holistic wellness recommendations

**Predictive Analytics**
- End-of-semester GPA prediction
- Academic risk probability
- Intervention timing recommendations
- Personalized improvement strategies

---

## ⚖️ Ethical & Social Considerations

### Data Privacy & Security
- Student data protection aligned with FERPA regulations
- Secure API key management through environment variables
- Session-based authentication to prevent unauthorized access
- Transparent data usage policies

### AI Bias & Fairness
- Training data reviewed for demographic bias
- Recommendations tested across diverse student populations
- Continuous monitoring for discriminatory patterns
- Explainable AI outputs for student transparency

### Accessibility
- WCAG 2.1 compliance for accessibility standards
- Keyboard navigation throughout the platform
- Screen reader optimization
- Color-blind friendly design choices

### Responsible AI Use
- Clear labeling of AI-generated content
- Student consent for data analysis
- Transparent risk calculations
- Human oversight for sensitive interventions

### Stakeholder Considerations
- Faculty involvement in recommendation validation
- Student agency in setting learning goals
- Administrative oversight for data governance
- Continuous feedback loops for improvement

---

## 📚 Lessons Learned & Team Reflection

### Key Takeaways

**1. Complexity of Holistic Systems**
Building a system that truly integrates academic, emotional, and career dimensions is significantly more complex than standalone features. The interconnectedness requires careful data modeling, thoughtful UX design, and comprehensive testing.

**2. Value of User-Centric Design**
Early user research with actual SLU students validated our assumptions but also revealed unexpected needs. Iterative design based on real feedback was crucial to creating a system that resonates with users.

**3. AI Integration Challenges**
While OpenAI's API is powerful, prompt engineering and result validation are non-trivial. We learned the importance of:
- Testing multiple prompts
- Implementing guardrails against inappropriate outputs
- Fallback strategies for API failures
- Cost management through efficient API usage

**4. Data as a Critical Asset**
Quality synthetic data was essential for realistic prototyping. The process of generating realistic student profiles, quiz data, and wellbeing assessments helped us understand the domain deeply.

**5. Ethical Responsibility in EdTech**
Working with student data made ethical considerations paramount. We learned to build privacy-first, validate for bias, and maintain transparency with users about AI decision-making.

### Team Collaboration Insights
- Regular standups and async updates kept everyone aligned
- Clear documentation reduced dependencies between team members
- Code reviews strengthened technical quality
- Design-dev collaboration ensured feasibility of ideas

### Future Recommendations
1. **Expand to Mobile:** Develop native mobile apps for better accessibility
2. **Enhanced Analytics:** Implement more sophisticated ML models for prediction
3. **Peer Learning:** Add collaborative features for study groups
4. **Faculty Dashboard:** Create complementary tools for instructor insights
5. **Integration APIs:** Enable connections with other university systems
6. **Continuous Learning:** Implement feedback loops to improve AI model accuracy over time

---

## ✨ Core Features

### Academic Features
- **Student Dashboard**: Track GPA, completion rate, Career Quiz performance, Academic Quiz performance, and Wellbeing scores
- **Career Learning System**: 90-day personalized learning roadmap with day-locking mechanism, AI-generated theory content, and curated external resources
- **Dual Quiz System**: 
  - Career Learning Quiz (10 questions on daily roadmap topic)
  - Academic Quiz (15 questions from enrolled courses)
  - AI-powered auto-scoring with personalized feedback
- **Course Management**: Enrollment tracking, progress monitoring, and AI-powered course recommendations

### AI-Powered Features
- **Performance Analysis**: Personalized insights based on academic metrics
- **SLU GPT Chat Assistant**: Context-aware conversational AI with rich text formatting
- **Course Recommendations**: Based on career goals and educational background
- **90-Day Roadmap Generation**: Personalized learning paths
- **Theory Content Generation**: AI-produced content for each roadmap topic
- **Auto-Scoring**: Quiz auto-generation and scoring with personalized feedback
- **Wellbeing Insights**: AI-generated motivational support

### Wellbeing & Analytics
- **Wellbeing Tracking**: Daily mental health assessments with emoji sliders (happiness, stress, energy, motivation, sleep)
- **Performance Analytics**: Interactive Chart.js line graphs tracking Career Quiz, Academic Quiz, and Wellbeing scores
- **Predictive Risk Assessment**: Early detection of academic and emotional risk
- **Admin Monitoring**: Comprehensive admin interface for student performance tracking

### Admin Features
- **Manage Students**: Add/delete students with automatic roadmap generation
- **Manage Courses**: Add/delete courses from the catalog
- **Student Monitoring**: View comprehensive student performance metrics
- **Risk Alerts**: Identify at-risk students for intervention

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-Login, Flask-WTF
- **Database**: SQLite with comprehensive schema
- **AI/ML**: OpenAI GPT API for content generation and analysis
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Authentication**: Flask Sessions
- **Deployment**: Replit (Live at https://forgeed.replit.app/)

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (get from https://platform.openai.com)

### Quick Start

**1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/forgeed.git
cd forgeed
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- Flask-Login
- Flask-WTF
- OpenAI
- python-dotenv

**3. Set Up Environment Variables**

Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
SESSION_SECRET=your_secret_key_here
```

**4. Initialize Database**
```bash
python database.py
```

**5. Load Sample Data (Optional)**
```bash
python seed_sample_data.py
```

This creates:
- 10 diverse student profiles with varying performance levels
- Sample course catalog
- Historical quiz and wellbeing data

**6. Run the Application**
```bash
python app.py
```

Access the app at `http://localhost:5000`

---

## 🔐 Default Login Credentials

### Admin Access
- **Email**: `admin@edu`
- **Password**: `Password@123`

### Sample Student Accounts
After running `seed_sample_data.py`:
- **Emails**: `ullasgowda@slu.edu`, `alice.johnson@slu.edu`, `bob.smith@slu.edu`, etc.
- **Password**: `password123` (for all sample students)

---

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- **students**: User credentials, GPA, completion rates, career goals
- **courses**: Catalog of available courses
- **enrolled_courses**: Junction table linking students to courses
- **daily_roadmap**: 90-day personalized career learning topics
- **career_quiz_history**: Career Learning Quiz records
- **academic_quiz_history**: Academic Quiz records
- **wellbeing_assessments**: Daily wellbeing check-ins
- **slu_gpt_chat_history**: Chat conversation history

---

## 📁 Project Structure

```
forgeed/
├── app.py                      # Flask application with routes and AI logic
├── database.py                 # Database initialization script
├── analytics_service.py        # Performance analytics and risk calculation
├── generate_roadmap.py         # AI-powered 90-day roadmap generator
├── seed_sample_data.py         # Sample data generator
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── forgeed.db                  # SQLite database
├── static/
│   └── style.css              # ForgeEd UI styling
├── templates/
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── courses.html           # Course management
│   ├── career_learning.html   # 90-day roadmap
│   ├── quiz.html              # Dual quiz system
│   ├── wellbeing.html         # Wellbeing assessment
│   ├── analytics.html         # Performance analytics
│   ├── slu_gpt.html          # AI chat interface
│   └── admin.html             # Admin dashboard
└── README.md                  # This file
```

---

## 🔌 API Endpoints

### Student Endpoints
- `GET /dashboard` - Main dashboard
- `GET /courses` - Course management
- `GET /career-learning` - 90-day roadmap
- `GET /quiz` - Dual quiz system
- `GET /wellbeing` - Daily wellbeing assessment
- `GET /analytics` - Performance analytics
- `GET /slu-gpt` - AI chat interface

### API Routes
- `POST /api/submit-career-quiz` - Submit Career Quiz
- `POST /api/submit-academic-quiz` - Submit Academic Quiz
- `POST /api/submit-wellbeing` - Submit wellbeing assessment
- `POST /api/chat` - SLU GPT chat
- `GET /api/get-day-content/<day>` - Get roadmap day content
- `POST /api/complete-day` - Mark roadmap day as complete
- `GET /api/dashboard-graph-data` - Dashboard graph data
- `GET /api/analytics-data` - Student analytics data
- `GET /api/enrolled-courses` - Get student's enrolled courses

### Admin Endpoints
- `GET /admin` - Admin dashboard
- `POST /api/admin/add-student` - Add new student
- `POST /api/admin/delete-student` - Delete student
- `POST /api/admin/add-course` - Add new course
- `POST /api/admin/delete-course` - Delete course

---

## ⚙️ Customization

### Modify AI Prompts
Edit prompts in `app.py`:
- SLU GPT context: `/api/chat` route
- Dashboard insights: `generate_ai_insights()` function
- Course recommendations: `get_ai_course_recommendations()` function

### Change UI Colors
Edit CSS variables in `static/style.css`:
- `--color-academic`: Academic metrics color (#2196F3)
- `--color-career`: Career metrics color (#9b7fd7)
- `--color-wellbeing`: Wellbeing metrics color (#f4a261)

### Add New Features
1. Create new route in `app.py`
2. Create new template in `templates/`
3. Add navigation link in sidebar
4. Update database schema if needed

---

## 🚀 Deployment

ForgeEd is currently deployed on Replit and accessible at:
**https://forgeed.replit.app/**

### Deployment Steps

1. **Push to Replit:** Connect GitHub repository to Replit
2. **Set Environment Variables:** Add `OPENAI_API_KEY` in Replit Secrets
3. **Initialize Database:** Run `python database.py`
4. **Load Sample Data:** Run `python seed_sample_data.py`
5. **Start Server:** Flask app auto-starts on Replit

---

## 🔒 Security Notes

**⚠️ Important for Production:**
- Current implementation stores passwords in plain text (development only)
- For production: Implement password hashing (bcrypt/argon2)
- Use strong SESSION_SECRET in production
- Secure OpenAI API key using environment variables
- Implement HTTPS/SSL
- Add rate limiting for API endpoints
- Implement CSRF protection
- Regular security audits

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database not found | Run `python database.py` first |
| No courses showing | Run `python seed_sample_data.py` to load sample data |
| AI not responding | Verify OPENAI_API_KEY is set correctly in `.env` |
| Login fails | Check that student data exists in database |
| External links not showing | Resources fallback to default links (MDN, W3Schools) |

---

## 📊 Risk Level Calculation

Student risk levels are calculated based on quiz performance:
- **High Risk**: Average quiz score < 50%
- **Medium Risk**: Average quiz score 50-79%
- **Low Risk**: Average quiz score ≥ 80%

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📞 Appendix

### Additional Resources

**Project Documentation:**
- Research Report: Full MRP documentation available upon request
- Architecture Diagrams: See Architecture & Data Design section
- API Documentation: See API Endpoints section
- Database Schema: See Database Schema section

**External Resources:**
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

**Related Research:**
- Ifenthaler, D., & Yau, J. M. K. (2020). Utilising learning analytics to support study success. *Journal of Learning Analytics*, 7(3), 1-4.
- Artificial Intelligence in Education: A Review (2020)

**Contact:**
- **Institution:** Saint Louis University
- **Program:** MS in Information Systems
- **Project Website:** https://forgeed.replit.app/

---

### Version History

**v1.0.0** - Initial Release
- Complete LMS functionality with AI integration
- Dual quiz system
- 90-day career roadmap
- Wellbeing tracking
- Performance analytics
- Admin dashboard

---

**Built with ❤️ by MRP Team 1 @ Saint Louis University**

**Last Updated:** November 2025

For questions or issues, please reach out through the GitHub repository or Saint Louis University's MS in Information Systems program.
