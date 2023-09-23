from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.main, name='main'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("home/", views.home,name="home"),
    path("courses/", views.courses,name="courses"),
    path('<str:username>/', views.profile, name='profile'),
]
