from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,authenticate
# Create your views here.

def loginpage(request):
    return render(request,'login.html')

def teacherIndex(request):
    return render(request,'teacher/index.html')

def logins(request):
    if request.method == 'POST':
        user = authenticate(request,username = request.POST["username"],password = request.POST["password"])
        if user is not None:
            login(request,user)
            return redirect('TeacherIndex')
        else:
            return HttpResponse("Wrong username or passowrd")