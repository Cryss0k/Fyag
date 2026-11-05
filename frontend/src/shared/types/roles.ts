export const ROLES = ["GERENCIA", "ADMINISTRATIVO", "SUPERVISOR", "TECNICO"] as const;
export type Rol = (typeof ROLES)[number];
