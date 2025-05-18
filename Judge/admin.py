from django.contrib import admin
from .models import Submissions,Contest,Contester,ContestSubmissions
# Register your models here.
admin.site.register([Submissions,Contest,ContestSubmissions,Contester])