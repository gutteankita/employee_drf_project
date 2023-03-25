from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Employee(models.Model):
    name = models.CharField(max_length=225, unique=True)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
                    ('M', 'Male'),
                    ('F', 'Female'),
                    ('T', 'Transgender'),
                    ]

    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    department = models.CharField(max_length=225)
    salary = models.FloatField()

    def get_salary(self):
        return self.salary

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")

    
