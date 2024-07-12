from django.db import models
from django.contrib.auth.models import AbstractUser
from countries.models import Country

class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.ManyToManyField(
        Country,
        related_name= 'users',
    blank=True)