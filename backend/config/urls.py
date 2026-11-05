from django.contrib import admin
from django.urls import include, path

# Cada app expone su propio urls.py. Se montan todas bajo /api/v1/.
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("", include("apps.common.urls")),
                path("", include("apps.accounts.urls")),
                path("", include("apps.clientes.urls")),
                path("", include("apps.presupuestos.urls")),
                path("", include("apps.obras.urls")),
                path("", include("apps.cobranzas.urls")),
                path("", include("apps.dashboard.urls")),
                path("", include("apps.reportes.urls")),
                path("", include("apps.audit.urls")),
            ]
        ),
    ),
]
