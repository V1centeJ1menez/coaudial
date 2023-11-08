from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout_view'),
    path("home/", views.home,name="home"),
    path("cursos/", views.cursos,name="cursos"),
    path('choose_user_type/', views.choose_user_type, name='choose_user_type'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_user, name='search_user'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('todos_los_cursos/', views.todos_los_cursos, name='todos_los_cursos'),
    path('reproducir_curso/<int:curso_id>/', views.reproducir_curso, name='reproducir_curso'),
    path('<str:username>/preview/', views.profile, {'preview': True}, name='profile_preview'),
    path('<str:username>/edit_template/', views.edit_organization_template, name='edit_organization_template'),
    path('<str:username>/', views.profile, name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
