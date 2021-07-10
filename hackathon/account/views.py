from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import Profile

# Create your views here.
def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error':"사용자 이름 혹은 패스워드가 일치하지 않습니다."})
    else:
        return render(request, 'login.html')

def register(request) :
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "이미 존재하는 사용자입니다. "})
        if password == request.POST['passwordCheck']:
            user = User.objects.create_user(
                username, password = password
            )
            auth.login(request,user)
            profile = Profile()
            profile.user = user
            profile.point = 100
            profile.nickname = request.POST['nickname']
            profile.save()
            return redirect('/')
        else:
            return render(request, 'register.html', {'error': '비밀번호가 일치하지 않습니다. '})
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')