from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Empleado, UserProfile


class CustomUserAdmin(UserAdmin):
    #add_form = UserCreationForm
    #form = UserChangeForm
    model = UserProfile
    list_display = ['email', 'last_login', 'is_active', 'is_superuser']

admin.site.register(UserProfile, CustomUserAdmin)