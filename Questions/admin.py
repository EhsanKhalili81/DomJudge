from django.contrib import admin
from .models import Course,Question

# Register your models here.
admin.site.register([Course,Question])