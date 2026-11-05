import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { UsuariosPage } from "./pages/UsuariosPage";

const ROLES = ["GERENCIA"] as const;

export const feature: FeatureModule = {
  name: "usuarios",
  routes: [
    {
      path: "/usuarios",
      element: (
        <RequireRole roles={[...ROLES]}>
          <UsuariosPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Usuarios", path: "/usuarios", roles: [...ROLES] }],
};
