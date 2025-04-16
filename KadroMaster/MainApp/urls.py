from django.urls import path
from MainApp.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', profile_hr, name="profile"),
    path('login/', auth_hr, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('department/', department_hr, name="department"),
    path('job/', job_hr, name="job"),
    path('change-password/', password_hr, name="password"),
    path('personal/', personal_hr, name="personal"),
    path('api/job-titles/', get_job_titles, name='get_job_titles'),
]