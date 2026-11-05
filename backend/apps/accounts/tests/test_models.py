import pytest

from apps.accounts.models import Rol, Usuario


@pytest.mark.django_db
def test_create_user_hashea_la_clave_con_argon2():
    user = Usuario.objects.create_user("ana@fyag.local", "una-clave-larga-123", nombre_completo="Ana", rol=Rol.GERENCIA)
    assert user.password.startswith("argon2")
    assert user.check_password("una-clave-larga-123")
    assert user.is_active
