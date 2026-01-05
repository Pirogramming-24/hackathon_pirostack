from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .models import Profile
import os
from dotenv import load_dotenv

# Create your views here.

def signUp(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        hashed_password = make_password(password)

        if Profile.objects.filter(phone_number=phone_number).exists():
            return render(request,"signUp.html",{"error":"이미 가입된 번호입니다"})

        if role == 'Executive':
            nickname='Piro_Executive'
        else:
            nickname='Piro'

        new_user = User.objects.create(
            username=phone_number,
            password=hashed_password
        )

        Profile.objects.create(
            user=new_user,
            role=role,
            name=name,
            nickname = nickname,
            phone_number=phone_number, #아이디로 취급
            password=hashed_password
        )
        return redirect('users:login')
    return render(request,"signUp.html")

def login(request):
    load_dotenv()
    secret_key = os.environ.get('SECRET_KEY')
    secret_password = os.environ.get('SECRET_PASSWORD')
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if check_password(password,secret_password) and phone_number==secret_key:
            return redirect('users:superadmin')
        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            messages.error(request,"아이디나 비밀번호가 틀렸습니다")
            return redirect('users:login')
        if check_password(password,profile.password) and profile.permission:
            profile.user.is_active = True
            return redirect('questions:list')
    return render(request,'login.html')

def superadmin(request):
    if request.method == 'POST':
        selected_id = request.POST.get('admit_btn')
        person = Profile.objects.get(id=selected_id)
        person.permission = True
        if person.role == "Executive":
            user_obj = person.user
            user_obj.is_staff = True
            user_obj.save()
            print('staff')
        person.save()

    people = Profile.objects.all()
    context = {
        'people':people
    }
    return render(request,'superadmin.html',context)