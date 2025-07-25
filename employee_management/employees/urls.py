from django.urls import path

urlpatterns = [
    # Define your employee management URLs here
    path('employees/', include('employees.urls')),
]