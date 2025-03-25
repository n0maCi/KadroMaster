from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *

def profile_hr(request):
    employeers = Employees.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
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