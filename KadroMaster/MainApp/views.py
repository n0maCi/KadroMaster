from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *
from django.db.models import Q, F, Count
from passlib.hash import django_pbkdf2_sha256

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
    jobs = Jobs.objects.all()
    return render(request, 'MainApp/personal.html', {'departments': departments, 'jobs': jobs})