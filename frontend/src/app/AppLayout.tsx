import { NavLink, Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/shared/auth/AuthContext";
import { features } from "./features";

/** Layout con sesión: menú según el rol (solo muestra lo que el rol puede usar). */
export function AppLayout() {
  const { user, logout } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  const items = features.flatMap((f) => f.nav ?? []).filter((item) => item.roles.includes(user.rol));

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="flex items-center justify-between bg-brand-600 px-4 py-3 text-white">
        <span className="font-semibold">FYAG</span>
        <div className="flex items-center gap-3 text-sm">
          <span>
            {user.nombre} · {user.rol}
          </span>
          <button type="button" onClick={logout} className="rounded bg-brand-700 px-2 py-1">
            Salir
          </button>
        </div>
      </header>
      <div className="flex flex-col md:flex-row">
        <nav className="flex gap-2 overflow-x-auto bg-white p-3 md:w-56 md:flex-col">
          {items.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `rounded px-3 py-2 text-sm ${isActive ? "bg-brand-50 font-medium text-brand-700" : "text-slate-600"}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <main className="flex-1 p-4">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
