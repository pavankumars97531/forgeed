# ForgeEd - User Interaction Guide

## Complete System Walkthrough with Visual References

---

## Table of Contents
1. [Login & Authentication](#1-login--authentication)
2. [Student Dashboard](#2-student-dashboard)
3. [Career Learning Roadmap](#3-career-learning-roadmap)
4. [Dual Quiz System](#4-dual-quiz-system)
5. [Wellbeing Assessment](#5-wellbeing-assessment)
6. [Performance Analytics](#6-performance-analytics)
7. [SLU GPT Chat Assistant](#7-slu-gpt-chat-assistant)
8. [Course Management](#8-course-management)
9. [Admin Dashboard](#9-admin-dashboard)

---

## 1. Login & Authentication

### **Screenshot: Login Page**
![Login Page Screenshot - See browser for actual view]

### **Key Features:**
1. **University Email Field** - Enter your SLU email address
2. **Password Field** - Enter your password
3. **Remember Me Checkbox** - Stay logged in across sessions
4. **Sign In Button** - Click to access the system
5. **Forgot Password Link** - Recover account access

### **User Interaction:**
```
Step 1: Navigate to the ForgeEd login page
Step 2: Enter university email (e.g., student@slu.edu)
Step 3: Enter password
Step 4: (Optional) Check "Remember me" to stay logged in
Step 5: Click the "Sign In →" button
Step 6: System redirects to appropriate dashboard based on role:
        - Students → Student Dashboard
        - Admins → Admin Dashboard
```

### **Sample Credentials:**
- **Student**: ullasgowda@slu.edu / password123
- **Admin**: admin@edu / Password@123

---

## 2. Student Dashboard

### **Key Features Visible:**

#### **📊 Top Statistics Cards (4 cards)**
1. **GPA Card** (Blue)
   - Displays current GPA
   - Color: Academic Blue (#2196F3)

2. **Course Completion Card** (Blue)
   - Shows overall completion percentage
   - Based on enrolled course progress

3. **Career Quiz Performance Card** (Purple)
   - Average score from Career Learning Quizzes
   - Color: Career Purple (#9b7fd7)

4. **Wellbeing Score Card** (Orange)
   - Latest wellbeing assessment total
   - Color: Wellbeing Orange (#f4a261)

#### **📈 Performance Tracking Graphs (3 graphs)**
1. **Career Quiz Performance Graph** (Purple line)
   - Shows last 30 days of Career Quiz scores
   - X-axis: Date
   - Y-axis: Score percentage

2. **Academic Quiz Performance Graph** (Blue line)
   - Shows last 30 days of Academic Quiz scores
   - X-axis: Date
   - Y-axis: Score percentage

3. **Wellbeing Trend Graph** (Orange line)
   - Shows last 30 days of wellbeing scores
   - X-axis: Date
   - Y-axis: Wellbeing score (0-100)

#### **🤖 AI-Generated Insights Section**
- 3 personalized insights based on performance
- Color-coded by category:
  - **Academic insights** (Blue background)
  - **Career insights** (Purple background)
  - **Wellbeing insights** (Orange background)

### **User Interaction:**
```
Step 1: After login, dashboard loads automatically
Step 2: View at-a-glance statistics in top cards
Step 3: Scroll down to see performance graphs
Step 4: Hover over graph points to see exact scores
Step 5: Read AI-generated insights for personalized feedback
Step 6: Use sidebar navigation to access other features
```

### **Sidebar Navigation:**
- 🏠 Dashboard (current page)
- 📚 My Courses
- 🎯 Career Learning
- ✍️ Quizzes
- 💚 Wellbeing
- 📊 Student Analytics
- 🤖 SLU GPT
- 🚪 Logout

---

## 3. Career Learning Roadmap

### **Key Features:**

#### **📅 Progress Overview (Top Section)**
1. **Current Day Card**
   - Shows your current day in the 90-day roadmap
   - Example: "Day 15 of 90 days"

2. **Completed Days Card**
   - Total number of completed learning topics
   - Updates in real-time

3. **Progress Percentage Card**
   - Overall completion percentage
   - Calculated: (Current Day / 90) × 100

#### **📋 Roadmap Timeline (Left Panel)**
- **Past Days** (Green checkmark)
  - Completed topics
  - Accessible for review
  - Example: "Day 1: Introduction to Machine Learning ✓"

- **Current Day** (Highlighted)
  - Today's learning topic
  - Marked with "📍 Today"
  - Can view content and take quiz

- **Future Days** (Locked)
  - Upcoming topics
  - Marked with "🔒 Locked"
  - Day-locking prevents access until current day

#### **📖 Day Content Panel (Right Section)**
When you click on a day, it displays:

1. **Topic Title**
   - Example: "Day 15: Cloud Computing Fundamentals"

2. **Study Duration**
   - Recommended study time
   - Example: "⏱️ Study Time: 60 minutes"

3. **Theory & Learning Content Section**
   - AI-generated comprehensive learning material
   - Formatted with headers, lists, and paragraphs
   - Covers key concepts, examples, and best practices

4. **External Resources Section**
   - Curated learning links
   - Default resources:
     - 📚 MDN Web Docs
     - 📚 W3Schools
     - 📚 FreeCodeCamp
   - Click to open in new tab

5. **Mark as Complete Button** (Current day only)
   - Appears only for today's topic
   - Allows manual completion
   - Note: Automatically completes when you submit Career Quiz

### **User Interaction:**
```
Step 1: Click "🎯 Career Learning" in sidebar
Step 2: View your current day and progress overview
Step 3: Click on any unlocked day card to view content
Step 4: Read AI-generated theory content
Step 5: Click external resource links for supplementary learning
Step 6: Option A: Click "Mark as Complete" to manually complete
        Option B: Go to Quizzes → Take Career Quiz (auto-completes day)
Step 7: Next day unlocks after completion
```

### **Day-Locking System:**
```
✅ Available Days:
   - All past days (for review)
   - Current day (for learning)

🔒 Locked Days:
   - All future days
   - Click shows alert: "🔒 This day is locked. Complete previous days to unlock."
```

---

## 4. Dual Quiz System

### **Key Features:**

#### **📝 Two Quiz Types**

**A. Career Learning Quiz (Left Card)**
- **Purpose**: Test knowledge of current day's roadmap topic
- **Questions**: 10 AI-generated questions
- **Topic**: Based on current day's learning content
- **Button**: "Start Career Quiz" (Purple)
- **Auto-completion**: Submitting this quiz automatically marks roadmap day as complete

**B. Academic Quiz (Right Card)**
- **Purpose**: Test knowledge across enrolled courses
- **Questions**: 15 questions (5 from each of 3 courses)
- **Coverage**: Comprehensive assessment of course materials
- **Button**: "Start Academic Quiz" (Blue)

#### **Quiz Interface (After clicking Start)**

1. **Question Display**
   - Question number and text
   - Example: "Question 1 of 10: What is machine learning?"

2. **Multiple Choice Options**
   - 4 radio button options (A, B, C, D)
   - Single selection per question

3. **Navigation**
   - "Next Question" button
   - Progress indicator (e.g., "Question 3/10")

4. **Submit Section**
   - Appears on last question
   - "Submit Quiz" button
   - Confirmation dialog before submission

#### **Results & Feedback**

After submission, displays:
1. **Score Summary**
   - Your score: X/10 or X/15
   - Percentage: XX%

2. **AI-Powered Feedback**
   - Personalized analysis of performance
   - Suggestions for improvement
   - Encouragement and next steps

3. **Question Review**
   - See all questions
   - Your answers vs correct answers
   - Explanations for incorrect answers

### **User Interaction:**

**Taking Career Quiz:**
```
Step 1: Click "✍️ Quizzes" in sidebar
Step 2: Click "Start Career Quiz" button (purple card)
Step 3: System generates 10 questions on current day's topic
Step 4: Read question and select your answer
Step 5: Click "Next Question" to proceed
Step 6: Repeat for all 10 questions
Step 7: Click "Submit Quiz" on final question
Step 8: Confirm submission in dialog
Step 9: View your score and AI feedback
Step 10: Automatic: Current roadmap day marks as complete ✅
```

**Taking Academic Quiz:**
```
Step 1: Click "✍️ Quizzes" in sidebar
Step 2: Click "Start Academic Quiz" button (blue card)
Step 3: System generates 15 questions (5 per enrolled course)
Step 4: Answer all questions across your courses
Step 5: Submit quiz
Step 6: View comprehensive feedback and score
```

---

## 5. Wellbeing Assessment

### **Key Features:**

#### **😊 Daily Check-in Section**

**Five Emoji Sliders (Interactive):**

1. **😊 Happiness Slider**
   - Scale: 1-100
   - Drag emoji to rate happiness level
   - Left (1) = Very Unhappy
   - Right (100) = Very Happy

2. **😰 Stress Level Slider**
   - Scale: 1-100
   - Drag emoji to rate stress
   - Left (1) = No Stress
   - Right (100) = Extremely Stressed
   - Note: Lower is better (inverted scoring)

3. **⚡ Energy Level Slider**
   - Scale: 1-100
   - Drag emoji to rate energy
   - Left (1) = Exhausted
   - Right (100) = Fully Energized

4. **🎯 Motivation Slider**
   - Scale: 1-100
   - Drag emoji to rate motivation
   - Left (1) = No Motivation
   - Right (100) = Highly Motivated

5. **😴 Sleep Quality Slider**
   - Scale: 1-100
   - Drag emoji to rate sleep quality
   - Left (1) = Terrible Sleep
   - Right (100) = Excellent Sleep

#### **📝 Optional Journal Section**
- Text area for daily reflections
- Free-form journaling
- Captures mood and thoughts

#### **💡 AI Insights Display**
After submission:
- Personalized wellbeing analysis
- AI-generated motivational feedback
- Suggestions for improvement
- Trend analysis

### **User Interaction:**
```
Step 1: Click "💚 Wellbeing" in sidebar
Step 2: Drag each emoji slider to reflect your current state
        - Happiness: How happy are you today?
        - Stress: How stressed do you feel?
        - Energy: What's your energy level?
        - Motivation: How motivated are you?
        - Sleep: How well did you sleep?
Step 3: (Optional) Write journal entry about your day
Step 4: Click "Submit Wellbeing Assessment" button
Step 5: View AI-generated insights and encouragement
Step 6: See your total wellbeing score (calculated from all metrics)
```

### **Scoring System:**
```
Total Score = (Happiness + (100 - Stress) + Energy + Motivation + Sleep) / 5

Example:
Happiness: 80
Stress: 30 → Inverted: (100 - 30) = 70
Energy: 75
Motivation: 85
Sleep: 80

Total = (80 + 70 + 75 + 85 + 80) / 5 = 78/100
```

---

## 6. Performance Analytics

### **Key Features:**

#### **📈 Three Interactive Graphs**

**1. Career Quiz Performance (Purple)**
- Line chart showing daily Career Quiz scores
- X-axis: Date
- Y-axis: Score (0-10)
- Tooltip on hover: Date, Score, Percentage

**2. Academic Quiz Performance (Blue)**
- Line chart showing Academic Quiz scores over time
- X-axis: Date
- Y-axis: Score (0-15)
- Tooltip: Course breakdown, total score

**3. Wellbeing Trends (Orange)**
- Line chart showing daily wellbeing total scores
- X-axis: Date
- Y-axis: Wellbeing score (0-100)
- Shows overall mental health trends

#### **📊 Performance Summary Cards**

1. **Average Career Score**
   - Mean score across all Career Quizzes
   - Color: Purple

2. **Average Academic Score**
   - Mean score across all Academic Quizzes
   - Color: Blue

3. **Average Wellbeing**
   - Mean wellbeing score over time
   - Color: Orange

4. **Risk Level Indicator**
   - Based on quiz performance
   - **Low Risk** (Green): Score ≥ 80%
   - **Medium Risk** (Yellow): Score 50-79%
   - **High Risk** (Red): Score < 50%

### **User Interaction:**
```
Step 1: Click "📊 Student Analytics" in sidebar
Step 2: View all three performance graphs
Step 3: Hover over any point on graphs to see detailed scores
Step 4: Observe trends over time (improving, declining, stable)
Step 5: Check summary cards for overall averages
Step 6: Review risk level based on performance
```

### **Insights from Analytics:**
- **Upward trends**: Improvement in performance
- **Downward trends**: May need additional support
- **Correlation**: Compare quiz scores with wellbeing trends
- **Risk assessment**: Early warning system for struggling students

---

## 7. SLU GPT Chat Assistant

### **Key Features:**

#### **💬 Chat Interface**

**Conversation Area:**
- **User messages** (Right side, blue background)
- **AI responses** (Left side, gray background)
- Scrollable chat history
- Rich text formatting support

**Input Section:**
- Large text area for typing messages
- Character counter
- "Send Message" button

#### **🎨 Rich Text Formatting**

AI responses support:
- **Bold text**: `**important**` renders as **important**
- **Headers**: `### Heading` renders as large heading
- **Bullet lists**: 
  ```
  - Item 1
  - Item 2
  ```
- **Numbered lists**:
  ```
  1. First step
  2. Second step
  ```
- **Inline code**: `` `code` `` renders with dark background
- **Code blocks**:
  ````
  ```python
  def hello():
      print("Hello")
  ```
  ````

#### **🧠 Context Awareness**

SLU GPT knows:
- Your enrolled courses
- Your career goals
- Saint Louis University information
- MS in Information Systems program details

### **User Interaction:**
```
Step 1: Click "🤖 SLU GPT" in sidebar
Step 2: Type your question or request in the text area
        Examples:
        - "Explain machine learning concepts"
        - "Help me with database normalization"
        - "What courses should I take for data science?"
        - "Tips for improving my GPA"
Step 3: Click "Send Message" button
Step 4: Wait for AI response (appears in chat)
Step 5: Read formatted response with headers, code, lists
Step 6: Continue conversation by asking follow-ups
Step 7: All conversation history is saved
```

### **Example Conversations:**

**Student**: "How can I prepare for a software engineering role?"

**SLU GPT Response** (with formatting):
```
### Preparing for Software Engineering

Based on your goal to become a **Software Engineer**, here's a roadmap:

**Core Skills to Develop:**
- Data structures and algorithms
- Object-oriented programming
- System design fundamentals
- Version control (Git)

**Recommended SLU Courses:**
1. Advanced Programming Concepts
2. Database Management Systems
3. Software Engineering Principles

**Practice Resources:**
- LeetCode for coding practice
- GitHub for portfolio projects
- Open source contributions

Good luck with your preparation! 🚀
```

---

## 8. Course Management

### **Key Features:**

#### **📚 Enrolled Courses Section**

**Course Cards Display:**
Each enrolled course shows:
1. **Course Code** (e.g., IS 6100)
2. **Course Name** (e.g., Database Management)
3. **Faculty Name** (e.g., Dr. Smith)
4. **Progress Bar**
   - Visual indicator of completion %
   - Color-coded: Green when complete
5. **Current Grade** (e.g., A, B+, A-)
6. **Credits** (e.g., 3 credits)

#### **🎓 AI Course Recommendations**

**Recommendation Cards:**
Shows 3 AI-suggested courses:
1. **Course Code & Name**
2. **Faculty Teaching**
3. **Intake Term** (e.g., Spring 2025)
4. **Relevance Explanation**
   - Why this course fits your career goal
   - How it builds on your background

**Refresh Button:**
- "Get New Recommendations"
- Regenerates suggestions using AI

### **User Interaction:**
```
Step 1: Click "📚 My Courses" in sidebar
Step 2: View all your enrolled courses with progress
Step 3: Check grades and completion percentages
Step 4: Scroll to "AI Course Recommendations" section
Step 5: Read personalized course suggestions
Step 6: Review relevance explanations
Step 7: Click "Get New Recommendations" for fresh suggestions
Step 8: Use recommendations for course planning
```

---

## 9. Admin Dashboard

### **Key Features:**

#### **👥 Three Management Sections**

**A. Manage Students Section**

**Add New Student Form:**
1. **Name Field** - Student's full name
2. **Email Field** - University email
3. **Password Field** - Initial password
4. **Educational Background** - Prior education
5. **Career Goal** - Student's career aspiration
6. **"Add Student" Button** (Green)

**What Happens:**
- Creates new student account
- Automatically generates 90-day personalized roadmap
- Student can log in immediately

**Student List:**
- Table showing all students
- Columns: Name, Email, Career Goal
- **Delete Button** (Red) for each student
- Confirmation before deletion

**B. Manage Courses Section**

**Add New Course Form:**
1. **Course Code** - e.g., IS 7500
2. **Course Name** - Full course title
3. **Faculty Name** - Instructor
4. **Intake Term** - When offered (e.g., Fall 2025)
5. **Credits** - Credit hours
6. **Semester** - Which semester
7. **Description** - Course overview
8. **"Add Course" Button** (Green)

**Course List:**
- Table of all available courses
- Columns: Code, Name, Faculty, Term
- **Delete Button** (Red) for removal

**C. Students Info Table**

**Comprehensive Monitoring:**
- All students in sortable table
- Columns:
  1. **Name** - Student name
  2. **Email** - Contact
  3. **GPA** - Current grade point average
  4. **Avg Wellbeing** - Average wellbeing score
  5. **Risk Level** - Color-coded risk assessment
     - 🟢 **Low** (Green): Score ≥ 80%
     - 🟡 **Medium** (Yellow): Score 50-79%
     - 🔴 **High** (Red): Score < 50%
  6. **Educational Background**
  7. **Career Goal**

**Sorting:**
- Click column headers to sort
- Identify at-risk students quickly

### **User Interaction:**

**Adding a Student:**
```
Step 1: Login as admin (admin@edu / Password@123)
Step 2: View admin dashboard (auto-redirects)
Step 3: Locate "Manage Students" section
Step 4: Fill in student details:
        - Name: John Doe
        - Email: john.doe@slu.edu
        - Password: password123
        - Education: Bachelor in Computer Science
        - Career Goal: Data Scientist
Step 5: Click "Add Student" button
Step 6: System creates account + generates 90-day roadmap
Step 7: Success message appears
Step 8: Student appears in list below
```

**Deleting a Student:**
```
Step 1: Find student in "Manage Students" list
Step 2: Click red "Delete" button next to student
Step 3: Confirm deletion in popup dialog
Step 4: Student removed from system (cascade delete)
Step 5: All student data (quizzes, roadmap, etc.) removed
```

**Adding a Course:**
```
Step 1: Scroll to "Manage Courses" section
Step 2: Fill in course details:
        - Code: IS 7500
        - Name: Advanced Machine Learning
        - Faculty: Dr. Jane Smith
        - Intake: Spring 2026
        - Credits: 3
        - Semester: 2
        - Description: Deep dive into ML algorithms
Step 3: Click "Add Course" button
Step 4: Course added to catalog
Step 5: Available for AI recommendations
```

**Monitoring Students:**
```
Step 1: Scroll to "Students Info" table
Step 2: View all student performance metrics
Step 3: Click column headers to sort:
        - Sort by GPA to see struggling students
        - Sort by Risk Level to prioritize interventions
        - Sort by Wellbeing to check mental health
Step 4: Identify high-risk students (red indicators)
Step 5: Use insights for academic support planning
```

---

## System Workflow Summary

### **Daily Student Workflow:**

```
Morning:
1. Log in to ForgeEd
2. Check dashboard for AI insights
3. Review today's roadmap topic in Career Learning
4. Read theory content and external resources

Afternoon:
5. Take Career Quiz (10 questions)
6. Quiz auto-completes roadmap day
7. Take Academic Quiz if available

Evening:
8. Complete Wellbeing Assessment
9. Use SLU GPT for homework help
10. Review Performance Analytics
```

### **Weekly Admin Workflow:**

```
Monday:
1. Log in to Admin Dashboard
2. Check Students Info table
3. Identify high-risk students

Mid-Week:
4. Add new students for upcoming semester
5. Update course catalog as needed

Friday:
6. Review overall class performance
7. Plan interventions for struggling students
8. Generate reports based on risk levels
```

---

## Key Benefits of Each Feature

### **1. Career Learning Roadmap**
- **Benefit**: Structured 90-day path prevents aimless learning
- **Day-locking**: Ensures sequential mastery
- **AI Content**: Personalized to career goals

### **2. Dual Quiz System**
- **Benefit**: Tests both specialized (career) and broad (academic) knowledge
- **Auto-grading**: Instant feedback saves time
- **AI Feedback**: Personalized improvement suggestions

### **3. Wellbeing Tracking**
- **Benefit**: Early detection of mental health issues
- **Daily Check-ins**: Builds awareness habit
- **AI Insights**: Motivational support

### **4. Performance Analytics**
- **Benefit**: Data-driven insights into progress
- **Trend Analysis**: Spot patterns early
- **Risk Assessment**: Proactive intervention

### **5. SLU GPT**
- **Benefit**: 24/7 personalized tutoring
- **Context-aware**: Understands your courses
- **Rich formatting**: Clear, readable responses

### **6. Admin Dashboard**
- **Benefit**: Centralized student management
- **Auto-roadmap**: Saves hours of manual planning
- **Risk Monitoring**: Prioritize support resources

---

## Technical Notes

### **Security Features:**
- Session-based authentication
- Server-side day-locking validation
- Admin authorization checks
- Password protection (enhance with hashing for production)

### **AI Integration:**
- OpenAI GPT-4 for all AI features
- Retry logic for reliability
- Graceful degradation if API unavailable

### **Performance:**
- SQLite database for fast queries
- Chart.js for smooth graph rendering
- Responsive design for all devices

---

## Troubleshooting Common Issues

### **Can't log in:**
- Check email and password spelling
- Use sample credentials for testing
- Contact admin to reset password

### **Roadmap day locked:**
- Complete current day first
- Take Career Quiz to auto-complete
- Or manually mark as complete

### **Quiz not loading:**
- Ensure AI service is configured
- Check OpenAI API key
- Try refreshing the page

### **Graphs not showing:**
- Need historical data first
- Take quizzes for at least 3 days
- Check browser console for errors

---

## Conclusion

ForgeEd provides a comprehensive, AI-enhanced learning experience that combines:
- **Structured learning** (90-day roadmap)
- **Knowledge assessment** (dual quizzes)
- **Mental health support** (wellbeing tracking)
- **Performance insights** (analytics)
- **Personalized tutoring** (SLU GPT)
- **Administrative control** (admin dashboard)

Every interaction is designed to support student success through data-driven insights and AI-powered assistance.

---

**For more information, see:**
- `README.md` - Installation and setup
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `GITHUB_SETUP.md` - Git and GitHub guide

**Support:** Open an issue on GitHub for questions or problems.
