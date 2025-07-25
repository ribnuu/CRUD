from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from io import BytesIO
from .models import Employee
from .forms import EmployeeForm, EmployeeSearchForm

# Helper for full name (add to model if you prefer)
def get_full_name(employee):
    return f"{employee.first_name} {employee.last_name}"

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = Employee.objects.count()
        context['active_employees'] = Employee.objects.filter(status='active').count()
        context['inactive_employees'] = Employee.objects.filter(status='inactive').count()
        context['search_form'] = EmployeeSearchForm()
        return context

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employee created successfully!')
        return super().form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully!')
        return super().form_valid(form)

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Employee deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def employee_search(request):
    employees = Employee.objects.none()
    search_form = EmployeeSearchForm()

    if request.method == 'GET' and 'search_query' in request.GET:
        search_form = EmployeeSearchForm(request.GET)
        if search_form.is_valid():
            search_type = search_form.cleaned_data['search_type']
            search_query = search_form.cleaned_data['search_query']

            if search_type == 'employee_id':
                employees = Employee.objects.filter(id=search_query)  # Use 'id' unless you have employee_id
            elif search_type == 'name':
                employees = Employee.objects.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            elif search_type == 'nic':
                employees = Employee.objects.filter(nic__icontains=search_query)
            elif search_type == 'email':
                employees = Employee.objects.filter(email__icontains=search_query)
            elif search_type == 'status':
                employees = Employee.objects.filter(status__icontains=search_query)

    context = {
        'employees': employees,
        'search_form': search_form,
        'search_performed': 'search_query' in request.GET
    }
    return render(request, 'employees/employee_search.html', context)

@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Employees'

    # Headers
    headers = [
        'Employee ID', 'First Name', 'Last Name', 'DOB', 'NIC',
        'Passport', 'Mobile', 'Telephone', 'Email', 'Address', 'Status', 'Remarks'
    ]
    worksheet.append(headers)

    # Data
    employees = Employee.objects.all().order_by('id')
    for employee in employees:
        worksheet.append([
            employee.id,  # Use 'id' unless you have employee_id
            employee.first_name,
            employee.last_name,
            employee.dob.strftime('%Y-%m-%d') if employee.dob else '',
            employee.nic,
            employee.passport or '',
            employee.mobile,
            employee.telephone or '',
            employee.email,
            employee.address,
            employee.get_status_display(),
            employee.remarks or ''
        ])

    workbook.save(response)
    return response

@login_required
def export_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("Employee Report", styles['Title'])
    elements.append(title)

    # Table data
    data = [['ID', 'Name', 'NIC', 'Email', 'Mobile', 'Status']]
    employees = Employee.objects.all().order_by('id')
    for employee in employees:
        data.append([
            str(employee.id),  # Use 'id' unless you have employee_id
            get_full_name(employee),
            employee.nic,
            employee.email,
            employee.mobile,
            employee.get_status_display()
        ])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'
    return response

@login_required
def dashboard(request):
    context = {
        'total_employees': Employee.objects.count(),
        'active_employees': Employee.objects.filter(status='active').count(),
        'inactive_employees': Employee.objects.filter(status='inactive').count(),
        'recent_employees': Employee.objects.order_by('-created_at')[:5]
    }
    return render(request, 'employees/dashboard.html', context)