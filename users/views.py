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
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')

        if Profile.objects.filter(phone_number=phone_number).exists():
            return render(request,"signUp.html",{"error":"이미 가입된 번호입니다"})

        if role == 'Executive':
            is_staff = True
        else:
            is_staff = False

        new_profile = Profile.objects.create(
            role=role,
            name=name,
            phone_number=phone_number, #아이디로 취급
            is_staff = is_staff
        )
        if role == 'Executive':
            return redirect('users:signupPass',pk=new_profile.id)
        return redirect('users:login')
    return render(request,"signUp.html")

def signupPass(request,pk):
    profile = Profile.objects.get(id=pk)
    context = {
        'profile':profile
    }
    if request.method == 'POST':
        profile.password = request.POST.get('password')
        profile.save()
        return redirect('users:login')
    return render(request,'password_form.html',context)

def login(request):
    load_dotenv()
    secret_key = os.environ.get('SECRET_KEY')
    secret_password = os.environ.get('SECRET_PASSWORD')
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # if check_password(password,secret_password) and phone_number==secret_key:#슈퍼 어드민
        #     print('')
        #     return redirect('users:superadmin')
        if phone_number==secret_key:#슈퍼 어드민
            print('iii')
            return redirect('users:superadmin')
        try:
            profile = Profile.objects.get(phone_number=phone_number)#프로필 객체 id겟
        except Profile.DoesNotExist:
            messages.error(request,"아이디나 비밀번호가 틀렸습니다")
            return redirect('users:login')
        
        if profile.is_staff:
            return redirect('users:loginPass',pk=profile.id)

        if profile.permission:
            return redirect('questions:list')
    return render(request,'login.html')

def loginPass(request,pk):
    profile = Profile.objects.get(id=pk)
    context = {
        'profile':profile
    }
    if request.method == 'POST':
        print(request.POST.get('password'))
        if profile.password == request.POST.get('password'):
            return redirect('questions:list')
    return render(request,'password_form.html',context)

def superadmin(request):
    if request.method == 'POST':
        selected_id = request.POST.get('admit_btn')
        person = Profile.objects.get(id=selected_id)
        person.permission = True
        person.save()

    people = Profile.objects.all()
    context = {
        'people':people
    }
    return render(request,'superadmin.html',context)