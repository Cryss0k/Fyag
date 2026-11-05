import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { Rol } from "@/shared/types/roles";
import { tokenStore } from "./tokenStore";

export interface SessionUser {
  nombre: string;
  rol: Rol;
}

interface AuthValue {
  user: SessionUser | null;
  setUser: (user: SessionUser | null) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthValue | null>(null);

// Front 1: reemplazar por la sesión real (login contra /auth/login/ y /auth/me/).
export function AuthProvider({ children }: { children: ReactNode }) {
  const devRole = import.meta.env.VITE_DEV_ROLE as Rol | undefined;
  const [user, setUser] = useState<SessionUser | null>(
    devRole ? { nombre: `Dev ${devRole}`, rol: devRole } : null,
  );

  const value = useMemo<AuthValue>(
    () => ({
      user,
      setUser,
      logout: () => {
        tokenStore.setToken(null);
        tokenStore.setDevRole(null);
        setUser(null);
      },
    }),
    [user],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <AuthProvider>");
  return ctx;
}
