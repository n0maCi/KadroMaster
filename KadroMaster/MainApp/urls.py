from django.urls import path
from MainApp.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', profile_hr, name="profile"),
    path('login/', auth_hr, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
]