from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("home/", views.home,name="home"),
    path("cursos/", views.cursos,name="cursos"),
    path('<str:username>/', views.profile, name='profile'),
]
