from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.views import View
from .models import Question,Course
from .forms import QuestionForm
from Judge.models import Contester,Contest,Submissions
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
        jalali_date = JalaliDateTime.strptime(str(request.POST.get('deadline')), "%Y/%m/%d %H:%M:%S")
        gregorian_date = jalali_date.to_gregorian()

        a = Question.objects.create(title = request.POST.get('title'), description = request.POST.get('description'), input_form = request.POST.get('inputs'),
                               output_form = request.POST.get('outputs'),question_file =request.FILES.get('file') ,timelimit = request.POST.get('timelimit'),
                                inputs_file = request.FILES['file-input'] , outputs_file = request.FILES['file-output'] , language = request.POST.get('language'),
                                 deadline = gregorian_date , score = request.POST.get('score'), 
                                 course = Course.objects.get(id=request.POST.get('course')),creator = request.user ,allowed_number = request.POST.get('allowednumber'))
        messages.success(request,"سوال با موفقیت ثبت شد.")
        return redirect('addquestion')
    

class submit_question(View):
    pass


import string
from django.db.models import Count, Q

class contest(View,LoginRequiredMixin):
    def get(self,request):
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
        contester = Contester.objects.get(user=request.user)
        questions = Contest.objects.get(id=contester.contest.id).questions.all()
        return render(request,'contest/questions.html',{'questions':questions})

class logoutContest(View,LoginRequiredMixin):
    def get(self,request):
        return redirect('student_home')
    
class addContest(View):
    def get(self,request):
        questions = Question.objects.all()
        return render(request,'contest/addcontest.html',{'questions':questions})

    def post(self,request):
        title = request.POST.get('title')
        questions = list(map(int,request.POST.getlist('questions')))
        newContest = Contest.objects.create(title = title)
        newContest.questions.set(questions)
        return redirect('addContest')
    

class solvedQuestion(View):
    def get(self,request):
        solved_question = Submissions.objects.filter(student = request.user)
        return render(request,'student/solvedquestion.html',{'context':solved_question})
    

class solvedQuestionsDetails(View):
    def get(self,request,id):
        submission = Submissions.objects.get(id=id)
        return render(request,'teacher/submissionsdetail.html',{'response':submission})
    def post(self,request,id):
        try:
            submission = Submissions.objects.get(id=id)
            submission.score = request.POST.get('score')
            submission.is_Checked = True
            submission.save()
            messages.success(request,"پاسخ تایید شد .")
        except:
            messages.warning(request,"مشکلی پیش آمده است.")
        return redirect('teacher_home')
    
from django.http import FileResponse, Http404
import os
from django.conf import settings

def download_file(request, pk):
    submission = get_object_or_404(Submissions, pk=pk)
    file_path = submission.solution_file.path

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found.")
    
def download_question_file(request,pk):
    question = get_object_or_404(Question, pk=pk)
    file_path = question.question_file.path

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found.")


class questionDetail(View):
    def get(self,request,id):
        context = Question.objects.get(id=id)
        return render(request,"teacher/questiondetail.html",{'context':context})

    def post(self,request,id):
        question = Question.objects.get(id=id)
        question.delete()
        messages.warning(request,"سوال با موفقیت حذف شد.")
        return redirect("questions")

class editQuestion(View):
    def post(self,request,id):
        try:
            jalali_date = JalaliDateTime.strptime(str(request.POST.get('deadline')), "%Y/%m/%d %H:%M:%S")
            gregorian_date = jalali_date.to_gregorian()
            data = request.POST
            question = Question.objects.get(id=id)
            question.title = data.get("title")
            question.description = data.get("description")
            question.input_form = data.get("inputs")
            question.output_form = data.get("outputs")
            question.deadline = gregorian_date
            question.score = data.get("score")
            question.allowed_number = data.get("allowednumber")
            # print("----------------------------",data)
            question.save()
            messages.success(request,"سوال با موفقیت ویرایش شد.")
        except:
            messages.warning(request,"سوال ویرایش نشد")
        return redirect('teacher_home')
