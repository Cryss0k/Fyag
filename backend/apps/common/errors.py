"""Errores con formato uniforme (Normas §6):

    {"error": {"code": "OBRA_SIN_TECNICO", "message": "...", "details": {}}}
"""

import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("fyag.errors")


class DomainError(Exception):
    """Violación de una regla de negocio. Por defecto responde 409."""

    def __init__(self, code: str, message: str, status_code: int = 409, details: dict | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


_CODES = {
    400: "VALIDACION",
    401: "NO_AUTENTICADO",
    403: "SIN_PERMISO",
    404: "NO_ENCONTRADO",
    405: "METODO_NO_PERMITIDO",
    429: "DEMASIADAS_SOLICITUDES",
}


def _body(code: str, message: str, details=None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}


def exception_handler(exc, context):
    if isinstance(exc, DomainError):
        return Response(_body(exc.code, exc.message, exc.details), status=exc.status_code)

    response = drf_exception_handler(exc, context)
    if response is None:
        # Error no controlado: mensaje genérico, sin trazas hacia el cliente.
        logger.exception("Error no controlado", exc_info=exc)
        return Response(_body("ERROR_INTERNO", "Error interno del servidor"), status=500)

    data = response.data
    code = _CODES.get(response.status_code, "ERROR")
    if isinstance(data, dict) and "detail" in data:
        response.data = _body(code, str(data["detail"]))
    elif response.status_code == 400:
        response.data = _body(code, "Hay datos inválidos", data)
    else:
        response.data = _body(code, "Error en la solicitud", data)
    return response
