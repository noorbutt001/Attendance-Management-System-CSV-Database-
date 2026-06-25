#!/usr/bin/env python3
"""
🐍 Attendance Management System - CLI Interface
Features: Marking attendance, viewing records, generating reports, CSV/DB sync
"""

import os
import sys
from datetime import datetime, timedelta
from modules.database import AttendanceDatabase
from modules.csv_handler import CSVHandler
from modules.validation import InputValidator
from modules.reports import ReportGenerator

class AttendanceManagementSystem:
    """Main CLI Interface for Attendance System"""
    
    def __init__(self):
        """Initialize system"""
        self.db = AttendanceDatabase()
        self.csv_handler = CSVHandler()
        self.report_gen = ReportGenerator()
        self.validator = InputValidator()
        self.running = True
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title: str):
        """Print styled header"""
        print("\n" + "=" * 60)
        print(f"🐍 {title}".center(60))
        print("=" * 60 + "\n")
    
    def main_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.print_header("ATTENDANCE MANAGEMENT SYSTEM")
        
        print("📋 MAIN MENU:")
        print("-" * 60)
        print("1. ➕  Mark Attendance")
        print("2. 👥  Employee Management")
        print("3. 📊 View Attendance Records")
        print("4. ✏️  Update/Delete Records")
        print("5. 📈 Generate Reports")
        print("6. 💾 CSV Operations")
        print("7. 🔄 Sync CSV-Database")
        print("8. 🔍 Search Records")
        print("9. ⚙️  Settings")
        print("0. ❌ Exit")
        print("-" * 60)
    
    def mark_attendance_menu(self):
        """Mark attendance submenu"""
        self.print_header("MARK ATTENDANCE")
        
        emp_id = input("👤 Enter Employee ID: ").strip().upper()
        is_valid, msg = self.validator.validate_emp_id(emp_id)
        if not is_valid:
            print(f"❌ {msg}")
            return
        
        # Check if employee exists
        employee = self.db.get_employee(emp_id)
        if not employee:
            print(f"❌ Employee {emp_id} not found. Add employee first.")
            return
        
        name = employee['name']
        
        date_str = input("📅 Enter Date (YYYY-MM-DD) [Today]: ").strip() or \
                   datetime.now().strftime('%Y-%m-%d')
        is_valid, msg = self.validator.validate_date(date_str)
        if not is_valid:
            print(f"❌ {msg}")
            return
        
        print("\n📝 Attendance Status:")
        print("1. Present")
        print("2. Absent")
        print("3. Late")
        
        choice = input("Select status (1-3): ").strip()
        status_map = {'1': 'Present', '2': 'Absent', '3': 'Late'}
        status = status_map.get(choice, 'Absent')
        
        remarks = input("💬 Enter Remarks (optional): ").strip()
        
        # Confirm before marking
        print(f"\n📌 Confirm Details:")
        print(f"   Employee: {name} ({emp_id})")
        print(f"   Date: {date_str}")
        print(f"   Status: {status}")
        print(f"   Remarks: {remarks or 'None'}")
        
        confirm = input("\nConfirm marking attendance? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.db.mark_attendance(emp_id, name, date_str, status, remarks):
                print("✅ Attendance marked successfully!")
            else:
                print("❌ Failed to mark attendance!")
        else:
            print("⚠️  Marking cancelled!")
        
        input("\nPress Enter to continue...")
    
    def view_records_menu(self):
        """View attendance records submenu"""
        self.print_header("VIEW ATTENDANCE RECORDS")
        
        print("1. View by Employee ID")
        print("2. View by Date")
        print("3. View all Records")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            emp_id = input("Enter Employee ID: ").strip().upper()
            records = self.db.get_attendance_by_emp_id(emp_id)
            
            if not records:
                print(f"❌ No records found for {emp_id}")
            else:
                self._display_records(records)
        
        elif choice == '2':
            date = input("Enter Date (YYYY-MM-DD): ").strip()
            is_valid, msg = self.validator.validate_date(date)
            if not is_valid:
                print(f"❌ {msg}")
                return
            
            records = self.db.get_attendance_by_date(date)
            if not records:
                print(f"❌ No records found for {date}")
            else:
                self._display_records(records)
        
        elif choice == '3':
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attendance ORDER BY date DESC LIMIT 100')
            records = [dict(row) for row in cursor.fetchall()]
            self.db.disconnect()
            
            if records:
                self._display_records(records)
            else:
                print("❌ No records found")
        
        input("\nPress Enter to continue...")
    
    def _display_records(self, records):
        """Display attendance records in table format"""
        print("\n" + "=" * 80)
        print(f"{'Date':<12} {'Emp ID':<12} {'Name':<20} {'Status':<10} {'Remarks':<20}")
        print("=" * 80)
        
        for record in records[:50]:  # Display first 50 records
            print(f"{record['date']:<12} {record['emp_id']:<12} "
                  f"{record['name']:<20} {record['status']:<10} "
                  f"{record['remarks'] or '':<20}")
        
        print("=" * 80)
        print(f"Total records displayed: {len(records)}")
    
    def update_delete_menu(self):
        """Update/Delete records submenu"""
        self.print_header("UPDATE/DELETE RECORDS")
        
        emp_id = input("Enter Employee ID: ").strip().upper()
        date = input("Enter Date (YYYY-MM-DD): ").strip()
        
        is_valid, msg = self.validator.validate_date(date)
        if not is_valid:
            print(f"❌ {msg}")
            return
        
        records = self.db.get_attendance_by_emp_id(emp_id, date, date)
        if not records:
            print(f"❌ No record found for {emp_id} on {date}")
            return
        
        record = records[0]
        print(f"\nCurrent Record: {record['status']} - {record['remarks']}")
        
        print("\n1. Update Status")
        print("2. Update Remarks")
        print("3. Delete Record")
        
        choice = input("Select action (1-3): ").strip()
        
        if choice == '1':
            print("1. Present\n2. Absent\n3. Late")
            status_choice = input("New status (1-3): ").strip()
            status_map = {'1': 'Present', '2': 'Absent', '3': 'Late'}
            new_status = status_map.get(status_choice, record['status'])
            
            if self.db.update_attendance(emp_id, date, new_status, record['remarks']):
                print("✅ Updated successfully!")
            else:
                print("❌ Update failed!")
        
        elif choice == '2':
            new_remarks = input("New remarks: ").strip()
            if self.db.update_attendance(emp_id, date, record['status'], new_remarks):
                print("✅ Updated successfully!")
            else:
                print("❌ Update failed!")
        
        elif choice == '3':
            confirm = input("Delete this record? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.db.delete_attendance(emp_id, date):
                    print("✅ Deleted successfully!")
                else:
                    print("❌ Deletion failed!")
        
        input("\nPress Enter to continue...")
    
    def generate_reports_menu(self):
        """Generate reports submenu"""
        self.print_header("GENERATE REPORTS")
        
        print("1. Individual Employee Report")
        print("2. Monthly Report")
        print("3. Department Report")
        
        choice = input("Select report type (1-3): ").strip()
        
        if choice == '1':
            emp_id = input("Enter Employee ID: ").strip().upper()
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()
            
            is_valid, msg = self.validator.validate_date_range(start_date, end_date)
            if not is_valid:
                print(f"❌ {msg}")
                return
            
            print("\nExport Format:")
            print("1. CSV")
            print("2. JSON")
            print("3. TXT")
            
            format_choice = input("Select format (1-3): ").strip()
            format_map = {'1': 'csv', '2': 'json', '3': 'txt'}
            file_format = format_map.get(format_choice, 'csv')
            
            filename = self.report_gen.generate_individual_report(
                emp_id, start_date, end_date, file_format
            )
            
            if filename:
                print(f"✅ Report generated: {filename}")
        
        elif choice == '2':
            year = int(input("Year (YYYY): "))
            month = int(input("Month (1-12): "))
            
            if month < 1 or month > 12:
                print("❌ Invalid month!")
                return
            
            filename = self.report_gen.generate_monthly_report(year, month)
            if filename:
                print(f"✅ Report generated: {filename}")
        
        input("\nPress Enter to continue...")
    
    def employee_management_menu(self):
        """Employee management submenu"""
        self.print_header("EMPLOYEE MANAGEMENT")
        
        print("1. Add New Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Import Employees from CSV")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            self._add_employee()
        elif choice == '2':
            self._view_all_employees()
        elif choice == '3':
            self._search_employee()
        elif choice == '4':
            self._import_employees_csv()
        
        input("\nPress Enter to continue...")
    
    def _add_employee(self):
        """Add new employee"""
        print("\n➕ ADD NEW EMPLOYEE")
        print("-" * 60)
        
        emp_id = input("Employee ID: ").strip().upper()
        is_valid, msg = self.validator.validate_emp_id(emp_id)
        if not is_valid:
            print(f"❌ {msg}")
            return
        
        name = input("Full Name: ").strip()
        is_valid, msg = self.validator.validate_name(name)
        if not is_valid:
            print(f"❌ {msg}")
            return
        
        email = input("Email (optional): ").strip()
        if email:
            is_valid, msg = self.validator.validate_email(email)
            if not is_valid:
                print(f"❌ {msg}")
                return
        
        department = input("Department: ").strip()
        
        if self.db.add_employee(emp_id, name, email, department):
            print("✅ Employee added successfully!")
        else:
            print("❌ Failed to add employee!")
    
    def _view_all_employees(self):
        """View all employees"""
        employees = self.db.get_all_employees()
        
        if not employees:
            print("\n❌ No employees found!")
            return
        
        print("\n" + "=" * 80)
        print(f"{'Emp ID':<12} {'Name':<20} {'Email':<25} {'Department':<20}")
        print("=" * 80)
        
        for emp in employees:
            print(f"{emp['emp_id']:<12} {emp['name']:<20} "
                  f"{emp['email']:<25} {emp['department']:<20}")
        
        print("=" * 80)
        print(f"Total employees: {len(employees)}")
    
    def _search_employee(self):
        """Search for employee"""
        search_term = input("Search (Emp ID or Name): ").strip()
        
        # Try emp_id first
        employee = self.db.get_employee(search_term.upper())
        
        if employee:
            print(f"\n✅ Found: {employee['name']} ({employee['emp_id']})")
            print(f"   Email: {employee['email']}")
            print(f"   Department: {employee['department']}")
        else:
            # Try case-insensitive name search
            employees = self.db.get_all_employees()
            matches = [e for e in employees if search_term.lower() in e['name'].lower()]
            
            if matches:
                for emp in matches:
                    print(f"✅ Found: {emp['name']} ({emp['emp_id']})")
            else:
                print("❌ No employee found!")
    
    def _import_employees_csv(self):
        """Import employees from CSV"""
        filename = input("CSV filename (data/employees.csv): ").strip() or "data/employees.csv"
        count = self.csv_handler.batch_import_employees(filename)
        print(f"✅ Imported {count} employees!")
    
    def csv_operations_menu(self):
        """CSV operations submenu"""
        self.print_header("CSV OPERATIONS")
        
        print("1. Export Database to CSV")
        print("2. Import CSV to Database")
        print("3. View CSV File")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            if self.csv_handler.sync_database_to_csv():
                print("✅ Data exported to CSV!")
        
        elif choice == '2':
            filename = input("CSV filename (data/attendance.csv): ").strip() or "data/attendance.csv"
            if self.csv_handler.sync_csv_to_database(filename):
                print("✅ Data imported from CSV!")
        
        elif choice == '3':
            data = self.csv_handler.import_from_csv()
            if data:
                for record in data[:20]:
                    print(record)
                if len(data) > 20:
                    print(f"... and {len(data) - 20} more records")
        
        input("\nPress Enter to continue...")
    
    def search_records_menu(self):
        """Search records submenu"""
        self.print_header("SEARCH RECORDS")
        
        print("1. Search by Employee ID")
        print("2. Search by Name")
        
        choice = input("Select search type (1-2): ").strip()
        
        search_term = input("Enter search term: ").strip()
        
        if choice == '1':
            search_type = 'emp_id'
        elif choice == '2':
            search_type = 'name'
        else:
            print("❌ Invalid choice!")
            return
        
        results = self.db.search_attendance(search_term, search_type)
        
        if results:
            self._display_records(results)
        else:
            print("❌ No records found!")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Settings submenu"""
        self.print_header("SETTINGS")
        
        print("1. Create Backup")
        print("2. Data Statistics")
        print("3. Export All Data")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            self._create_backup()
        elif choice == '2':
            self._show_statistics()
        elif choice == '3':
            self._export_all_data()
        
        input("\nPress Enter to continue...")
    
    def _create_backup(self):
        """Create database backup"""
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup/attendance_backup_{timestamp}.db"
        
        os.makedirs('backup', exist_ok=True)
        
        try:
            shutil.copy2('data/attendance.db', backup_file)
            print(f"✅ Backup created: {backup_file}")
        except Exception as e:
            print(f"❌ Backup failed: {str(e)}")
    
    def _show_statistics(self):
        """Show data statistics"""
        conn = self.db.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM employees')
        emp_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM attendance')
        att_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(DISTINCT date) as count FROM attendance')
        days_count = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT status, COUNT(*) as count FROM attendance 
            GROUP BY status
        ''')
        status_dist = cursor.fetchall()
        
        self.db.disconnect()
        
        print("\n📊 SYSTEM STATISTICS")
        print("-" * 60)
        print(f"Total Employees: {emp_count}")
        print(f"Total Attendance Records: {att_count}")
        print(f"Days with Records: {days_count}")
        print("\nAttendance Distribution:")
        for row in status_dist:
            print(f"  {row['status']}: {row['count']}")
    
    def _export_all_data(self):
        """Export all data"""
        format_choice = input("Export format (csv/json): ").strip().lower()
        
        if format_choice in ['csv', 'json']:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attendance')
            records = [dict(row) for row in cursor.fetchall()]
            self.db.disconnect()
            
            if format_choice == 'csv':
                filename = f"reports/full_export_{timestamp}.csv"
                self.csv_handler.export_to_csv(records, filename)
            else:
                filename = f"reports/full_export_{timestamp}.json"
                import json
                with open(filename, 'w') as f:
                    json.dump(records, f, indent=2, default=str)
                print(f"✅ Data exported to {filename}")
    
    def run(self):
        """Run the main application"""
        while self.running:
            self.main_menu()
            
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using Attendance Management System!")
                self.running = False
            elif choice == '1':
                self.mark_attendance_menu()
            elif choice == '2':
                self.employee_management_menu()
            elif choice == '3':
                self.view_records_menu()
            elif choice == '4':
                self.update_delete_menu()
            elif choice == '5':
                self.generate_reports_menu()
            elif choice == '6':
                self.csv_operations_menu()
            elif choice == '7':
                self.print_header("CSV-DATABASE SYNC")
                print("1. Sync CSV → Database")
                print("2. Sync Database → CSV")
                sync_choice = input("Select (1-2): ").strip()
                
                if sync_choice == '1':
                    filename = input("CSV file: ").strip() or "data/attendance.csv"
                    self.csv_handler.sync_csv_to_database(filename)
                elif sync_choice == '2':
                    self.csv_handler.sync_database_to_csv()
                
                input("\nPress Enter to continue...")
            elif choice == '8':
                self.search_records_menu()
            elif choice == '9':
                self.settings_menu()
            else:
                print("❌ Invalid choice! Please try again.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        system = AttendanceManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")