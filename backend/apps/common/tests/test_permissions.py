"""Ejemplo del patrón de pruebas de permisos por rol (Normas §10).

Cada endpoint nuevo debe tener un test como este por cada rol relevante.
"""

import pytest
from rest_framework.test import APIClient

URL = "/api/v1/audit/logs/?tipo_entidad=OBRA&id_entidad=1"


@pytest.fixture
def dev_client(settings):
    settings.DEBUG = True
    settings.DEV_AUTH = True
    return APIClient()


def test_sin_sesion_recibe_401():
    response = APIClient().get(URL)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "NO_AUTENTICADO"


@pytest.mark.django_db
def test_tecnico_recibe_403(dev_client):
    response = dev_client.get(URL, HTTP_X_DEV_ROLE="TECNICO")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "SIN_PERMISO"


@pytest.mark.django_db
@pytest.mark.parametrize("rol", ["GERENCIA", "SUPERVISOR"])
def test_roles_autorizados_reciben_200(dev_client, rol):
    response = dev_client.get(URL, HTTP_X_DEV_ROLE=rol)
    assert response.status_code == 200
