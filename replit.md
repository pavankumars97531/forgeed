# ForgeEd - AI-Enhanced Learning Management System

## Overview

ForgeEd is an AI-powered Learning Management System (LMS) designed for Saint Louis University's MS in Information Systems students. The application combines traditional LMS features (course management, progress tracking, grading) with AI-enhanced capabilities powered by OpenAI's GPT models. Key features include personalized learning recommendations, AI-generated daily quizzes, context-aware chat assistance (SLU GPT), and performance analytics.

The system serves as a student portal where learners can track their academic progress, interact with AI tutors, receive course recommendations aligned with career goals, and complete auto-graded assessments.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask-based MVC Architecture**: The application uses Flask as a lightweight Python web framework following the Model-View-Controller pattern. Routes are defined in `app.py`, data persistence is handled through `database.py`, and HTML templates reside in the `templates/` directory.
- **Session-based Authentication**: User authentication relies on Flask sessions with a secret key. Login credentials are validated against the database, and session data stores the student ID and name for subsequent requests.
- **Server-side Rendering**: All pages are rendered server-side using Jinja2 templates, with dynamic data injected from the database and AI services.

### Data Layer
- **SQLite Database**: The application uses SQLite as its relational database (`forgeed.db`), suitable for single-user or development scenarios. The schema includes three main tables:
  - `students`: Stores user credentials, GPA, completion rates, career goals, and SLU GPT session counts
  - `courses`: Catalog of available courses with descriptions, instructors, and semester information
  - `enrolled_courses`: Junction table linking students to courses with progress tracking, grades, and assignment status
- **Row Factory Pattern**: Database connections use `sqlite3.Row` factory for dictionary-like access to query results, simplifying data handling in templates and route handlers.

### AI Integration
- **OpenAI GPT Integration**: The system integrates OpenAI's API (via the official Python SDK) to power multiple AI features:
  - **Performance Analysis**: Generates personalized insights based on student GPA, completion rates, and course performance
  - **SLU GPT Chat**: Context-aware conversational AI that understands the student's enrolled courses and career goals
  - **Course Recommendations**: Analyzes career goals and current courses to suggest relevant next-semester courses
  - **Quiz Generation**: Auto-generates 10-question quizzes tailored to enrolled courses and career objectives
  - **Auto-Scoring**: AI evaluates quiz responses and provides detailed feedback
- **API Key Management**: OpenAI API key is loaded from environment variables using `python-dotenv`, with graceful degradation if the key is missing.

### Frontend Architecture
- **Multi-page Application**: Traditional multi-page design with separate HTML templates for login, dashboard, courses, quiz, and SLU GPT chat interfaces.
- **Component-based CSS**: Custom CSS in `static/style.css` provides consistent styling across the application with a sidebar navigation pattern and card-based layouts.
- **JavaScript for Interactivity**: Client-side JavaScript handles dynamic features like quiz submission, chat interactions, and real-time UI updates without page reloads.

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