from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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
                return HttpResponse("Usuario del tipo 1 autenticado exitosamente")
            
            elif hasattr(user, 'organizacion'):
                return HttpResponse("Usuario del tipo 2 autenticado exitosamente")
            
            else:
                return HttpResponse("Usuario autenticado exitosamente")
            
        else:
            return HttpResponse("Credenciales inválidas")
        
    else:
        # Renderizar la plantilla de inicio de sesión aquí
        return render(request, 'tasks/login.html')


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