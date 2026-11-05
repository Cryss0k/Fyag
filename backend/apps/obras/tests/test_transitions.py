"""Máquina de estados (lógica pura). Casos del plan: CPF-09 a CPF-15."""

import pytest

from apps.obras.models import EstadoObra as E
from apps.obras.services import is_transition_allowed


@pytest.mark.parametrize(
    "desde,hacia",
    [
        (E.SUSPENDIDA, E.EN_PROCESO),
        (E.EN_PROCESO, E.FINALIZADA),
        (E.EN_PROCESO, E.SUSPENDIDA),
        (E.SUSPENDIDA, E.CANCELADA),
        (E.FINALIZADA, E.COBRADA),
    ],
)
def test_transiciones_permitidas(desde, hacia):
    assert is_transition_allowed(desde, hacia)


@pytest.mark.parametrize(
    "desde,hacia",
    [
        (E.EN_PROCESO, E.CANCELADA),  # CPF-14: solo se cancela una obra suspendida
        (E.SUSPENDIDA, E.FINALIZADA),
        (E.FINALIZADA, E.SUSPENDIDA),
        (E.COBRADA, E.EN_PROCESO),
        (E.CANCELADA, E.EN_PROCESO),
    ],
)
def test_transiciones_prohibidas(desde, hacia):
    assert not is_transition_allowed(desde, hacia)
