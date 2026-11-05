# Decisiones de diseño

Los informes 1 y 2 se contradicen en estos puntos. Las columnas "Propuesta" vienen del Plan; el kickoff
las confirma o cambia. Cada decisión cerrada se anota con fecha y quién la aprobó.

| ID | Tema | Propuesta | Estado | Fecha / aprobó |
|---|---|---|---|---|
| D-01 | Quién aprueba un presupuesto | Gerencia aprueba o rechaza; Finanzas crea, edita y envía. Corregir CPF-03 y CPS-03 | Pendiente | |
| D-02 | Estados de la obra | Los del informe: EN_PROCESO, SUSPENDIDA, FINALIZADA, CANCELADA, más COBRADA (cierre automático, Informe 2 §4.1). Transiciones: EN_PROCESO → FINALIZADA o SUSPENDIDA; SUSPENDIDA → EN_PROCESO o CANCELADA; FINALIZADA → COBRADA. Regla N°1: crear la obra y reanudarla exigen al menos un técnico | **Decidida (5 nov)** | Equipo |
| D-03 | Técnicos por obra | Relación N:M (`obra_tecnicos`) | Pendiente | |
| D-04 | Ajustes al esquema v1 | `presupuesto_items`, `costos_obra`, folio/subtotal/IVA, ubicación y confirmación en obras, ANULADA en facturas, bloqueo de usuarios | Pendiente | |
| D-05 | Presupuesto → obra | La obra la crea el Supervisor; 1 presupuesto = máximo 1 obra. Reescribir CPI-01 y CPI-02 | Pendiente | |
| D-06 | Cierre por cobro | FINALIZADA pasa a COBRADA cuando todas las facturas no anuladas están pagadas y suman el monto del presupuesto | Pendiente | |
| D-07 | Auditoría | Mongo `audit_logs`; en desarrollo `AUDIT_BACKEND=log`; si falla, se revierte el cambio | Pendiente | |
| D-08 | Sesión | JWT de acceso de 1 h en memoria | Pendiente | |
| D-09 | Supervisor y presupuestos | El Supervisor SÍ accede a presupuestos: solo lectura y solo los APROBADOS (`GET /presupuestos/?estado=APROBADO&sin_obra=true`), para crear la ficha de obra. No puede crear, editar ni aprobar | **Decidida (5 nov)** | Equipo |

El Informe 2 prevalece sobre el Informe 1 (así lo declara su plan de pruebas).
