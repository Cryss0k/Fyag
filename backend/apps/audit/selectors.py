"""audit — selectors. Dueño: Manager."""

from django.conf import settings

from . import services


def list_logs(tipo_entidad: str, id_entidad: int, limit: int = 100) -> list[dict]:
    backend = settings.AUDIT_BACKEND
    if backend == "memory":
        rows = [
            r for r in services._memory_store if r["tipo_entidad"] == tipo_entidad and r["id_entidad"] == id_entidad
        ]
        return list(reversed(rows))[:limit]
    if backend == "mongo":
        cursor = (
            services._collection()
            .find({"tipo_entidad": tipo_entidad, "id_entidad": id_entidad})
            .sort("fecha_registro", -1)
            .limit(limit)
        )
        return [{**row, "_id": str(row["_id"])} for row in cursor]
    return []  # backend "log": no hay dónde consultar
