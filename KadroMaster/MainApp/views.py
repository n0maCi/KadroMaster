from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *
from django.db.models import Q

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
    departments = Departments.objects.all()
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
            departments = Departments.objects.filter(title__contains=request.POST.get('title'))
        elif 'delete' in request.GET:
            delete_department = Departments.objects.filter(Q(id=request.GET.get("delete")) & Q(amount_jobs=0) & Q(amount_employees=0)).delete()
            if delete_department[0] == 0:
                delete_department = Departments.objects.filter(id=request.GET.get("delete")).first()
                if delete_department.amount_jobs != 0:
                    return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Количество должностей больше 0'})
                elif delete_department.amount_employees != 0:
                    return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Количество сотрудников больше 0'})
            return redirect('department')
    return render(request, 'MainApp/department.html', {'departments': departments})

def job_hr(request):
    departments = Departments.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'MainApp/job.html', {'departments': departments})