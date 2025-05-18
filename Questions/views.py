from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .models import Question,Course
from .forms import QuestionForm
from Judge.models import Contester,Contest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.

class question(View):
    def get(self,request):
        q = Question.objects.filter(creator = request.user )
        return render(request,'teacher/questions.html',{'context':q})
    
from persiantools.jdatetime import JalaliDateTime

class add_question(View):
    def get(self,request):
        course = Course.objects.all()
        return render(request,'teacher/addquestion.html',{'context':course})
    def post(self,request,*args,**kwargs):
        jalali_date = JalaliDateTime.strptime("1404/02/17 09:14:00", "%Y/%m/%d %H:%M:%S")
        gregorian_date = jalali_date.to_gregorian()

        a = Question.objects.create(title = request.POST.get('title'), description = request.POST.get('description'), input_form = request.POST.get('inputs'),
                               output_form = request.POST.get('outputs'),question_file =request.FILES['file'] ,timelimit = request.POST.get('timelimit'),
                                inputs_file = request.FILES['file-input'] , outputs_file = request.FILES['file-output'] , language = request.POST.get('language'),
                                 deadline = gregorian_date , score = request.POST.get('score'), 
                                 course = Course.objects.get(id=request.POST.get('course')),creator = request.user )
        return redirect('addquestion')
    

class submit_question(View):
    pass


import string
from django.db.models import Count, Q

class contest(View,LoginRequiredMixin):
    def get(self,request):
        print()
        if not Contester.objects.filter(user=request.user):
            messages.warning(request,"شما عضو هیچ مسابقه ای نیستید .")
            return redirect('student_home')
        contesters = Contester.objects.annotate(true_result_count=Count('questions',filter=Q(questions__icontains='"result": true'))).order_by('-true_result_count', '-score', 'penalty')
        for index, contester in enumerate(contesters, start=1):
            contester.rank = index 
        numberOfQuestions = Contest.objects.get(id=1).questions.count()
        letters = list(string.ascii_uppercase[:numberOfQuestions])
        return render(request,'contest/ContestPage.html',{'contesters':contesters,'letters':letters})

class contestQuestions(View,LoginRequiredMixin):
    def get(self,request):
        questions = Contest.objects.get(id=1).questions.all()
        return render(request,'contest/questions.html',{'questions':questions})

class logoutContest(View,LoginRequiredMixin):
    def get(self,request):
        return redirect('student_home')

