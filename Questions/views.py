from django.shortcuts import render,HttpResponse
from django.views import View
from .models import Question
from .forms import QuestionForm
# Create your views here.

class question(View):
    def get(self,request):
        q = Question.objects.filter(creator = request.user )
        return render(request,'teacher/questions.html',{'context':q})
    

class add_question(View):
    def get(self,request):
        form = QuestionForm()
        return render(request,'teacher/addquestion.html',{'form':form})
    def post(self,request,*args,**kwargs):
        print(request.POST)
        return HttpResponse("ygdsfhdsgfdshjfdsgfds")
    

class submit_question(View):
    pass
