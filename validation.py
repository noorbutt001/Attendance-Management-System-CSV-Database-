import re
from datetime import datetime
from typing import Tuple

class InputValidator:
    """Input validation for attendance system"""
    
    @staticmethod
    def validate_emp_id(emp_id: str) -> Tuple[bool, str]:
        """Validate employee ID format"""
        if not emp_id:
            return False, "Employee ID cannot be empty"
        
        if len(emp_id) > 20:
            return False, "Employee ID too long (max 20 characters)"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', emp_id):
            return False, "Employee ID can only contain letters, numbers, hyphens, and underscores"
        
        return True, "Valid"
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate employee name"""
        if not name or len(name.strip()) == 0:
            return False, "Name cannot be empty"
        
        if len(name) > 100:
            return False, "Name too long (max 100 characters)"
        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False, "Name can only contain letters and spaces"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        if not email:
            return True, "Email is optional"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Valid"
        except ValueError:
            return False, "Invalid date format (use YYYY-MM-DD)"
    
    @staticmethod
    def validate_status(status: str) -> Tuple[bool, str]:
        """Validate attendance status"""
        valid_statuses = ['Present', 'Absent', 'Late']
        if status not in valid_statuses:
            return False, f"Status must be one of: {', '.join(valid_statuses)}"
        return True, "Valid"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """Validate date range"""
        valid_start, msg_start = InputValidator.validate_date(start_date)
        valid_end, msg_end = InputValidator.validate_date(end_date)
        
        if not valid_start:
            return False, msg_start
        if not valid_end:
            return False, msg_end
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            return False, "Start date must be before end date"
        
        return True, "Valid"