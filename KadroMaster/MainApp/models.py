from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    password = models.CharField(("password"), max_length=128, null=True)
    username = models.CharField(max_length=150, null=True, unique=True)