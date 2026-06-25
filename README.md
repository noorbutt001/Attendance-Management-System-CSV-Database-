attendance_system/
├── main.py                 # Entry point with CLI menu
├── config.py              # Configuration & database setup
├── modules/
│   ├── __init__.py
│   ├── attendance.py      # Attendance marking & retrieval
│   ├── database.py        # Database operations
│   ├── csv_handler.py     # CSV export/import
│   ├── reports.py         # Report generation
│   ├── validation.py      # Input validation
│   └── sync.py            # CSV-Database sync
├── gui/
│   └── gui_app.py         # Tkinter GUI interface
├── backup/                # Auto-backup directory
├── reports/               # Generated reports directory
├── data/                  # CSV & Database files
└── requirements.txt       # Dependencies

# 🐍 Attendance Management System

A comprehensive Python-based Attendance Management System designed for managing employee attendance records using SQLite, CSV files, and a user-friendly CLI/GUI interface.

---

## 📌 Features

### Employee Management

* Add new employees
* View all employees
* Search employees by ID or name
* Import employees from CSV

### Attendance Management

* Mark attendance (Present, Absent, Late)
* Update attendance records
* Delete attendance records
* Prevent duplicate attendance entries for the same day

### Data Management

* SQLite database storage
* CSV import/export support
* Database-to-CSV synchronization
* CSV-to-Database synchronization
* Automatic data validation

### Reporting

* Individual attendance reports
* Monthly attendance reports
* Export reports in:

  * CSV
  * JSON
  * TXT

### Additional Features

* Attendance statistics
* Backup creation
* Search attendance records
* Command Line Interface (CLI)
* Graphical User Interface (GUI) using Tkinter

---

## 📂 Project Structure

```text
attendance_system/
│
├── main.py
├── requirements.txt
│
├── modules/
│   ├── __init__.py
│   ├── database.py
│   ├── csv_handler.py
│   ├── validation.py
│   └── reports.py
│
├── gui/
│   └── gui_app.py
│
├── data/
├── reports/
└── backup/
```

---

## 🛠 Requirements

* Python 3.9 or higher
* SQLite3 (included with Python)

Install required packages:

```bash
pip install -r requirements.txt
```

---

## 📦 Dependencies

```text
matplotlib==3.7.1
pandas==2.0.3
openpyxl==3.1.2
python-dateutil==2.8.2
```

---

## 🚀 Running the Application

### Run CLI Version

```bash
python main.py
```

### Run GUI Version

```bash
python gui/gui_app.py
```

---

## 👨‍💼 Adding an Employee

1. Select Employee Management.
2. Choose Add Employee.
3. Enter:

   * Employee ID
   * Name
   * Email
   * Department

Example:

```text
Employee ID: EMP001
Name: Ali Khan
Email: ali@gmail.com
Department: IT
```

---

## 📅 Marking Attendance

1. Select Mark Attendance.
2. Enter Employee ID.
3. Enter Date.
4. Select Status:

   * Present
   * Absent
   * Late
5. Add optional remarks.

Example:

```text
Employee ID: EMP001
Date: 2026-06-25
Status: Present
Remarks: On Time
```

---

## 📊 Generating Reports

### Individual Report

Generate attendance reports for a specific employee within a selected date range.

Supported formats:

* CSV
* JSON
* TXT

### Monthly Report

Generate attendance summaries for all employees for a selected month.

---

## 💾 CSV Operations

### Export Database to CSV

```text
Menu → CSV Operations → Export Database to CSV
```

### Import CSV to Database

```text
Menu → CSV Operations → Import CSV to Database
```

---

## 🔄 Backup System

Create a backup of the SQLite database from:

```text
Settings → Create Backup
```

Backups are stored in:

```text
backup/
```

---

## 📈 Statistics

View:

* Total employees
* Total attendance records
* Attendance distribution
* Number of recorded days

Location:

```text
Settings → Data Statistics
```

---

## 🔍 Search Records

Search attendance records using:

* Employee ID
* Employee Name

Search results are displayed in a formatted table.

---

## 🗄 Database Schema

### Employees Table

| Field      | Type    |
| ---------- | ------- |
| id         | INTEGER |
| emp_id     | TEXT    |
| name       | TEXT    |
| email      | TEXT    |
| department | TEXT    |

### Attendance Table

| Field   | Type    |
| ------- | ------- |
| id      | INTEGER |
| emp_id  | TEXT    |
| name    | TEXT    |
| date    | DATE    |
| status  | TEXT    |
| remarks | TEXT    |

---

## 🧪 Sample Login-Free Workflow

```text
1. Add Employee
2. Mark Attendance
3. View Records
4. Generate Reports
5. Export Data
```

---

## ⚠️ Common Issues

### Module Not Found

Ensure the project structure is correct and contains:

```text
modules/__init__.py
```

### GUI Not Opening

Install Tkinter:

```bash
pip install tk
```

---

## 👨‍💻 Technologies Used

* Python
* SQLite
* Tkinter
* CSV
* JSON
* Pandas
* OpenPyXL

---

## 📜 License

This project is developed for educational and learning purposes. You are free to modify and extend it according to your requirements.

---

## ✨ Author

Developed as a complete Python Attendance Management System project demonstrating:

* Database Programming
* File Handling
* Data Validation
* Reporting
* GUI Development
* Modular Software Design
