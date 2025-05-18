from django.urls import path
from .views import SubmitQuestion,unsolvedQuestion,unsolvedQuestionDetail,checkByTeacher,contestSubmitQuestion

urlpatterns = [
    path('unsolvedQuestion', unsolvedQuestion.as_view(), name='unsolvedQuestion'),
    path('unsolvedQuestionDetail/<int:id>', unsolvedQuestionDetail.as_view(), name='unsolvedQuestionDetail'),
    path('submitQuestion/<int:id>', SubmitQuestion.as_view(), name='submitQuestion'),
    path('checkByTeacher/<int:id>', checkByTeacher.as_view(), name='checkByTeacher'),
    path('contestSubmitQuestion/<int:id>', contestSubmitQuestion.as_view(), name='contestSubmitQuestion'),

]
