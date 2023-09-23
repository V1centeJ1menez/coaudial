from django.contrib import admin
from .models import CustomUser, Normal, Organizacion

admin.site.register(CustomUser)
admin.site.register(Normal)
admin.site.register(Organizacion)
