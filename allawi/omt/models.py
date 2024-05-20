from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.db import models

POSITIONS = [
    ('member', 'MR'),
    ('Manager', 'M'),
    ('Assistant Manager', 'AM'),
    ('Supervisor', 'S'),
    ('Team Lead', 'TL'),
    ('Software Engineer', 'SE'),
    ('Quality Assurance Engineer', 'QAE'),
    ('Data Analyst', 'DA'),
    ('Project Manager', 'PM'),
    ('Sales Representative', 'SR'),
    ('Marketing Specialist', 'MS'),
    ('Human Resources Coordinator', 'HRC'),
    ('Accountant', 'AT'),
    ('Financial Analyst', 'FA'),
    ('Customer Support Representative', 'CSR'),
    ('Administrative Assistant', 'AA'),
]
class Customer(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="akdikor@gmail.com")
    worth = models.IntegerField()

    def __str__(self):
        return self.name.username

class Employee(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    experience_years = models.IntegerField()
    date_employed = models.DateField()
    position = models.CharField(max_length=100, choices=POSITIONS, default="MR")
    salary = models.IntegerField(default=0)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    report = models.TextField()  # Add the report field

    def __str__(self):
        return self.name.username

    def login(self):
        current_time = timezone.localtime(timezone.now()) + timezone.timedelta(hours=3)
        self.login_time = current_time
        self.save()

    def logout(self):
        if self.login_time:
            current_time = timezone.localtime(timezone.now()) + timezone.timedelta(hours=3)
            self.logout_time = current_time
            elapsed_time = self.logout_time - self.login_time
            self.login_time = None
            self.save()
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        return None

class EmployeeCV(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    experience = models.IntegerField()
    education = models.TextField()
    profile = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return f"Wallet of {self.user.name.username}"

class Transaction(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    amount = models.IntegerField()

    status = models.CharField(max_length=10, default='SENT')
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now() + timedelta(hours=3))
    #email = models.EmailField()


    def str(self):
        return f"Transaction Email: {self.email} - Status: {self.status}"

class Appointment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def str(self):
        return self.title





# Create your models here.
