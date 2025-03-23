from django.shortcuts import render, redirect
from MainApp.models import *

def profile_hr(request):
    return render(request, 'MainApp/main.html')