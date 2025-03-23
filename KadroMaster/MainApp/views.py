from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *

def profile_hr(request):
    return render(request, 'MainApp/main.html')

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
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
            else:
                error_message = "Неправильный пароль!"
                return render(request, 'MainApp/login.html', {'form': form, 'error_message': error_message, 'users': users})
    else:
        form = LoginForm()
    return render(request, 'MainApp/login.html', {'form': form, 'users': users})