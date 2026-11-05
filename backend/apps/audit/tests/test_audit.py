from types import SimpleNamespace

from apps.audit import selectors, services


def test_log_event_y_consulta_en_backend_memory():
    services.clear_memory_store()
    usuario = SimpleNamespace(pk=5, nombre_completo="Carlos Soto", rol="SUPERVISOR")
    services.log_event(
        tipo_entidad="OBRA",
        id_entidad=104,
        accion="CAMBIO_ESTADO",
        usuario=usuario,
        estado_anterior="EN_PROCESO",
        estado_nuevo="FINALIZADA",
        motivo="Trabajos concluidos",
    )
    rows = selectors.list_logs("OBRA", 104)
    assert len(rows) == 1
    assert rows[0]["estado_nuevo"] == "FINALIZADA"
    assert rows[0]["usuario"]["rol"] == "SUPERVISOR"
    assert selectors.list_logs("OBRA", 999) == []
