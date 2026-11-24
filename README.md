# 🎓 Smart Campus Management System

A web-based campus management platform designed to simplify communication between students and college administration through centralized complaint management, announcement sharing, and administrative monitoring.

## 📌 Project Overview

The **Smart Campus Management System** is a centralized web application developed to improve campus operations, enhance communication, and provide an efficient platform for managing student-related activities.

The system enables students to register, log in, submit campus-related complaints, track complaint progress, and receive important announcements. Administrators can manage student complaints, update their status, publish announcements, and monitor overall campus activities through an interactive dashboard.

The application aims to reduce manual paperwork, improve transparency, and create a more organized and responsive campus environment.

## 🎯 Objectives

- Develop a centralized digital platform for campus management.
- Simplify the complaint submission and resolution process.
- Improve communication between students and administration.
- Provide transparent complaint tracking and status updates.
- Enable administrators to monitor and manage campus issues efficiently.
- Reduce manual work through digital automation.

## ✨ Key Features

### 👨‍🎓 Student Module
- Student registration and secure login.
- Personalized student dashboard.
- Submit campus-related complaints.
- Select complaint categories.
- Track complaint status.
- View complaint history.
- Access college announcements.

### 👨‍💼 Admin Module
- Secure administrator authentication.
- Interactive administrative dashboard.
- View and manage registered students.
- Monitor total, pending, and resolved complaints.
- Review and manage student complaints.
- Update complaint status.
- Publish and manage campus announcements.
- Search and filter complaints.

### 📝 Complaint Management
Students can report issues related to:
- Classroom facilities.
- Laboratory equipment.
- Library facilities.
- Hostel maintenance.
- Electricity and water supply.
- Internet and Wi-Fi connectivity.
- Washroom maintenance.
- Other campus-related issues.

**Complaint Status:**
- Submitted
- Under Review
- In Progress
- Resolved
- Rejected

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend interactivity |
| Bootstrap 5 | Responsive user interface |
| Chart.js | Dashboard statistics and visualization |
| VS Code | Development environment |

## 🏗️ System Architecture

The application follows a three-tier architecture:

1. **Presentation Layer:** HTML, CSS, JavaScript, and Bootstrap provide the user interface.
2. **Application Layer:** Python Flask handles authentication, business logic, complaint processing, and application routes.
3. **Database Layer:** MySQL stores student information, administrator details, complaints, and announcements.

## ⚙️ Installation and Setup

### Prerequisites

Ensure the following software is installed:

- Python 3.x
- MySQL Server
- MySQL Workbench
- Visual Studio Code
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SmartCampus.git
```

### Step 2: Navigate to the Project Directory

```bash
cd SmartCampus
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure MySQL Database

1. Open MySQL Workbench.
2. Create the required database.
3. Execute the SQL schema provided in the project.
4. Configure your database credentials in the configuration file.
5. Ensure the database connection is successful.

### Step 7: Run the Application

```bash
python app.py
```

### Step 8: Open in Browser

```text
http://127.0.0.1:5000/
```

## 📂 Project Structure

```text
SmartCampus/
│
├── app.py
├── db.py
├── config.py
├── create_admin.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── student_dashboard.html
│   ├── submit_complaint.html
│   ├── admin_dashboard.html
│   ├── manage_complaints.html
│   ├── announcements.html
│   └── profile.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
│
├── README.md
└── requirements.txt
```

## 🔐 Security Features

- Password hashing for secure credential storage.
- Session-based authentication.
- Role-based access control for students and administrators.
- Form validation and error handling.
- Restricted access to administrative functionalities.
- File upload validation.

## 🚀 Future Enhancements

- Email and SMS notifications.
- Mobile application integration.
- QR-code-based campus services.
- AI-powered complaint categorization.
- Smart campus attendance management.
- Real-time notifications.
- Advanced analytics and reporting.
- Integration with IoT-based campus monitoring systems.

## 🎓 Project Information

**Project Title:** Smart Campus Management System

**Project Domain:** Web Development / Campus Automation

**Project Type:** Academic Project

**Development Environment:** Windows 11 and Visual Studio Code

## 👨‍💻 Developer

Developed as an academic project with the objective of applying full-stack web development concepts to solve real-world campus management challenges.

## 📄 License

This project is developed for educational and academic purposes. You may adapt and modify it with appropriate attribution.
