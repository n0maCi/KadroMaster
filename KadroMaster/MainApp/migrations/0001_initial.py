# Generated by Django 5.1.7 on 2025-05-14 20:00

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('personnel_number', models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6)])),
                ('gender', models.CharField(choices=[('m', 'm'), ('f', 'f')], max_length=1)),
                ('birthday', models.DateField()),
                ('residence_address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100, null=True)),
                ('employment_date', models.DateField()),
                ('passport', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('individual_tax_number', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12)])),
                ('insurance_number', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
                ('work_book_number', models.CharField(max_length=7, validators=[django.core.validators.MinLengthValidator(7)])),
                ('military_ticket', models.CharField(max_length=7, null=True, validators=[django.core.validators.MinLengthValidator(7)])),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('access_for_emplyees', models.IntegerField(default=0)),
                ('access_for_departments', models.IntegerField(default=0)),
                ('access_for_jobs', models.IntegerField(default=0)),
                ('access_for_reports', models.IntegerField(default=0)),
                ('access_for_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('state', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('salary_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('departament', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.departments')),
            ],
        ),
        migrations.AddField(
            model_name='employees',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.jobs'),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_date', models.DateField()),
                ('number_of_hours_worked', models.CharField(max_length=20)),
                ('final_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.employees')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTraking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.employees')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.employees')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.groups')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
