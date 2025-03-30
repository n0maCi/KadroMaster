from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    password = models.CharField(("password"), max_length=128)
    username = models.CharField(max_length=150, unique=True)

class Employees(models.Model):
    male = 'm'
    female = 'f'
    genders = (
        (male, male),
        (female, female),
    )
    fullname = models.CharField(max_length=150)
    personnel_number = models.CharField(max_length=6, validators=[MinLengthValidator(6)], unique=True)
    gender = models.CharField(max_length=1, choices=genders)
    birthday = models.DateField()
    residence_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100, null=True)
    employment_date = models.DateField()
    passport = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    individual_tax_number = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    insurance_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    work_book_number = models.CharField(max_length=7, validators=[MinLengthValidator(7)])
    military_ticket = models.CharField(max_length=7, validators=[MinLengthValidator(7)], null=True)

class Departments(models.Model):
    title = models.CharField(max_length=150, unique=True)
    amount_jobs = models.IntegerField(default=0)

class Jobs(models.Model):
    title = models.CharField(max_length=150)
    salary_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)
    departament = models.ForeignKey(Departments, on_delete=models.DO_NOTHING)

class TimeTraking(models.Model):
    date = models.DateField()
    amount = models.IntegerField()
    employee = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)

class Salary(models.Model):
    salary_date = models.DateField()
    number_of_hours_worked = models.CharField(max_length=20)
    final_salary = models.DecimalField(max_digits=10, decimal_places=2)
    employee = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)