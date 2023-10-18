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

            if user.user_type == 1:
                Normal.objects.create(user=user)

            else:
                Organizacion.objects.create(user=user)
            messages.success(request, f'El usuario {tipo_usuario} {user.username} fue correctamente registrado')

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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.user.is_authenticated and request.user.username == username:
        if user.user_type == 1:
            normal_user = get_object_or_404(Normal, user=user)
            return render(request, 'tasks/perfiles/normal_home.html', {'user': normal_user, 'user_type': 'normal'})
        
        elif user.user_type == 2:
            org_user = get_object_or_404(Organizacion, user=user)
            return render(request, 'tasks/perfiles/organization_home.html', {'user': org_user, 'user_type': 'organizacion'})
        
        else:
            return HttpResponse("Hola")
        
    else:
        if user.user_type == 1:
            normal_user = get_object_or_404(Normal, user=user)
            return render(request, 'tasks/perfiles/normal_profile.html', {'user': normal_user, 'user_type': 'normal'})
        
        elif user.user_type == 2:
            org_user = get_object_or_404(Organizacion, user=user)
            return render(request, 'tasks/perfiles/organization_profile.html', {'user': org_user, 'user_type': 'organizacion'})
        
        else:
            return HttpResponse('hola')

@login_required
def cursos(request):
    # Aqui necesito ponerle mas cosas, ya que se divide en mas secciones este apartado
    return render(request, 'tasks/aprendizaje/cursos.html')