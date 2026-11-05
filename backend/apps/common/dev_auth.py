"""Autenticación de DESARROLLO. Dueño: Manager.

Permite probar cada rol antes de que exista el login real (Back 1):

    curl -H "X-Dev-Role: SUPERVISOR" http://localhost:8000/api/v1/obras/

Solo actúa si DEBUG=True y DEV_AUTH=True. En cualquier otro caso es inerte.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .roles import ALL_ROLES


class DevAuthentication(BaseAuthentication):
    header = "HTTP_X_DEV_ROLE"

    def authenticate(self, request):
        if not (settings.DEBUG and getattr(settings, "DEV_AUTH", False)):
            return None
        rol = request.META.get(self.header)
        if not rol:
            return None
        rol = rol.strip().upper()
        if rol not in ALL_ROLES:
            raise AuthenticationFailed("Rol de desarrollo inválido")
        user_model = get_user_model()
        correo = f"dev-{rol.lower()}@fyag.local"
        try:
            user = user_model.objects.get(correo=correo)
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(
                correo=correo, password=None, nombre_completo=f"Dev {rol.title()}", rol=rol
            )
        return (user, None)

    def authenticate_header(self, request):
        # Sin esto, una petición sin sesión respondería 403 en vez de 401 (DRF usa el 1.er autenticador).
        return "Bearer"
