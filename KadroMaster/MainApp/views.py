from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *
from django.db.models import Q, F, Count, Sum
from django.http import JsonResponse
import random, datetime

def profile_hr(request):
    employeers = Employees.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        if request.GET.get("delete") is not None:
            Employees.objects.filter(id=request.GET.get("delete")).delete()
            return redirect("profile")
        try:
            if request.POST.get('fullname') and request.POST.get('p_number'):
                employeers = Employees.objects.filter(Q(fullname__contains=request.POST.get('fullname')) & Q(personnel_number__contains=request.POST.get('p_number')))
            elif request.POST.get('fullname'):
                employeers = Employees.objects.filter(fullname__contains=request.POST.get('fullname'))
            else:
                employeers = Employees.objects.filter(personnel_number__contains=request.POST.get('p_number'))
        except:
            pass

    return render(request, 'MainApp/main.html', {'employeers': employeers})

def auth_hr(request):
    if request.user.is_authenticated:
        return redirect('profile')

    users = User.objects.filter(password__isnull=False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error_message = "Неправильный пароль!"
                return render(request, 'MainApp/login.html', {'error_message': error_message, 'users': users})

    return render(request, 'MainApp/login.html', {'users': users})

def department_hr(request):
    departments = Departments.objects.annotate(employee_count=Count('jobs__employees')).prefetch_related('jobs_set')
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        if 'add' in request.POST:
            department_new = Departments()
            department_new.title = request.POST.get('title')
            try:
                department_new.save()
            except:
                return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Данный отдел уже существует'})
        elif 'find' in request.POST:
            departments = Departments.objects.filter(title__contains=request.POST.get('title')).annotate(employee_count=Count('jobs__employees')).prefetch_related('jobs_set')
        elif 'delete' in request.GET:
            count_of_jobs = Jobs.objects.filter(departament=Departments.objects.filter(id=request.GET.get("delete")).first()).count()
            if count_of_jobs == 0:
                Departments.objects.filter(id=request.GET.get("delete")).delete()
            else:
                return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Необходимо удалить все должности'})
    return render(request, 'MainApp/department.html', {'departments': departments})

def job_hr(request):
    departments = Departments.objects.all()
    jobs = Jobs.objects.all().prefetch_related('employees_set')
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        if 'add' in request.POST:
            job_new = Jobs()
            job_new.title = request.POST.get('title')
            job_new.salary_per_hour = request.POST.get('salary_per_hour')
            job_new.departament = Departments.objects.filter(id=request.POST.get('departament_id')).first()
            try:
                job_new.save()
            except:
                pass
        elif 'find' in request.POST:
            filter_params = {
            'title__contains': request.POST.get('title'),
            'salary_per_hour__contains': request.POST.get('salary_per_hour'),
            'departament_id': request.POST.get('departament_id'),
            }
            filter_params = {k: v for k, v in filter_params.items() if v is not None}
            jobs = Jobs.objects.filter(**filter_params).prefetch_related('employees_set')
        elif 'delete' in request.GET:
            Jobs.objects.filter(Q(id=request.GET.get("delete"))).delete()
    return render(request, 'MainApp/job.html', {'departments': departments, 'jobs': jobs})

def password_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'MainApp/password.html', {'form': form})

def personal_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    departments = Departments.objects.all()

    if request.method == 'POST':
        form = AddEmployee(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            if request.POST['military_ticket']:
                db.military_ticket = request.POST['military_ticket']
            db.personnel_number = random.randint(100000,999999)
            db.save()
    return render(request, 'MainApp/personal.html', {'departments': departments})

def get_job_titles(request):
    department_id = request.GET.get('department')
    if department_id:
        jobs = Jobs.objects.filter(departament_id=department_id)
    else:
        jobs = Jobs.objects.none()
    
    data = [{'id': job.id, 'title': job.title} for job in jobs]
    return JsonResponse(data, safe=False)

def time_tracking_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    employeers = Employees.objects.all()
    time_tracking = TimeTraking.objects.all()
    if request.method == 'POST':
        if 'add' in request.POST:
            time_tracking_new = TimeTraking()
            time_tracking_new.date = request.POST.get('date')
            time_tracking_new.amount = request.POST.get('amount')
            time_tracking_new.employee = Employees.objects.filter(id=request.POST.get('employee')).first()
            try:
                time_tracking_new.save()
            except:
                pass
        elif 'find' in request.POST:
            filter_params = {
            'date': request.POST.get('date'),
            'amount': request.POST.get('amount'),
            'employee_id': request.POST.get('employee'),
            }
            filter_params = {k: v for k, v in filter_params.items() if v is not None and v != ''}
            time_tracking = TimeTraking.objects.filter(**filter_params)
        elif 'delete' in request.GET:
            TimeTraking.objects.filter(id=request.GET.get("delete")).delete()
    return render(request, 'MainApp/time_tracking.html', {'employeers': employeers, 'time_tracking': time_tracking})

def info_personal_hr(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    departments = Departments.objects.all()
    employee = Employees.objects.filter(id=id).first()
    if request.method == 'POST':
        if 'new' in request.POST:
            if request.POST.get('job') is not None:
                employee.job = Jobs.objects.filter(id=request.POST.get('job')).first()
            employee.fullname = request.POST.get('fullname')
            employee.birthday = request.POST.get('birthday')
            employee.gender = request.POST.get('gender')
            employee.phone = request.POST.get('phone')
            employee.residence_address = request.POST.get('residence_address')
            employee.passport = request.POST.get('passport')
            employee.insurance_number = request.POST.get('insurance_number')
            employee.individual_tax_number = request.POST.get('individual_tax_number')
            employee.work_book_number = request.POST.get('work_book_number')
            employee.military_ticket = request.POST.get('military_ticket')
            employee.email = request.POST.get('email')
            employee.employment_date = request.POST.get('employment_date')
            employee.save()
            return redirect("info-personal", id=id)
    return render(request, 'MainApp/info_personal.html', {'departments': departments, 'employee': employee})

def salary_hr(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    salaries = Salary.objects.filter(employee=id)
    if request.POST:
        if 'add' in request.POST:
            if request.POST.get('from') > request.POST.get('before'):
                return render(request, 'MainApp/report_salary.html', {'salaries': salaries, 'error': 'Период с не должен превышать периода до'})
            else:
                employee_salary_hour = Employees.objects.filter(id=id).first().job.salary_per_hour
                employee_amount_hours = TimeTraking.objects.filter(employee=id, date__range=(request.POST.get('from'), request.POST.get('before'))).aggregate(Sum('amount'))['amount__sum']
                employee_final_salary = employee_salary_hour * employee_amount_hours
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                Salary.objects.create(salary_date=current_date, number_of_hours_worked=employee_amount_hours, final_salary=employee_final_salary, employee=Employees.objects.filter(id=id).first())
    return render(request, 'MainApp/report_salary.html', {'salaries': salaries})