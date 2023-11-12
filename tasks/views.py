from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Normal, Organizacion, CustomUser, Curso
from .forms import CustomUserCreationForm, ChooseUserTypeForm, EditProfileForm, CustomPasswordChangeForm, EditOrganizationTemplateForm, CursoForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth import get_user_model
import re
from googleapiclient.discovery import build


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
    user = request.user  # Obtener el usuario actual
    if user.user_type == 1:
        # Usuario de tipo 1 (normal)
        return render(request, 'tasks/aprendizaje/normal_cursos.html')
    elif user.user_type == 2:
        # Usuario de tipo 2 (organización)
        return render(request, 'tasks/aprendizaje/organizacion_cursos.html')

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)

        if form.is_valid():
            curso = form.save(commit=False)
            curso.user_name = request.user.first_name # Asigna el nombre de usuario al campo "user_name"
            curso.save()

            return redirect('cursos')

    else:
        form = CursoForm()

    return render(request, 'tasks/aprendizaje/crear_curso.html', {'form': form})


@login_required
def obtener_id_playlist(url):
    # Expresión regular para extraer el identificador de la playlist de una URL de YouTube
    pattern = r"^(https?://)?(www\.youtube\.com|youtu\.?be)/playlist\?list=([a-zA-Z0-9_-]+)"
    match = re.match(pattern, url)
    if match:
        return match.group(3)
    return None


@login_required
def obtener_informacion_playlist(id_playlist):
    # Configura la API de YouTube
    api_key = 'TU_API_KEY_DE_YOUTUBE'
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Realiza una solicitud para obtener información sobre la playlist
    playlist_info = youtube.playlists().list(
        part='snippet',
        id=id_playlist
    ).execute()

    return playlist_info

@login_required
def reproducir_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    return render(request, 'tasks/aprendizaje/reproducir_curso.html', {'curso': curso})

# Vista para crear un nuevo curso
@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el nombre de usuario en el formulario
            form.instance.user_name = request.user.first_name
            form.save()
            return redirect('todos_los_cursos')
    else:
        form = CursoForm()
    return render(request, 'tasks/aprendizaje/crear_curso.html', {'form': form})

# Vista para ver todos los cursos
@login_required
def todos_los_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'tasks/aprendizaje/todos_los_cursos.html', {'cursos': cursos})