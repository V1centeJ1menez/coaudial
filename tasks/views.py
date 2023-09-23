from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Normal, Organizacion, CustomUser
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):

    return render(request, 'tasks/home.html')

def signup(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            if user.user_type == 1:

                Normal.objects.create(user=user)
                return render(request, "tasks/home.html")

            else:

                Organizacion.objects.create(user=user)
                return render(request, "tasks/home.html")
            
        else:
            print(form.errors)
        
    else:

        form = CustomUserCreationForm()

    return render(request, "tasks/signup.html", {"register_form":form})

def login(request):
    
    return render(request, 'tasks/login.html')

def main(request):

    return render(request, 'tasks/main.html')

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if user.user_type == 1:
        return render(request, "tasks/normal_home.html", {"user": user})
    else:
        return render(request, "tasks/organization_home.html", {"user": user})

def cursos(request):

    return render(request, 'tasks/cursos.html')