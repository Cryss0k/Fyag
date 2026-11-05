import { useNavigate } from "react-router-dom";
import { useAuth } from "@/shared/auth/AuthContext";
import { tokenStore } from "@/shared/auth/tokenStore";
import { ROLES } from "@/shared/types/roles";

/**
 * Pantalla de login PROVISORIA (Front 1): permite elegir un rol de desarrollo para probar la
 * navegación sin backend. Reemplazar por el formulario real (correo + contraseña) en el Sprint 1.
 */
export function LoginPage() {
  const { setUser } = useAuth();
  const navigate = useNavigate();

  return (
    <main className="mx-auto mt-24 max-w-sm rounded-lg bg-white p-6 shadow">
      <h1 className="mb-4 text-xl font-semibold">FYAG — Ingreso (modo desarrollo)</h1>
      <div className="flex flex-col gap-2">
        {ROLES.map((rol) => (
          <button
            key={rol}
            type="button"
            className="rounded bg-brand-600 px-3 py-2 text-white"
            onClick={() => {
              tokenStore.setDevRole(rol);
              setUser({ nombre: `Dev ${rol}`, rol });
              navigate("/");
            }}
          >
            Entrar como {rol}
          </button>
        ))}
      </div>
    </main>
  );
}
