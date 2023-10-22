from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        (1, 'normal'),
        (2, 'organizacion'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null="True", blank="True")
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_user_permissions")


class Normal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def delete(self, *args, **kwargs):
        self.groups.clear()
        super().delete(*args, **kwargs)

class Organizacion(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    foundation_image = models.ImageField(upload_to='foundation_images/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    redirect_url = models.URLField(max_length=200, null=True, blank=True)
    footer = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.groups.clear()
        super().delete(*args, **kwargs)


