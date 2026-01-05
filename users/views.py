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

        current_user = User.objects.create_user(username=phone_number, password=password)

        Profile.objects.create(
            user=current_user,
            role=role,
            nickname='Piro',
            name=name,
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
            print('success')
        else:
            print('fail')
    return render(request,'login.html')