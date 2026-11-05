# Contratos de API

Un archivo OpenAPI por módulo. **Contrato primero:** el dueño completa los schemas y publica los
ejemplos JSON a más tardar el **domingo 8 de noviembre**; después solo se aceptan cambios aditivos
(un cambio que rompe compatibilidad se avisa con 48 h y lo aprueba el Manager).

| Archivo | Dueño |
|---|---|
| `accounts.yaml`, `clientes.yaml`, `presupuestos.yaml` | Back 1 |
| `obras.yaml`, `cobranzas.yaml` | Back 2 |
| `dashboard.yaml`, `reportes.yaml` | Base de datos |
| `audit.yaml` | Manager |

- `x-roles` indica quién puede llamar a cada endpoint (RBAC). Sin `x-roles` válido, el PR no se aprueba.
- `examples/` guarda respuestas de ejemplo. El frontend las usa como datos simulados (MSW, alias `@contracts`).
- Los errores siempre tienen la forma `{"error": {"code", "message", "details"}}`.
- El PR que cambia un endpoint actualiza su contrato en el mismo PR.
