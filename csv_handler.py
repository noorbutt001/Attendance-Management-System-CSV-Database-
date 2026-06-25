import csv
import os
from datetime import datetime
from typing import List, Dict
from .database import AttendanceDatabase

class CSVHandler:
    """CSV file operations for attendance data"""
    
    def __init__(self, csv_path: str = "data/attendance.csv"):
        """Initialize CSV handler"""
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        self.db = AttendanceDatabase()
    
    def export_to_csv(self, data: List[Dict], filename: str = None) -> bool:
        """Export attendance data to CSV"""
        try:
            if filename is None:
                filename = self.csv_path
            
            if not data:
                print("⚠️  No data to export!")
                return False
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            keys = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✅ Data exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting to CSV: {str(e)}")
            return False
    
    def import_from_csv(self, filename: str = None) -> List[Dict]:
        """Import attendance data from CSV"""
        try:
            if filename is None:
                filename = self.csv_path
            
            if not os.path.exists(filename):
                print(f"⚠️  File not found: {filename}")
                return []
            
            data = []
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
            
            print(f"✅ Imported {len(data)} records from {filename}")
            return data
        except Exception as e:
            print(f"❌ Error importing CSV: {str(e)}")
            return []
    
    def sync_csv_to_database(self, csv_file: str = None) -> bool:
        """Synchronize CSV data to database"""
        try:
            data = self.import_from_csv(csv_file)
            if not data:
                return False
            
            for record in data:
                if 'emp_id' in record and 'name' in record and 'date' in record:
                    self.db.mark_attendance(
                        emp_id=record['emp_id'],
                        name=record['name'],
                        date=record['date'],
                        status=record.get('status', 'Absent'),
                        remarks=record.get('remarks', '')
                    )
            
            print(f"✅ Synced {len(data)} records from CSV to database")
            return True
        except Exception as e:
            print(f"❌ Error syncing CSV to database: {str(e)}")
            return False
    
    def sync_database_to_csv(self, csv_file: str = None) -> bool:
        """Synchronize database to CSV file"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attendance ORDER BY date DESC, name ASC')
            data = [dict(row) for row in cursor.fetchall()]
            self.db.disconnect()
            
            if not data:
                print("⚠️  No records in database to export")
                return False
            
            if csv_file is None:
                csv_file = self.csv_path
            
            return self.export_to_csv(data, csv_file)
        except Exception as e:
            print(f"❌ Error syncing database to CSV: {str(e)}")
            return False
    
    def batch_import_employees(self, csv_file: str) -> int:
        """Bulk import employees from CSV"""
        try:
            data = self.import_from_csv(csv_file)
            imported_count = 0
            
            for record in data:
                if 'emp_id' in record and 'name' in record:
                    if self.db.add_employee(
                        emp_id=record['emp_id'],
                        name=record['name'],
                        email=record.get('email', ''),
                        department=record.get('department', '')
                    ):
                        imported_count += 1
            
            print(f"✅ Imported {imported_count} employees")
            return imported_count
        except Exception as e:
            print(f"❌ Error batch importing employees: {str(e)}")
            return 0