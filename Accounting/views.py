from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .models import *
from django.contrib import messages
from Judge.models import Submissions,Contester,Contest,Question
from .permission import student_required,teacher_required



class signUp(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        data = request.POST
        user_exists = CustomUser.objects.filter(username=data.get("studentcode")).exists()
        if user_exists:
            messages.warning(request,"نام کاربری تکراری است")
            return redirect('signUp')

        try:
            CustomUser.objects.create_user(first_name = data.get("name") , last_name = data.get("lname") 
                                              , username = data.get("studentcode"),password=data.get("nationalcode"),
                                              nationalcode = data.get("nationalcode") , email=data.get("email"))
            messages.warning(request,"حساب کاربری ساخته شد . ")
            
        except:
            messages.warning(request,"حساب کاربری ساخته نشد . ")
            return redirect('signUp')
        return redirect('login')

 
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.role == 'teacher':
            return reverse_lazy('teacher_home')
        else:
            return reverse_lazy('student_home')
        

@method_decorator(teacher_required, name='dispatch')
class TeacherHomeView(LoginRequiredMixin,TemplateView):
    template_name = 'teacher\index.html'
    login_url = '/login/'

    def get_context_data(self ,**kwargs):
        studentActivity = Submissions.objects.filter( is_Checked = False , is_contest = False)
        sent_submissions = Submissions.objects.all().count()
        correct_submissions = Submissions.objects.filter(final_result = True).count()
        wrong_submissions = Submissions.objects.filter(final_result = False).count()
        questions = Question.objects.all().count()
        return {"context" : studentActivity,"sent_submissions":sent_submissions,"correct_submissions":correct_submissions,"wrong_submissions":wrong_submissions,"questions":questions}


# @method_decorator(student_required, name='dispatch')
class StudentHomeView(LoginRequiredMixin,TemplateView):
    template_name = 'student\index.html'

    def get_context_data(self ,**kwargs):
        studentActivity = Submissions.objects.filter(student = self.request.user , is_contest = False)
        sent_submissions = Submissions.objects.filter(student = self.request.user).count()
        correct_submissiobs = Submissions.objects.filter(student = self.request.user , final_result = True).count()
        unsolvedQuestions = Question.objects.exclude(id__in=Submissions.objects.filter(student=self.request.user).values_list("question_id", flat=True)).count
        return {"context" : studentActivity,"numberOfSent" : sent_submissions,"numberOfCorrects" : correct_submissiobs,"numberOfWrongs":sent_submissions-correct_submissiobs,"unslovedQuestion":unsolvedQuestions}


# @method_decorator(student_required, name='dispatch')
class StudentProfile(LoginRequiredMixin, View):
    template_name = 'student\profile.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self, request):
        try:
            user = request.user
            email = request.POST.get('email')
            mobilephone = request.POST.get('phone')
            user.mobilephone = mobilephone
            user.email = email
            user.save()
            messages.success(request, "اطلاعات شما با موفقیت ویرایش شد .")
        except Exception as e:
            messages.warning(request,e)
        return redirect('profile')

@method_decorator(teacher_required, name='dispatch')
class Add_User(View):
    template_name = 'teacher/clientAdd.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        try:
            if not CustomUser.objects.filter(username=request.POST.get('username')).exists():
                if request.POST.get('nationalcode') == "":
                    messages.warning(request,"رمز ورود خالی می باشد .")
                else:
                    user = CustomUser.objects.create_user(username = request.POST.get('username') , password = request.POST.get('nationalcode') , first_name = request.POST.get('fname') , last_name = request.POST.get('lname'), role = request.POST.get('role'))
                    user.save()
                    messages.success(request, "کاربر افزوده شد .")
            else:
                messages.warning(request, f"کاربر با نام کاربری {request.POST.get('username')} وجود دارد .")
        except Exception as e:
                messages.warning(request, e)
        return redirect('addUser')




def logout_user(request):
    logout(request)
    return redirect('/') 


import openpyxl
@method_decorator(teacher_required, name='dispatch')
class register_users_from_excel(View):
    def post(self,request):
        try:
            excel_file = request.FILES['excel_file']

            # Open the Excel file
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            # Iterate over the rows in the Excel file and create users
            for row in sheet.iter_rows(min_row=2, values_only=True):
                username ,nationalcode , firstname , lastname , role = row
            # print(username,password,firstname,lastname,role)
                # Validate and create user
                if username and nationalcode:  # Simple validation (can be expanded)
                    if not CustomUser.objects.filter(username=username).exists():
                        user = CustomUser.objects.create_user(
                            username=username,
                            first_name=firstname,
                            last_name=lastname,
                            password=str(nationalcode),
                            role = role 
                        )
                        user.save()
                    else:
                        messages.warning(request, f"کاربر با نام کاربری {username} وجود دارد.")
                else:
                    messages.warning(request, "بعضی از مقادیر وجود ندارند .")

            messages.success(request, 'کاربران با موفقیت ثبت شدند.')
        except:
            messages.warning(request,"فایلی انتخاب نشده است")
        return redirect('addUser') 
    
@method_decorator(teacher_required, name='dispatch')
class Users(View):
    def get(self,request):
        users = CustomUser.objects.filter(role = 1)
        return render(request,'teacher/users.html',{'context' : users})
    

@method_decorator(teacher_required, name='dispatch')
class User_Detail(View):
    def post(self,request,id):
        user = get_object_or_404(CustomUser,pk = id)
        return render(request,'teacher/userdetail.html',{'context':user})


@method_decorator(teacher_required, name='dispatch')
class addContester(View):
    def get(self,request):
        contests = Contest.objects.all()
        # users = CustomUser.objects.filter(role=1)
        users = CustomUser.objects.exclude(id__in=Contester.objects.values_list('user_id', flat=True)).filter(role=1)
        return render(request,'contest/addcontester.html',{'contests':contests,'users':users})
    def post(self,request):
        contest = Contest.objects.get(id=request.POST.get('contest'))
        questions = {}
        # counter = 1
        for question in contest.questions.values():
            id = question['id']
            questions[f'{id}'] = {"result":False,"tries":0,"first":False}
            id = ''
            # counter += 1
        Contester.objects.create(user = CustomUser.objects.get(id=request.POST.get('user')),contest =contest,questions=questions )
        messages.success(request, 'کاربر با موفقیت ثبت شد.')
        return redirect('addContester') 


class report(View):
    def get(self,request):
        return render(request,'teacher/report.html')
    def post(self,request):
        usercode = request.POST.get("code")
        user = CustomUser.objects.get(username = usercode)
        user_submissions = Submissions.objects.filter(student = user)
        return render(request,'teacher/report.html',{"client":user,
                                                     "user_submissions":user_submissions.count()
                                                     ,"user_trueResponse":user_submissions.filter(final_result=True).count()
                                                     ,"user_falseResponse":user_submissions.filter(final_result=False).count()})