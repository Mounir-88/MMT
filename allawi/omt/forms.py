from django import forms
from .models import *

from django import forms
from .models import EmployeeCV

class EmployeeCVForm(forms.ModelForm):
    class Meta:
        model = EmployeeCV
        fields = ['name', 'email', 'password', 'experience', 'education', 'profile']


class CVReviewForm(forms.ModelForm):
    class Meta:
        model = EmployeeCV
        fields = ['is_accepted']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['position', 'salary', 'report']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'report': forms.TextInput(attrs={'class': 'form-control'})
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'description', 'date', 'time']  # Add more fields as needed

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }