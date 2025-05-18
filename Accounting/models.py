from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('0', 'Teacher'),
        ('1', 'Student'),
    )
    
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='student')
    mobilephone = models.CharField(max_length=15, blank=True, null=True)
    nationalcode = models.CharField(max_length=10,blank=True) 

    # def __str__(self):
    #     return self.username