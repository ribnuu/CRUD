from django.contrib import admin
from django.utils.html import format_html
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'image_tag', 'first_name', 'last_name', 
        'email', 'mobile', 'status', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'nic', 'mobile']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 25

    fieldsets = (
        ('Personal Information', {
            'fields': ('employee_image', 'first_name', 'last_name', 'dob', 'nic', 'passport')
        }),
        ('Contact Information', {
            'fields': ('email', 'mobile', 'telephone', 'address')
        }),
        ('Status & Remarks', {
            'fields': ('status', 'remarks')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_tag(self, obj):
        if obj.employee_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.employee_image.url)
        return "No Image"
    image_tag.short_description = 'Photo'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['nic']  # Make NIC readonly when editing
        return self.readonly_fields