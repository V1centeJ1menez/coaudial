from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.main),
    path("signup/", views.signup),
    path("login/", views.login, name="login"),
    path("home/", views.home,name="home"),
    path("orgPage/", views.orgPage,name="orgPage"),
    path("userPage/", views.userPage, name="userPage"),
     path("courses/", views.courses,name="courses"),
]
