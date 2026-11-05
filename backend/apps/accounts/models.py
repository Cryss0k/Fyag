"""accounts — models. Dueño: Back 1. Esquema v1 + D-04 (intentos_fallidos, bloqueado_hasta)."""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Rol(models.TextChoices):
    GERENCIA = "GERENCIA", "Gerencia"
    ADMINISTRATIVO = "ADMINISTRATIVO", "Administrativo (Finanzas)"
    SUPERVISOR = "SUPERVISOR", "Supervisor de obra"
    TECNICO = "TECNICO", "Técnico en terreno"


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, correo, password=None, **extra):
        if not correo:
            raise ValueError("El correo es obligatorio")
        user = self.model(correo=self.normalize_email(correo), **extra)
        user.set_password(password)  # password=None deja la clave inutilizable
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("rol", Rol.GERENCIA)
        return self.create_user(correo, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    rol = models.CharField(max_length=20, choices=Rol.choices)
    activo = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # solo para /admin
    intentos_fallidos = models.PositiveSmallIntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)

    objects = UsuarioManager()
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre_completo"]

    class Meta:
        db_table = "usuarios"

    @property
    def is_active(self):
        return self.activo

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"
