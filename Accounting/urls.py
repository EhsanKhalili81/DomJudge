from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage , name=''),
    path('teacher/home',views.teacherIndex , name='TeacherIndex'),
    path('login',views.logins , name='login')
]
