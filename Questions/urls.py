from django.urls import path
from .views import question,add_question

# urlpatterns = [
#     # path('', views.loginpage , name=''),
#     # path('teacher/home',views.teacherIndex , name='TeacherIndex'),
#     # path('login',views.logins , name='login')
#     path('login/', CustomLoginView.as_view(), name='login'),
# ]
urlpatterns = [
    path('questions/', question.as_view()  , name='questions'),
    path('add_question/', add_question.as_view()  , name='addquestion'),

]
