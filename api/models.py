from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('El usuario debe ingresar un email')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=False, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return '{0}{1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    def __str__(self):
        return self.email


class Empleado(models.Model):
    cedula = models.CharField(max_length=10, null=False, blank=False)
    nombres = models.CharField(max_length=100, null=False, blank=False)
    apellidos = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion_domicilio = models.TextField(null=True, blank=True)
    celular = models.CharField(max_length=10, null=True, blank=True)
    vacunado = models.BooleanField(null=True, blank=True, default=True)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{0} {1} {2}'.format(self.cedula, self.apellidos, self.nombres)


class Dosis(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    vacuna = models.CharField(max_length=60, null=False, blank=False)
    fecha_vacuna = models.DateField(null=False, blank=False)
    dosis_numero = models.SmallIntegerField(null=False, blank=False)
    deleted = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'dosis'

    def __str__(self):
        return '{0} {1} {2}'.format(self.empleado.cedula, self.vacuna, self.dosis_numero)