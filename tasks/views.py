from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Normal, Organizacion, CustomUser
from .forms import CustomUserCreationForm, ChooseUserTypeForm, EditProfileForm, CustomPasswordChangeForm, EditOrganizationTemplateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth import get_user_model

# Create your views here.

def search_user(request):
    if request.method == 'GET':
        user_type = 2  # Tipo de usuario "organización"
        query = request.GET.get('query', '')  # Obtiene la consulta de búsqueda

        # Realiza la búsqueda de usuarios por first_name
        users = get_user_model().objects.filter(user_type=user_type, first_name__icontains=query)

        if not users:
            messages.error(request, f"No se encontró ningún usuario con el nombre '{query}'.")
            return redirect('home')  # Redirige a la página home con un mensaje de error

        return render(request, 'tasks/search_results.html', {'users': users})


def home(request):
    organizations = CustomUser.objects.filter(user_type=2)
    return render(request, 'tasks/home.html', {'organizations': organizations})


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


def profile(request, username, preview=False):
    user = get_object_or_404(CustomUser, username=username)

    
    if preview:
        # Si estamos en modo de vista previa, mostramos el perfil público
        if user.user_type == 2:  # Solo permitimos la vista previa para los usuarios de tipo "Organización"
            org_user = get_object_or_404(Organizacion, user=user)
            return render(request, 'tasks/perfiles/organization_profile.html', {'user': org_user, 'user_type': 'organizacion'})
        else:
            raise Http404("La vista previa no está disponible para este tipo de usuario.")
        
        
    else:

        if request.user.is_authenticated and (request.user.username == username) and (request.user.is_staff or request.user.is_superuser):
            return HttpResponse("Eres admin papu, don worri")

        elif request.user.is_authenticated and request.user.username == username:
            if user.user_type is None:
                return redirect('choose_user_type')
            elif user.user_type == 1:
                normal_user = get_object_or_404(Normal, user=user)
                return render(request, 'tasks/perfiles/normal_home.html', {'user': normal_user, 'user_type': 'normal'})
            elif user.user_type == 2:
                org_user = get_object_or_404(Organizacion, user=user)
                return render(request, 'tasks/perfiles/organization_home.html', {'user': org_user, 'user_type': 'organizacion'})
        
        else:  # El usuario no está autenticado o no es el propietario del perfil
            if user.user_type == 1:
                normal_user = get_object_or_404(Normal, user=user)
                return render(request, 'tasks/perfiles/normal_profile.html', {'user': normal_user, 'user_type': 'normal'})
            
            elif user.user_type == 2:
                org_user = get_object_or_404(Organizacion, user=user)
                return render(request, 'tasks/perfiles/organization_profile.html', {'user': org_user, 'user_type': 'organizacion'})
            
            elif user.user_type is None:    
                raise Http404("El perfil no existe.")
    


@login_required
def choose_user_type(request):
    if request.method == 'POST':
        form = ChooseUserTypeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.user_type == 1:  # Si el usuario ha elegido el tipo de usuario "normal"
                Normal.objects.get_or_create(user=request.user)  # Crea una instancia de Normal si no existe
            messages.success(request, 'Tu tipo de usuario ha sido actualizado.')
            return redirect('profile', username=request.user.username)
    else:
        form = ChooseUserTypeForm(instance=request.user)

    return render(request, 'tasks/perfiles/choose_user_type.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if 'submit-profile' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('profile', username=request.user.username)
        elif 'submit-password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Actualiza la sesión para que no sea necesario volver a iniciar sesión
                return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    return render(request, 'tasks/perfiles/edit_profile.html', {'form': form, 'password_form': password_form})


@login_required
def edit_organization_template(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user != user or user.user_type != 2:
        return HttpResponseForbidden("No tienes permiso para editar esta plantilla.")
    if request.method == 'POST':
        form = EditOrganizationTemplateForm(request.POST, request.FILES, instance=user.organizacion)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = EditOrganizationTemplateForm(instance=user.organizacion)
    return render(request, 'tasks/perfiles/edit_organization_template.html', {'form': form})


@login_required
def cursos(request):
    # Aqui necesito ponerle mas cosas, ya que se divide en mas secciones este apartado
    return render(request, 'tasks/aprendizaje/cursos.html')