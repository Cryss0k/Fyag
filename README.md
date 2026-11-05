# Base de datos (dueño: Base de datos)

La **fuente de verdad ejecutable** son las migraciones de Django (`backend/apps/*/migrations`).
Esta carpeta guarda la referencia y lo que Django no genera solo.

| Carpeta | Contenido |
|---|---|
| `ddl/schema_v1.sql` | DDL de referencia del esquema v1 (con las decisiones D-02 a D-06). Sirve para revisar el modelo y para el ERD. |
| `views/` | Vistas SQL de solo lectura que consumen `dashboard` y `reportes`. Se aplican con una migración `RunSQL` en `apps/dashboard`. |
| `mongo/` | Esquema de validación e índices de las colecciones `audit_logs` y `adjuntos_obra`. |
| `backups/` | Scripts de respaldo y restauración (cifrados). Nunca subir respaldos reales al repositorio. |

Datos de prueba: `python manage.py seed_demo` (datos ficticios, ver `backend/apps/seeds`).

Cambios al esquema: abrir un issue con la plantilla **Solicitud de cambio de esquema** y avisar con 24 h.
