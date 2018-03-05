from django.contrib.auth.models import User
from django.db import models

from utils.settings import CSRF_LENGTH


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=128)
    csrf = models.CharField(max_length=CSRF_LENGTH, default='')


