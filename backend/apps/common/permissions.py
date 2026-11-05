"""Permisos por rol. Dueño: Manager.

Uso en una vista:

    from apps.common.permissions import roles
    from apps.common import roles as R

    class MiVista(APIView):
        permission_classes = [roles(R.GERENCIA, R.ADMINISTRATIVO)]

Un usuario sin sesión o con otro rol recibe 401/403 (denegar por defecto).
"""

from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "rol", None) in self.allowed_roles)


def roles(*allowed: str) -> type[HasRole]:
    """Crea una clase de permiso que acepta solo los roles indicados."""
    return type("HasRole_" + "_".join(allowed), (HasRole,), {"allowed_roles": tuple(allowed)})
