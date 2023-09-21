from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):

    return render(request, 'tasks/home.html')

def signup(request):

    return render(request, 'tasks/signup.html')

def login(request):
    
    return render(request, 'tasks/login.html')

def main(request):

    return render(request, 'tasks/main.html')

def orgPage(request):

    return render(request, 'tasks/orgPage.html')

def userPage(request):

    return render(request, 'tasks/userPage.html')

def courses(request):

    return render(request, 'tasks/courses.html')