import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import type { Rol } from "@/shared/types/roles";
import { useAuth } from "./AuthContext";

/** Guarda de ruta por rol. El servidor sigue siendo la autoridad: esto solo mejora la experiencia. */
export function RequireRole({ roles, children }: { roles: Rol[]; children: ReactNode }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (!roles.includes(user.rol)) return <Navigate to="/" replace />;
  return <>{children}</>;
}
