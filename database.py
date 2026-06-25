import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class AttendanceDatabase:
    """SQLite Database Management for Attendance System"""
    
    def __init__(self, db_path: str = "data/attendance.db"):
        """Initialize database connection and create tables"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.connection = None
        self.initialize_database()
    
    def connect(self):
        """Create database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Access columns by name
        return self.connection
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def initialize_database(self):
        """Create tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Students/Employees Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Attendance Records Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT NOT NULL,
                name TEXT NOT NULL,
                date DATE NOT NULL,
                status TEXT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
                UNIQUE(emp_id, date)
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_emp_id ON attendance(emp_id)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_date ON attendance(date)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON attendance(status)
        ''')
        
        conn.commit()
        self.disconnect()
    
    def add_employee(self, emp_id: str, name: str, email: str = "", 
                     department: str = "") -> bool:
        """Add new employee"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (emp_id, name, email, department)
                VALUES (?, ?, ?, ?)
            ''', (emp_id, name.strip(), email.strip(), department.strip()))
            conn.commit()
            self.disconnect()
            return True
        except sqlite3.IntegrityError:
            self.disconnect()
            print(f"❌ Employee ID '{emp_id}' already exists!")
            return False
        except Exception as e:
            self.disconnect()
            print(f"❌ Error adding employee: {str(e)}")
            return False
    
    def get_employee(self, emp_id: str) -> Optional[Dict]:
        """Retrieve employee details"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE emp_id = ?', (emp_id,))
        result = cursor.fetchone()
        self.disconnect()
        return dict(result) if result else None
    
    def get_all_employees(self) -> List[Dict]:
        """Get all employees"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees ORDER BY name ASC')
        results = cursor.fetchall()
        self.disconnect()
        return [dict(row) for row in results]
    
    def mark_attendance(self, emp_id: str, name: str, date: str, 
                       status: str, remarks: str = "") -> bool:
        """Mark attendance (Present/Absent/Late)"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check for duplicate entry on same day
            cursor.execute('''
                SELECT id FROM attendance 
                WHERE emp_id = ? AND date = ?
            ''', (emp_id, date))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE attendance 
                    SET status = ?, remarks = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE emp_id = ? AND date = ?
                ''', (status, remarks, emp_id, date))
                print(f"✏️  Updated attendance for {name} on {date}")
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO attendance (emp_id, name, date, status, remarks)
                    VALUES (?, ?, ?, ?, ?)
                ''', (emp_id, name, date, status, remarks))
                print(f"✅ Marked {name} as {status} on {date}")
            
            conn.commit()
            self.disconnect()
            return True
        except Exception as e:
            self.disconnect()
            print(f"❌ Error marking attendance: {str(e)}")
            return False
    
    def get_attendance_by_emp_id(self, emp_id: str, 
                                 start_date: str = None, 
                                 end_date: str = None) -> List[Dict]:
        """Retrieve attendance records for employee"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute('''
                SELECT * FROM attendance 
                WHERE emp_id = ? AND date BETWEEN ? AND ?
                ORDER BY date DESC
            ''', (emp_id, start_date, end_date))
        else:
            cursor.execute('''
                SELECT * FROM attendance 
                WHERE emp_id = ? 
                ORDER BY date DESC
            ''', (emp_id,))
        
        results = cursor.fetchall()
        self.disconnect()
        return [dict(row) for row in results]
    
    def get_attendance_by_date(self, date: str) -> List[Dict]:
        """Get all attendance records for a specific date"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE date = ?
            ORDER BY name ASC
        ''', (date,))
        results = cursor.fetchall()
        self.disconnect()
        return [dict(row) for row in results]
    
    def get_attendance_report(self, emp_id: str, 
                             start_date: str, 
                             end_date: str) -> Dict:
        """Generate attendance statistics"""
        records = self.get_attendance_by_emp_id(emp_id, start_date, end_date)
        
        total_days = len(records)
        if total_days == 0:
            return {
                'emp_id': emp_id,
                'total_days': 0,
                'present': 0,
                'absent': 0,
                'late': 0,
                'attendance_percentage': 0
            }
        
        present = sum(1 for r in records if r['status'] == 'Present')
        absent = sum(1 for r in records if r['status'] == 'Absent')
        late = sum(1 for r in records if r['status'] == 'Late')
        
        attendance_percentage = (present / total_days) * 100 if total_days > 0 else 0
        
        return {
            'emp_id': emp_id,
            'total_days': total_days,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_percentage': round(attendance_percentage, 2)
        }
    
    def update_attendance(self, emp_id: str, date: str, status: str, 
                         remarks: str = "") -> bool:
        """Update attendance record"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE attendance 
                SET status = ?, remarks = ?, updated_at = CURRENT_TIMESTAMP
                WHERE emp_id = ? AND date = ?
            ''', (status, remarks, emp_id, date))
            conn.commit()
            self.disconnect()
            return cursor.rowcount > 0
        except Exception as e:
            self.disconnect()
            print(f"❌ Error updating attendance: {str(e)}")
            return False
    
    def delete_attendance(self, emp_id: str, date: str) -> bool:
        """Delete attendance record"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM attendance 
                WHERE emp_id = ? AND date = ?
            ''', (emp_id, date))
            conn.commit()
            self.disconnect()
            return cursor.rowcount > 0
        except Exception as e:
            self.disconnect()
            print(f"❌ Error deleting attendance: {str(e)}")
            return False
    
    def search_attendance(self, search_term: str, search_type: str = 'emp_id') -> List[Dict]:
        """Search attendance with case-insensitive search"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if search_type == 'name':
            cursor.execute('''
                SELECT DISTINCT * FROM attendance 
                WHERE LOWER(name) LIKE LOWER(?)
                ORDER BY date DESC
            ''', (f'%{search_term}%',))
        elif search_type == 'emp_id':
            cursor.execute('''
                SELECT * FROM attendance 
                WHERE emp_id LIKE ?
                ORDER BY date DESC
            ''', (f'%{search_term}%',))
        else:
            return []
        
        results = cursor.fetchall()
        self.disconnect()
        return [dict(row) for row in results]