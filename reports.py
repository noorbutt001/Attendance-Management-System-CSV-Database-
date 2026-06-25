import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict
import json
from .database import AttendanceDatabase
from .csv_handler import CSVHandler

class ReportGenerator:
    """Generate attendance reports"""
    
    def __init__(self):
        """Initialize report generator"""
        self.db = AttendanceDatabase()
        self.csv_handler = CSVHandler()
        os.makedirs('reports', exist_ok=True)
    
    def generate_individual_report(self, emp_id: str, start_date: str, 
                                   end_date: str, export_format: str = 'csv') -> str:
        """Generate individual employee attendance report"""
        try:
            report_data = self.db.get_attendance_report(emp_id, start_date, end_date)
            records = self.db.get_attendance_by_emp_id(emp_id, start_date, end_date)
            
            employee = self.db.get_employee(emp_id)
            if not employee:
                print(f"❌ Employee {emp_id} not found")
                return ""
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reports/report_{emp_id}_{timestamp}.{export_format}"
            
            if export_format == 'csv':
                return self._export_report_csv(filename, report_data, records, employee)
            elif export_format == 'json':
                return self._export_report_json(filename, report_data, records, employee)
            elif export_format == 'txt':
                return self._export_report_txt(filename, report_data, records, employee)
        except Exception as e:
            print(f"❌ Error generating report: {str(e)}")
            return ""
    
    def _export_report_csv(self, filename: str, report: Dict, 
                          records: List[Dict], employee: Dict) -> str:
        """Export report as CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['ATTENDANCE REPORT'])
                writer.writerow([])
                writer.writerow(['Employee ID:', employee['emp_id']])
                writer.writerow(['Name:', employee['name']])
                writer.writerow(['Department:', employee['department']])
                writer.writerow([])
                
                # Summary
                writer.writerow(['SUMMARY'])
                writer.writerow(['Total Days:', report['total_days']])
                writer.writerow(['Present:', report['present']])
                writer.writerow(['Absent:', report['absent']])
                writer.writerow(['Late:', report['late']])
                writer.writerow(['Attendance %:', f"{report['attendance_percentage']}%"])
                writer.writerow([])
                
                # Details
                writer.writerow(['DETAILED RECORDS'])
                writer.writerow(['Date', 'Status', 'Remarks'])
                for record in records:
                    writer.writerow([
                        record['date'],
                        record['status'],
                        record['remarks'] or ''
                    ])
            
            print(f"✅ Report exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting CSV: {str(e)}")
            return ""
    
    def _export_report_json(self, filename: str, report: Dict, 
                           records: List[Dict], employee: Dict) -> str:
        """Export report as JSON"""
        try:
            data = {
                'employee': {
                    'id': employee['emp_id'],
                    'name': employee['name'],
                    'department': employee['department']
                },
                'summary': report,
                'records': records,
                'generated_at': datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"✅ Report exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting JSON: {str(e)}")
            return ""
    
    def _export_report_txt(self, filename: str, report: Dict, 
                          records: List[Dict], employee: Dict) -> str:
        """Export report as TXT"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('=' * 60 + '\n')
                f.write('ATTENDANCE REPORT\n')
                f.write('=' * 60 + '\n\n')
                
                f.write(f"Employee ID: {employee['emp_id']}\n")
                f.write(f"Name: {employee['name']}\n")
                f.write(f"Department: {employee['department']}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write('-' * 60 + '\n')
                f.write('SUMMARY\n')
                f.write('-' * 60 + '\n')
                f.write(f"Total Days: {report['total_days']}\n")
                f.write(f"Present: {report['present']}\n")
                f.write(f"Absent: {report['absent']}\n")
                f.write(f"Late: {report['late']}\n")
                f.write(f"Attendance %: {report['attendance_percentage']}%\n\n")
                
                f.write('-' * 60 + '\n')
                f.write('DETAILED RECORDS\n')
                f.write('-' * 60 + '\n')
                f.write(f"{'Date':<12} {'Status':<10} {'Remarks':<30}\n")
                f.write('-' * 60 + '\n')
                
                for record in records:
                    f.write(f"{record['date']:<12} {record['status']:<10} "
                            f"{record['remarks'] or '':<30}\n")
                
                f.write('\n' + '=' * 60 + '\n')
            
            print(f"✅ Report exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting TXT: {str(e)}")
            return ""
    
    def generate_monthly_report(self, year: int, month: int, 
                               export_format: str = 'csv') -> str:
        """Generate monthly attendance report for all employees"""
        try:
            start_date = f"{year}-{month:02d}-01"
            
            # Calculate end date
            if month == 12:
                end_date = f"{year + 1}-01-01"
            else:
                end_date = f"{year}-{month + 1:02d}-01"
            
            employees = self.db.get_all_employees()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reports/monthly_report_{year}_{month:02d}_{timestamp}.{export_format}"
            
            if export_format == 'csv':
                return self._export_monthly_csv(filename, year, month, employees, 
                                               start_date, end_date)
            elif export_format == 'json':
                return self._export_monthly_json(filename, year, month, employees, 
                                                start_date, end_date)
        except Exception as e:
            print(f"❌ Error generating monthly report: {str(e)}")
            return ""
    
    def _export_monthly_csv(self, filename: str, year: int, month: int, 
                           employees: List[Dict], start_date: str, 
                           end_date: str) -> str:
        """Export monthly report as CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                writer.writerow([f'MONTHLY ATTENDANCE REPORT - {year}-{month:02d}'])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                writer.writerow(['Emp ID', 'Name', 'Department', 'Total Days', 
                               'Present', 'Absent', 'Late', 'Attendance %'])
                
                for emp in employees:
                    report = self.db.get_attendance_report(emp['emp_id'], 
                                                          start_date, end_date)
                    writer.writerow([
                        emp['emp_id'],
                        emp['name'],
                        emp['department'],
                        report['total_days'],
                        report['present'],
                        report['absent'],
                        report['late'],
                        f"{report['attendance_percentage']}%"
                    ])
            
            print(f"✅ Monthly report exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting monthly CSV: {str(e)}")
            return ""
    
    def _export_monthly_json(self, filename: str, year: int, month: int, 
                            employees: List[Dict], start_date: str, 
                            end_date: str) -> str:
        """Export monthly report as JSON"""
        try:
            data = {
                'month': f"{year}-{month:02d}",
                'generated_at': datetime.now().isoformat(),
                'employees': []
            }
            
            for emp in employees:
                report = self.db.get_attendance_report(emp['emp_id'], 
                                                      start_date, end_date)
                data['employees'].append({
                    'emp_id': emp['emp_id'],
                    'name': emp['name'],
                    'department': emp['department'],
                    'attendance': report
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"✅ Monthly report exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting monthly JSON: {str(e)}")
            return ""