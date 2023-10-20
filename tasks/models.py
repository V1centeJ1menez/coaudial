from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        (1, 'normal'),
        (2, 'organizacion'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_user_permissions")


class Normal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Organizacion(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

