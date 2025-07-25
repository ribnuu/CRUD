from django.db import models

class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    
    employee_image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    nic = models.CharField(max_length=20, unique=True)
    passport = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.nic})"