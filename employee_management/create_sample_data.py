from employees.models import Employee
from datetime import date

# Create sample employees
sample_employees = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'dob': date(1990, 5, 15),
        'nic': '199012345678',
        'email': 'john.doe@email.com',
        'mobile': '+94771234567',
        'address': '123 Main Street, Colombo',
        'status': 'active'
    },
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'dob': date(1985, 8, 22),
        'nic': '198523456789',
        'email': 'jane.smith@email.com',
        'mobile': '+94771234568',
        'address': '456 Oak Avenue, Kandy',
        'status': 'active'
    },
    {
        'first_name': 'Mike',
        'last_name': 'Johnson',
        'dob': date(1992, 12, 3),
        'nic': '199234567890',
        'email': 'mike.johnson@email.com',
        'mobile': '+94771234569',
        'address': '789 Pine Road, Galle',
        'status': 'inactive'
    }
]

for emp_data in sample_employees:
    Employee.objects.create(**emp_data)

print("Sample data created successfully!")