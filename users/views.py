from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def signUp(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if User.objects.filter(username=phone_number).exists():
            return render(request,"signUp.html",{"error":"이미 가입된 번호입니다"})

        current_user = User.objects.create_user(username=phone_number, password=password)

        if role == 'Executive':
            nickname='Piro_Executive'
            current_user.is_staff = True
        else:
            nickname='Piro'
            current_user.is_staff = False

        current_user.save()

        Profile.objects.create(
            user=current_user,
            role=role,
            name=name,
            nickname = nickname,
            phone_number=phone_number, #아이디로 취급
            password=password

        )
    return render(request,"signUp.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            if user.is_staff:
                print('staff')
                print(user.profile.id)
                print(user.id)
                return redirect('questions:list')
            else:
                print('member')
        else:
            print('fail')
    return render(request,'login.html')