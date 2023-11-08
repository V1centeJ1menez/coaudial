from django.contrib import admin
from .models import CustomUser, Normal, Organizacion,Curso

admin.site.register(CustomUser)
admin.site.register(Normal)
admin.site.register(Organizacion)
admin.site.register(Curso)