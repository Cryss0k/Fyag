# Estado de los módulos (semáforo)

Verde = en fecha · Amarillo = atraso de hasta 2 días o riesgo identificado · Rojo = bloqueo de más de 48 h,
atraso de más de 3 días en la ruta crítica o persona sin responder 72 h (el Manager avisa al docente ese día).

| Módulo | Dueño | Respaldo | Estado | Nota | Actualizado |
|---|---|---|---|---|---|
| accounts (login, RBAC, usuarios) | Back 1 | Back 2 | 🟢 | | |
| clientes | Back 1 | Back 2 | 🟢 | | |
| presupuestos | Back 1 | Back 2 | 🟢 | | |
| obras | Back 2 | Back 1 | 🟢 | | |
| cobranzas | Back 2 | Back 1 | 🟢 | | |
| dashboard + reportes + BD | Base de datos | Manager | 🟢 | | |
| audit + plataforma + CI | Manager | Base de datos | 🟢 | | |
| frontend shell, auth, dashboard, reportes | Front 1 | Front 2 | 🟢 | | |
| frontend clientes, presupuestos, obras, cobranzas | Front 2 | Front 1 | 🟢 | | |
