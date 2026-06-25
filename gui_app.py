import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from modules.database import AttendanceDatabase
from modules.csv_handler import CSVHandler
from modules.reports import ReportGenerator
from modules.validation import InputValidator

class AttendanceGUI:
    """Tkinter GUI for Attendance Management System"""
    
    def __init__(self, root):
        """Initialize GUI"""
        self.root = root
        self.root.title("🐍 Attendance Management System")
        self.root.geometry("1000x700")
        
        self.db = AttendanceDatabase()
        self.csv_handler = CSVHandler()
        self.report_gen = ReportGenerator()
        self.validator = InputValidator()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.mark_tab = ttk.Frame(self.notebook)
        self.employee_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.mark_tab, text="Mark Attendance")
        self.notebook.add(self.employee_tab, text="Employees")
        self.notebook.add(self.view_tab, text="View Records")
        self.notebook.add(self.reports_tab, text="Reports")
        
        self.setup_mark_tab()
        self.setup_employee_tab()
        self.setup_view_tab()
        self.setup_reports_tab()
    
    def setup_mark_tab(self):
        """Setup Mark Attendance tab"""
        frame = ttk.LabelFrame(self.mark_tab, text="Mark Attendance", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Employee ID
        ttk.Label(frame, text="Employee ID:").grid(row=0, column=0, sticky=tk.W)
        self.emp_id_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.emp_id_var, width=20).grid(row=0, column=1)
        
        # Date
        ttk.Label(frame, text="Date:").grid(row=1, column=0, sticky=tk.W)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(frame, textvariable=self.date_var, width=20).grid(row=1, column=1)
        
        # Status
        ttk.Label(frame, text="Status:").grid(row=2, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="Present")
        ttk.Combobox(frame, textvariable=self.status_var, 
                    values=["Present", "Absent", "Late"], width=20).grid(row=2, column=1)
        
        # Remarks
        ttk.Label(frame, text="Remarks:").grid(row=3, column=0, sticky=tk.W)
        self.remarks_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.remarks_var, width=20).grid(row=3, column=1)
        
        # Button
        ttk.Button(frame, text="Mark Attendance", 
                  command=self.mark_attendance).grid(row=4, column=0, columnspan=2, pady=20)
    
    def mark_attendance(self):
        """Mark attendance"""
        emp_id = self.emp_id_var.get().strip().upper()
        date = self.date_var.get().strip()
        status = self.status_var.get()
        remarks = self.remarks_var.get().strip()
        
        # Validation
        is_valid, msg = self.validator.validate_emp_id(emp_id)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        is_valid, msg = self.validator.validate_date(date)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        employee = self.db.get_employee(emp_id)
        if not employee:
            messagebox.showerror("Error", f"Employee {emp_id} not found!")
            return
        
        if self.db.mark_attendance(emp_id, employee['name'], date, status, remarks):
            messagebox.showinfo("Success", "Attendance marked successfully!")
            self.remarks_var.set("")
        else:
            messagebox.showerror("Error", "Failed to mark attendance!")
    
    def setup_employee_tab(self):
        """Setup Employee Management tab"""
        frame = ttk.Frame(self.employee_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add employee frame
        add_frame = ttk.LabelFrame(frame, text="Add Employee", padding=10)
        add_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(add_frame, text="Emp ID:").grid(row=0, column=0)
        self.new_emp_id = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_emp_id, width=20).grid(row=0, column=1)
        
        ttk.Label(add_frame, text="Name:").grid(row=1, column=0)
        self.new_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_name, width=20).grid(row=1, column=1)
        
        ttk.Label(add_frame, text="Email:").grid(row=2, column=0)
        self.new_email = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_email, width=20).grid(row=2, column=1)
        
        ttk.Label(add_frame, text="Department:").grid(row=3, column=0)
        self.new_dept = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_dept, width=20).grid(row=3, column=1)
        
        ttk.Button(add_frame, text="Add Employee", 
                  command=self.add_employee).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Employee list frame
        list_frame = ttk.LabelFrame(frame, text="Employees", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        self.emp_tree = ttk.Treeview(list_frame, columns=('ID', 'Name', 'Email', 'Dept'), height=15)
        self.emp_tree.column('#0', width=0)
        self.emp_tree.column('ID', width=80)
        self.emp_tree.column('Name', width=150)
        self.emp_tree.column('Email', width=200)
        self.emp_tree.column('Dept', width=150)
        
        self.emp_tree.heading('#0', text='')
        self.emp_tree.heading('ID', text='Emp ID')
        self.emp_tree.heading('Name', text='Name')
        self.emp_tree.heading('Email', text='Email')
        self.emp_tree.heading('Dept', text='Department')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscroll=scrollbar.set)
        
        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        ttk.Button(frame, text="Refresh", command=self.refresh_employees).pack()
        
        self.refresh_employees()
    
    def add_employee(self):
        """Add new employee"""
        emp_id = self.new_emp_id.get().strip().upper()
        name = self.new_name.get().strip()
        email = self.new_email.get().strip()
        dept = self.new_dept.get().strip()
        
        if self.db.add_employee(emp_id, name, email, dept):
            messagebox.showinfo("Success", "Employee added!")
            self.new_emp_id.set("")
            self.new_name.set("")
            self.new_email.set("")
            self.new_dept.set("")
            self.refresh_employees()
        else:
            messagebox.showerror("Error", "Failed to add employee!")
    
    def refresh_employees(self):
        """Refresh employee list"""
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        employees = self.db.get_all_employees()
        for emp in employees:
            self.emp_tree.insert('', tk.END, values=(
                emp['emp_id'], emp['name'], emp['email'], emp['department']
            ))
    
    def setup_view_tab(self):
        """Setup View Records tab"""
        frame = ttk.Frame(self.view_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(frame, text="Filter Records", padding=10)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Emp ID:").grid(row=0, column=0)
        self.filter_emp = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_emp, width=20).grid(row=0, column=1)
        
        ttk.Button(filter_frame, text="Filter", 
                  command=self.filter_records).grid(row=0, column=2, padx=10)
        
        # Records frame
        records_frame = ttk.LabelFrame(frame, text="Records", padding=10)
        records_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.rec_tree = ttk.Treeview(records_frame, 
                                    columns=('Date', 'Emp ID', 'Name', 'Status', 'Remarks'),
                                    height=20)
        self.rec_tree.column('#0', width=0)
        for col in ('Date', 'Emp ID', 'Name', 'Status', 'Remarks'):
            self.rec_tree.column(col, width=100)
            self.rec_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.rec_tree.yview)
        self.rec_tree.configure(yscroll=scrollbar.set)
        
        self.rec_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def filter_records(self):
        """Filter and display records"""
        emp_id = self.filter_emp.get().strip().upper()
        
        if not emp_id:
            messagebox.showwarning("Warning", "Enter Employee ID!")
            return
        
        for item in self.rec_tree.get_children():
            self.rec_tree.delete(item)
        
        records = self.db.get_attendance_by_emp_id(emp_id)
        
        if not records:
            messagebox.showinfo("Info", f"No records found for {emp_id}")
            return
        
        for rec in records:
            self.rec_tree.insert('', tk.END, values=(
                rec['date'], rec['emp_id'], rec['name'], rec['status'], rec['remarks'] or ''
            ))
    
    def setup_reports_tab(self):
        """Setup Reports tab"""
        frame = ttk.LabelFrame(self.reports_tab, text="Generate Reports", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Employee ID:").grid(row=0, column=0)
        self.rep_emp = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rep_emp, width=20).grid(row=0, column=1)
        
        ttk.Label(frame, text="Start Date:").grid(row=1, column=0)
        self.rep_start = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rep_start, width=20).grid(row=1, column=1)
        
        ttk.Label(frame, text="End Date:").grid(row=2, column=0)
        self.rep_end = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rep_end, width=20).grid(row=2, column=1)
        
        ttk.Label(frame, text="Format:").grid(row=3, column=0)
        self.rep_format = tk.StringVar(value="CSV")
        ttk.Combobox(frame, textvariable=self.rep_format, 
                    values=["CSV", "JSON", "TXT"], width=20).grid(row=3, column=1)
        
        ttk.Button(frame, text="Generate Report", 
                  command=self.generate_report).grid(row=4, column=0, columnspan=2, pady=20)
    
    def generate_report(self):
        """Generate attendance report"""
        emp_id = self.rep_emp.get().strip().upper()
        start = self.rep_start.get().strip()
        end = self.rep_end.get().strip()
        fmt = self.rep_format.get().lower()
        
        if not all([emp_id, start, end]):
            messagebox.showwarning("Warning", "Fill all fields!")
            return
        
        is_valid, msg = self.validator.validate_date_range(start, end)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return
        
        filename = self.report_gen.generate_individual_report(emp_id, start, end, fmt)
        
        if filename:
            messagebox.showinfo("Success", f"Report saved: {filename}")
        else:
            messagebox.showerror("Error", "Failed to generate report!")


def run_gui():
    """Run GUI application"""
    root = tk.Tk()
    gui = AttendanceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()