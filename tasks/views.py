from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Normal, Organizacion, CustomUser
from .forms import CustomUserCreationForm

# Create your views here.
def home(request):

    return render(request, 'tasks/home.html')

def signup(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            tipo_usuario = 'normal' if user.user_type == 1 else 'organizacion'
            messages.success(request, f'El usuario {tipo_usuario} {user.username} fue correctamente registrado')

            if user.user_type == 1:

                Normal.objects.create(user=user)
                return render(request, "tasks/index.html")

            else:

                Organizacion.objects.create(user=user)
                return render(request, "tasks/index.html")
            
        else:
            print(form.errors)
        
    else:

        form = CustomUserCreationForm()

    return render(request, "tasks/signup.html", {"register_form":form})

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if hasattr(user, 'normal'):
                messages.success(request, f'Bienvenido de vuelta {user.username}. ¡Esperamos que disfrutes tu tiempo aquí!')
            else:
                messages.success(request, f'La organización {user.username} ha iniciado sesión exitosamente. ¡Estamos emocionados de ver las contribuciones que harás a nuestra comunidad!')
            return redirect('home')
            
        else:
            return HttpResponse("Credenciales inválidas")
        
    else:
        # Renderizar la plantilla de inicio de sesión aquí
        return render(request, 'tasks/login.html')

def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, f'Has cerrado sesión exitosamente, {username}. ¡Esperamos verte de nuevo pronto!')
    return redirect('index')


def index(request):

    return render(request, 'tasks/index.html')

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.user.username == username:
        if user.user_type == 1:
            # Aquí puedes agregar el código para permitir a los usuarios normales editar su perfil
            pass
        else:
            # Aquí puedes agregar el código para permitir a las cuentas de organización editar su perfil
            pass
    else:
        if user.user_type == 1:
            return render(request, "tasks/normal_home.html", {"user": user})
        else:
            return render(request, "tasks/organization_home.html", {"user": user})

def cursos(request):

    return render(request, 'tasks/cursos.html')