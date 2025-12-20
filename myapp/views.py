from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import College, AptitudeQuestion, TestResult


def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        try:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('login')
        except Exception:
            messages.error(request, "Something went wrong. Try again.")
            return redirect('signup')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('college_list')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def college_list(request):
    location = request.GET.get('location')
    if location:
        colleges = College.objects.filter(location__icontains=location)
    else:
        colleges = College.objects.all()
    return render(request, 'collegelist.html', {'colleges': colleges})


@login_required
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


@login_required
def result(request):
    test_result = TestResult.objects.filter(student=request.user).last()
    return render(request, 'result.html', {'result': test_result})
