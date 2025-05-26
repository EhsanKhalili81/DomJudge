from django.urls import path
from .views import question,add_question,contest,editQuestion,download_question_file,contestQuestions,logoutContest,addContest,questionDetail,solvedQuestion,solvedQuestionsDetails,download_file

# urlpatterns = [
#     # path('', views.loginpage , name=''),
#     # path('teacher/home',views.teacherIndex , name='TeacherIndex'),
#     # path('login',views.logins , name='login')
#     path('login/', CustomLoginView.as_view(), name='login'),
# ]
urlpatterns = [
    path('questions/', question.as_view()  , name='questions'),
    path('add_question/', add_question.as_view()  , name='addquestion'),
    path('contest/', contest.as_view()  , name='contest'),
    path('contestQuestions/', contestQuestions.as_view()  , name='contestQuestions'),
    path('logoutContest/', logoutContest.as_view()  , name='logoutContest'),
    path('addContest/', addContest.as_view()  , name='addContest'),
    path('solvedQuestion/', solvedQuestion.as_view()  , name='solvedQuestion'),
    path('solvedQuestionsDetails/<int:id>', solvedQuestionsDetails.as_view()  , name='solvedQuestionsDetails'),
    path('download/<int:pk>/', download_file, name='download'),
    path('questionfile/<int:pk>/', download_question_file, name='questionfile'),
    path('questionDetail/<int:id>', questionDetail.as_view(), name='questionDetail'),
    path('editQuestion/<int:id>', editQuestion.as_view(), name='editQuestion'),





]
