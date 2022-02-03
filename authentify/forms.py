from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


"""
Create and update custom user form on admin
"""
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email','username','slug', 'created_at', 'updated_at')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email','username', 'slug', 'created_at', 'updated_at')