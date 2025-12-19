from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import College, AptitudeQuestion, TestResult
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('college_list')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def college_list(request):
    location = request.GET.get('location')
    if location:
        colleges = College.objects.filter(location__icontains=location)
    else:
        colleges = College.objects.all()
    return render(request, 'collegelist.html', {'colleges': colleges})

def aptitude_test(request):
    questions = AptitudeQuestion.objects.all()
    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1
        TestResult.objects.create(student=request.user, score=score)
        return redirect('result')
    return render(request, 'aptitudetest.html', {'questions': questions})

def result(request):
    test_result = TestResult.objects.filter(student=request.user).last()
    return render(request, 'result.html', {'result': test_result})

