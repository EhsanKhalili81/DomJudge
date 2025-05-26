from django.urls import path
from .views import CustomLoginView,TeacherHomeView,report,StudentHomeView,StudentProfile,Add_User,logout_user,addContester,register_users_from_excel,Users,User_Detail,signUp
from django.contrib.auth.views import LogoutView

# urlpatterns = [
#     # path('', views.loginpage , name=''),
#     # path('teacher/home',views.teacherIndex , name='TeacherIndex'),
#     # path('login',views.logins , name='login')
#     path('login/', CustomLoginView.as_view(), name='login'),
# ]
urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('teacher_home/', TeacherHomeView.as_view(), name='teacher_home'),
    path('student_home/', StudentHomeView.as_view(), name='student_home'),
    path('student_home/profile/', StudentProfile.as_view(), name='profile'),
    path('addUser/', Add_User.as_view(), name='addUser'),
    path('logout/', logout_user, name='logout'),
    path('register_users_from_excel',register_users_from_excel.as_view(),name = 'register_users_from_excel'),
    path('users/',Users.as_view(),name = 'users'),
    path('user_detail/<int:id>',User_Detail.as_view(),name = 'user_detail'),
    path('addContester/',addContester.as_view(),name = 'addContester'),
    path('signUp/',signUp.as_view(),name = 'signUp'),
    path('report/',report.as_view(),name = 'report'),





]
