from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'email', 'first_name', 'last_name',)

class ChooseUserTypeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_type']
