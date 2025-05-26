from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views import View
from .utils import send_file,contest_send_file
from Questions.models import Question
from .models import Submissions,Contester
from django.contrib import messages

# Create your views here.


class unsolvedQuestion(View):
    def get(self,request):
        # questions = Question.objects.all()
        questions = Question.objects.exclude(id__in=Submissions.objects.filter(student=request.user).values_list("question_id", flat=True))
        # questions = Question.objects.all()
        return render(request,'student\questions.html',{'context':questions})
    

class unsolvedQuestionDetail(View):
    def post(self,request,id):
        question = get_object_or_404(Question,id=id)
        submission = Submissions.objects.filter(student = request.user , question = question).count()
        if submission < int(question.allowed_number):
        # send_file(question.question_file.path, question.inputs_file.path,question.outputs_file.path,{"user_id": question.creator.id, "file_type": "pdf", "action": "compile"})
            return render(request,'student\questionDetail.html',{'context':question})
        else:
            messages.warning(request,"تعداد دفعات مجاز شما به پایان رسیده است")
            return redirect('student_home')


from django.utils.timezone import now
class SubmitQuestion(View):
    def post(self,request,id):
        question = get_object_or_404(Question,id=id)
        submissions = Submissions.objects.filter(student = request.user ,question = question ).count()
        if now() <= question.deadline :
            if submissions < question.allowed_number :
                solution = request.FILES.get('solution')
                submit =  Submissions.objects.create(student = request.user,question = question , solution_file = solution)
                send_file(submit.solution_file.path, question.inputs_file.path,question.outputs_file.path,{"user_id": question.creator.id,"submission_id":submit.id ,"lang": f"{question.language}", "timelimit": question.timelimit})
                messages.success(request, "فایل ارسال شد")
            else:
                messages.warning(request, "تعداد دفعات مجاز برای ارسال به اتمام رسیده است .")
        else:
            messages.warning(request, "مهلت ارسال پاسخ به پایان رسیده است.")
        return redirect('student_home')
        
    
class checkByTeacher(View):
    def post(self,request,id):
        submission = Submissions.objects.get(id=id)
        submission.is_Checked = True
        submission.save()
        messages.success(request, "تایید شد .")
        return redirect('teacher_home')
    
class contestSubmitQuestion(View):
    def post(self,request,id):
        question = get_object_or_404(Question,id=id)
        # print("--------------",request.user)
        contester = Contester.objects.get(user=request.user)
        solution = request.FILES.get("solution")
        language = request.POST.get("lang")
        # print("adasdasdasd",solution,language)
        if now() <= question.deadline:
            submit =  Submissions.objects.create(student = request.user,question = question , solution_file = solution, is_compiled = True,is_Checked=True,is_contest = True)
            print(submit)
            contest_send_file(submit.solution_file.path, question.inputs_file.path,question.outputs_file.path,{"contester_id": contester.id,"question_id":question.id ,"lang": f"{language}", "timelimit": question.timelimit})
            messages.success(request, "فایل ارسال شد")
        else:
            messages.warning(request, "مهلت ارسال پاسخ به پایان رسیده است.")
        return redirect('contest')
