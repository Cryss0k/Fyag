"""obras — services. Dueño: Back 2.

Interfaz pública del módulo. Los cambios de estado pasan SIEMPRE por transition_state().
Estados oficiales (Informe 1 HDU-06 e Informe 2, diagrama 4.7 y CPF-09 a CPF-15):
EN_PROCESO, FINALIZADA, SUSPENDIDA, CANCELADA y COBRADA (cierre automático al cobrar el 100 %).

Reglas que NO caben en la tabla y las valida transition_state():
  N°1  Una obra solo puede estar EN_PROCESO con al menos un técnico asignado. Por eso crear una obra
       exige al menos un técnico (nace EN_PROCESO) y reanudar una SUSPENDIDA también lo exige.
  N°2  No se puede pasar a CANCELADA si la obra ya tiene facturas o abonos registrados.
  N°3  No se puede pasar a FINALIZADA sin la confirmación de ejecución del supervisor.
  D-06 FINALIZADA pasa a COBRADA sola cuando todas sus facturas no anuladas están pagadas.
"""

from .models import EstadoObra

E = EstadoObra

TRANSITIONS: dict[str, set[str]] = {
    E.EN_PROCESO: {E.FINALIZADA, E.SUSPENDIDA},  # FINALIZADA exige confirmación del supervisor (regla N°3)
    E.SUSPENDIDA: {E.EN_PROCESO, E.CANCELADA},  # EN_PROCESO exige técnico (N°1); CANCELADA sin facturas (N°2)
    E.FINALIZADA: {E.COBRADA},  # automático al pagar el 100 % (D-06)
    E.CANCELADA: set(),
    E.COBRADA: set(),
}


def is_transition_allowed(desde: str, hacia: str) -> bool:
    return hacia in TRANSITIONS.get(desde, set())


def transition_state(obra, hacia: str, usuario, motivo: str = ""):
    """TODO (Back 2): validar is_transition_allowed y las reglas N°1, N°2 y N°3 lanzando
    DomainError(code=..., message=...), cambiar el estado dentro de transaction.atomic() y,
    como último paso del bloque, llamar a audit.services.log_event(...)."""
    raise NotImplementedError("Back 2: implementar transition_state()")
