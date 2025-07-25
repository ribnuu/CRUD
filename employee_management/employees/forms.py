# employees/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_image', 'first_name', 'last_name', 'dob',
            'nic', 'passport', 'mobile', 'telephone', 'email',
            'address', 'status', 'remarks'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter NIC number'
            }),
            'passport': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter passport number'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter telephone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter remarks (optional)'
            }),
            'employee_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existing = Employee.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Employee with this email already exists.')
        return email
    
    def clean_nic(self):
        nic = self.cleaned_data.get('nic')
        if nic:
            existing = Employee.objects.filter(nic=nic)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Employee with this NIC already exists.')
        return nic

class EmployeeSearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('employee_id', 'Employee ID'),
        ('name', 'Name'),
        ('nic', 'NIC Number'),
        ('email', 'Email'),
        ('status', 'Status'),
    ]
    
    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search_query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter search term'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_type'].label = 'Search By'
        self.fields['search_query'].label = 'Search Term'