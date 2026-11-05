from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import roles as R
from apps.common.errors import DomainError
from apps.common.permissions import roles

from . import selectors


class AuditLogListView(APIView):
    """GET /api/v1/audit/logs/?tipo_entidad=OBRA&id_entidad=104 (Gerencia y Supervisor)."""

    permission_classes = [roles(R.GERENCIA, R.SUPERVISOR)]

    def get(self, request):
        tipo = request.query_params.get("tipo_entidad")
        id_entidad = request.query_params.get("id_entidad")
        if not tipo or not id_entidad or not id_entidad.isdigit():
            raise DomainError("PARAMETROS_INVALIDOS", "Indique tipo_entidad e id_entidad (número).", status_code=400)
        return Response({"results": selectors.list_logs(tipo, int(id_entidad))})
