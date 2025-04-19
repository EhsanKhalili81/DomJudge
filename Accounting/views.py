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



def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view
 
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


@method_decorator(student_required, name='dispatch')
class StudentHomeView(LoginRequiredMixin,TemplateView):
    template_name = 'student\index.html'


@method_decorator(student_required, name='dispatch')
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