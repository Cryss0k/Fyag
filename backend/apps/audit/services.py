"""audit — services. Dueño: Manager.

Interfaz pública que usan TODOS los módulos:

    from apps.audit.services import log_event

    log_event(
        tipo_entidad="OBRA", id_entidad=obra.pk, accion="CAMBIO_ESTADO",
        usuario=request.user, estado_anterior="EN_PROCESO", estado_nuevo="FINALIZADA",
        motivo="Trabajos concluidos", detalles={"tecnico_responsable": "Juan Pérez"},
    )

Llamar como ÚLTIMO paso dentro de transaction.atomic(): si la auditoría falla se lanza
AuditError y el cambio se revierte (caso CPI-07).

Backends (settings.AUDIT_BACKEND): "mongo" (colección audit_logs), "log" (solo logging, para
desarrollo sin Mongo) y "memory" (tests).
"""

import logging
from datetime import UTC, datetime

from django.conf import settings

logger = logging.getLogger("fyag.audit")

_memory_store: list[dict] = []
_mongo_client = None


class AuditError(Exception):
    """No se pudo registrar el evento de auditoría."""


def _collection():
    global _mongo_client
    from pymongo import MongoClient

    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
    return _mongo_client[settings.MONGO_DB]["audit_logs"]


def log_event(
    *,
    tipo_entidad: str,
    id_entidad: int,
    accion: str,
    usuario,
    estado_anterior: str | None = None,
    estado_nuevo: str | None = None,
    motivo: str = "",
    detalles: dict | None = None,
) -> dict:
    doc = {
        "id_entidad": id_entidad,
        "tipo_entidad": tipo_entidad,
        "accion": accion,
        "estado_anterior": estado_anterior,
        "estado_nuevo": estado_nuevo,
        "usuario": {
            "id_usuario": usuario.pk,
            "nombre": getattr(usuario, "nombre_completo", ""),
            "rol": getattr(usuario, "rol", ""),
        },
        "fecha_registro": datetime.now(UTC).isoformat(),
        "detalles": {"motivo": motivo, **(detalles or {})},
    }
    backend = settings.AUDIT_BACKEND
    try:
        if backend == "mongo":
            _collection().insert_one(dict(doc))
        elif backend == "memory":
            _memory_store.append(doc)
        else:
            logger.info("AUDIT %s", doc)
    except Exception as exc:  # noqa: BLE001
        raise AuditError("No se pudo registrar la auditoría") from exc
    return doc


def clear_memory_store() -> None:
    """Solo para tests."""
    _memory_store.clear()
