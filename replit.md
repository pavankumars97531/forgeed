# ForgeEd - AI-Enhanced Learning Management System

## Overview

ForgeEd is an AI-powered Learning Management System (LMS) designed for Saint Louis University's MS in Information Systems students. The application combines traditional LMS features (course management, progress tracking, grading) with AI-enhanced capabilities powered by OpenAI's GPT models.

**Core Features:**
- **Career Learning System**: 90-day personalized learning roadmap with day-locking mechanism, AI-generated theory content, and curated external resources
- **Dual Quiz System**: Career Learning Quiz (10 questions on daily topic) + Academic Quiz (15 questions from enrolled courses) with AI feedback
- **Wellbeing Tracking**: Daily mental health assessments with emoji sliders (1-100 scoring) and AI-generated motivational insights
- **Performance Analytics**: Three interactive Chart.js line graphs tracking Career Quiz, Academic Quiz, and Wellbeing scores over time
- **SLU GPT Chat Assistant**: Context-aware conversational AI with rich text formatting (headers, bold, lists, code blocks) that understands enrolled courses and career goals
- **Course Management**: Enrollment tracking, progress monitoring, and AI-powered course recommendations based on actual university courses
- **Admin Dashboard**: Comprehensive administrative interface for managing students, courses, and monitoring student performance

The system serves as a comprehensive student portal integrating academic learning, career development, and personal wellbeing support, with a powerful admin interface for institutional management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask-based MVC Architecture**: The application uses Flask as a lightweight Python web framework following the Model-View-Controller pattern. Routes are defined in `app.py`, data persistence is handled through `database.py`, and HTML templates reside in the `templates/` directory.
- **Dual-Role Authentication**: User authentication relies on Flask sessions with a secret key. Login credentials are validated against the database, and the system automatically redirects to either the student dashboard or admin dashboard based on the `is_admin` flag. Session data stores the user ID, name, and admin status for authorization throughout the application.
- **Server-side Rendering**: All pages are rendered server-side using Jinja2 templates, with dynamic data injected from the database and AI services.

### Data Layer
- **SQLite Database**: The application uses SQLite as its relational database (`forgeed.db`), suitable for single-user or development scenarios. The schema includes seven main tables:
  - `students`: Stores user credentials, GPA, completion rates, career goals, educational background, admin status (`is_admin`), SLU GPT session counts, and account creation timestamps
  - `courses`: Catalog of available courses with course codes, names, descriptions, faculty names, intake terms, and semester information
  - `enrolled_courses`: Junction table linking students to courses with progress tracking, grades, and assignment status
  - `daily_roadmap`: 90-day personalized career learning topics with theory content, resources, completion tracking, and study duration
  - `career_quiz_history`: Records of Career Learning Quiz attempts with scores, answers, and AI feedback
  - `academic_quiz_history`: Records of Academic Quiz attempts with scores, answers, and AI feedback
  - `wellbeing_assessments`: Daily wellbeing check-ins with happiness/stress/energy scores, journal entries, and AI insights
- **Row Factory Pattern**: Database connections use `sqlite3.Row` factory for dictionary-like access to query results, simplifying data handling in templates and route handlers.
- **Day-Locking Security**: Server-side validation enforces sequential progression through the 90-day roadmap based on account creation date, preventing unauthorized access to future content.
- **Admin Authorization**: All admin routes enforce server-side authorization checks to ensure only users with `is_admin=1` can access administrative functions.

### AI Integration
- **OpenAI GPT Integration**: The system integrates OpenAI's API (via the official Python SDK) to power multiple AI features:
  - **Performance Analysis**: Generates personalized insights based on student GPA, completion rates, and course performance
  - **SLU GPT Chat**: Context-aware conversational AI that understands the student's enrolled courses and career goals
  - **Course Recommendations**: Analyzes career goals, educational background, and actual university courses (from database) to suggest relevant next-semester courses with faculty and intake term considerations
  - **90-Day Roadmap Generation**: Creates personalized career learning paths with daily topics tailored to career goals
  - **Theory Content Generation**: Dynamically generates detailed learning content for each roadmap topic
  - **Career Quiz Generation**: Auto-generates 10 questions based on the current day's roadmap topic
  - **Academic Quiz Generation**: Creates 15 questions (5 from each of 3 enrolled courses) for comprehensive assessment
  - **Quiz Auto-Scoring**: AI evaluates responses and provides personalized feedback on incorrect answers
  - **Wellbeing Insights**: Analyzes daily mental health assessments and generates supportive, motivational feedback
- **API Key Management**: OpenAI API key is loaded from environment variables using `python-dotenv`, with graceful degradation if the key is missing.

