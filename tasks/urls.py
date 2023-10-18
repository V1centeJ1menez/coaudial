from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout_view'),
    path("home/", views.home,name="home"),
    path("cursos/", views.cursos,name="cursos"),
    path('choose_user_type/', views.choose_user_type, name='choose_user_type'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile, name='profile'),
]
