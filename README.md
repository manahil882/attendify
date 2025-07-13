# 🎓 Attendify: Facial Recognition Attendance System

---

## 📑 Table of Contents

- [About Attendify](#about-attendify)  
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Installation and Setup](#installation-and-setup)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Future Implementations](#future-implementations)  
- [Contributing](#contributing)    

---

## 📘 About Attendify

**Attendify** is a robust and user-friendly facial recognition attendance system designed to automate and streamline the attendance marking process for educational institutions or organizations. Leveraging advanced computer vision techniques, Attendify can detect faces from group photos and accurately mark attendance with timestamps, reducing manual effort and increasing efficiency.

---

## ✨ Features

Attendify offers a range of features to cater to different user roles (Admin, Teacher, Student):

- **Separate Panels**: Dedicated and intuitive interfaces for students, teachers, and administrators.
- **User-Friendly Interface**: Simple and accessible for all users.
- **High-Accuracy Face Recognition**: Uses the `dlib` library and OpenCV for reliable detection and recognition.
- **Timestamped Attendance**: Records date and time automatically for each entry.

### 🛠 Admin Management:
- Secure admin login with a predefined password.
- Manage departments, subjects, faculty, and assign subjects.
- Enroll students and manage student data.
- View and clear attendance records.

### 👨‍🏫 Teacher Functionality:
- Mark attendance using group photos.
- View attendance records.

### 🎓 Student Functionality:
- View their attendance records.

---

## 💻 Technology Stack

Attendify is built using the following technologies:

- **Python**
- **Tkinter**
- **OpenCV (cv2)**
- **face_recognition (dlib)**
- **MySQL Connector**
- **SQLite3**
- **NumPy**
- **datetime**
- **tkinter.filedialog**
- **PIL (Pillow)**
- **haarcascade_frontalface_default.xml**

---

## 🧰 Installation and Setup

### 📌 Prerequisites

- Python 3.x
- MySQL Server

---

### 🔧 1. Clone the Repository

```
git clone https://github.com/manahil882/attendify
cd Attendify
```
---

### 📦 2. Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install opencv-python face-recognition mysql-connector-python Pillow numpy
```
### 🛢 3. Database Setup
🔹 MySQL Setup:
```
CREATE DATABASE attendify_db;
USE attendify_db;
```
## Then create these tables:
```
-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(100),
    department VARCHAR(100),
    image_encoding BLOB
);
```
```
-- Faculty Table
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100)
);
```
```
-- Subjects Table
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(50) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    department VARCHAR(100)
);
```
```
-- Assign Subjects
CREATE TABLE IF NOT EXISTS assigned_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id VARCHAR(50) NOT NULL,
    subject_code VARCHAR(50) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_code) REFERENCES subjects(subject_code)
);
```
```
-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    attendance_status VARCHAR(20) NOT NULL
);
```
```
-- Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);
```
Update credentials in app.py:

```
self.db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",
    password="your_mysql_password",
    database="attendify_db"
)
```
---
### 🔹 SQLite Setup
The SQLite DB will be created automatically for storing the admin password.

Default Admin Password: admin123

You can change this in the CustomDialog class inside app.py.

---

### 🧠 4. Place Haar Cascade XML
Ensure haarcascade_frontalface_default.xml is in the same directory as app.py.

---

### 🧑‍🎓 5. Prepare Face Data

Create Training_images/ directory and place student images there.

---

### Important:  Filenames (e.g., John_Doe.jpg) are used as identifiers during attendance.
---

### 🚀 Usage
▶️ Run the Application
```
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

🔐 Admin Panel
---
Launch app and login using default admin password.

Manage departments, subjects, faculty, students.

Add student photos in Training_images/ as described above.

---

🧑‍🏫 Teacher Panel
---
Select group photo to mark attendance.

Recognizes students and saves attendance records.

---

👩‍🎓 Student Panel
---
Students can view their attendance history.

---
🗂 Project Structure
```
Attendify/
├── app.py
├── student_data.py
├── haarcascade_frontalface_default.xml
├── firstPage.png
├── Admin.jpg
├── Attendify.jpg
├── img.jpg
├── OKY.png
└── Training_images/
    ├── student1.jpg
    ├── student2.png
    └── ...
```
---

### 🔮 Future Implementations
--- 
Student Defaulter Check

Enhanced Faculty Management

Class-specific Attendance

Attendance Report Download (PDF, CSV)

### 🤝 Contributing
Fork the repository

Create a new branch:
```
git checkout -b feature/your-feature-name
```
Commit your changes

Push and create a Pull Request

Please ensure code readability and documentation.