### Frontend Architecture
- **Multi-page Application**: Traditional multi-page design with separate HTML templates for login, dashboard, courses, quiz, career learning, wellbeing, SLU GPT chat, student analytics, and admin dashboard interfaces.
- **Component-based CSS**: Custom CSS in `static/style.css` provides consistent styling across the application with a sidebar navigation pattern and card-based layouts.
- **JavaScript for Interactivity**: Client-side JavaScript handles dynamic features like quiz submission, chat interactions with markdown-style formatting, day-locking UI, wellbeing sliders, admin CRUD operations, and real-time UI updates without page reloads.
- **Chart.js Integration**: Line graphs on the dashboard and analytics pages use Chart.js (loaded via CDN) to visualize performance metrics including Career Quiz scores, Academic Quiz scores, Wellbeing scores, GPA progression, and predictive performance charts.
- **Rich Text Formatting**: SLU GPT chat responses support markdown-style formatting including **bold text**, ### headers, bullet lists, numbered lists, inline code (`code`), and code blocks (```) with dark theme syntax highlighting.
- **Color-Coordinated Design System**: Dashboard uses a unified color theme managed via CSS variables to ensure visual consistency across all tracking categories:
  - **Academic/GPA** (Blue #2196F3): Stat cards, Academic Quiz graph line, and academic insights
  - **Career** (Purple #9b7fd7): Stat cards, Career Quiz graph line, and career insights
  - **Wellbeing** (Orange #f4a261): Stat cards, Wellbeing graph line, and wellbeing insights
  - Theme colors defined as CSS variables (`--color-academic`, `--color-career`, `--color-wellbeing`) with light variants for backgrounds
  - AI-generated insights are categorized by topic (academic/career/wellbeing) and rendered with matching color coding

### Admin Dashboard
- **Three-Section Interface**: Admin dashboard provides comprehensive institutional management through three dedicated sections:
  - **Manage Students**: Add new students with name, email, password, educational background, and career goals. The system automatically generates a personalized 90-day career roadmap for each new student. Delete students with cascade cleanup.
  - **Manage Courses**: Add courses with course code, name, faculty name, intake term, credits, semester, and description. Delete courses from the catalog. All course data is used by the AI recommendation engine.
  - **Students Info Table**: View comprehensive student performance metrics including GPA, average wellbeing scores, risk levels (Low/Medium/High based on GPA thresholds), educational background, and career goals in a sortable data table.
- **Atomic Transaction Handling**: Student creation commits the database record before generating the roadmap, ensuring the roadmap generator can see the new student. If roadmap generation fails, the system automatically deletes the orphaned student record to maintain data consistency.
- **Authorization Enforcement**: All admin routes (`/admin/dashboard`, `/api/admin/*`) enforce server-side session and `is_admin` flag checks, preventing unauthorized access to administrative functions.
- **Dynamic Data Integration**: Course recommendations and student insights dynamically pull from the actual courses table, ensuring AI recommendations reflect real university offerings with faculty expertise and intake schedules.

### Security Considerations
- **Plain-text Password Storage**: The current implementation stores passwords in plain text in the database. This is a development-stage decision that should be replaced with hashed passwords (bcrypt/argon2) for production.
- **Session Management**: Sessions are secured with a secret key that defaults to a development value but should be set via environment variable in production.

### Data Initialization
- **Database Schema Setup**: `database.py` includes an `init_db()` function that creates tables if they don't exist, allowing for easy database initialization.
- **Sample Data Scripts**: `insert_sample_data.py` provides example data insertion for testing, including a sample student, course catalog, and enrollment records.

## External Dependencies

### Third-party Libraries
- **Flask** (v2.x+): Python web framework for routing, templating, and session management
- **OpenAI Python SDK** (v1.x+): Official OpenAI library for GPT API integration
- **python-dotenv**: Environment variable management for API keys and configuration

### AI Services
- **OpenAI GPT API**: Core AI functionality provider for chat completions, text analysis, and content generation. Requires an active API key and handles:
  - Student performance analysis
  - Conversational AI (SLU GPT)
  - Course recommendation engine
  - Quiz generation and auto-grading

### Database
- **SQLite3**: Built-in Python database engine (no external installation required). While suitable for development and single-user scenarios, production deployments may benefit from migration to PostgreSQL or MySQL for multi-user concurrent access.

### Frontend Resources
- **System Fonts**: Uses native operating system fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto) for optimal rendering without external font dependencies
- **Emoji Icons**: Navigation and UI icons use Unicode emoji characters, eliminating the need for icon libraries

### Environment Configuration
- **OPENAI_API_KEY**: Required environment variable for AI features
- **SESSION_SECRET**: Optional environment variable for Flask session encryption (defaults to development key)