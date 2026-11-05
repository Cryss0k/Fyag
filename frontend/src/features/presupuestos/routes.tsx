import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { PresupuestosPage } from "./pages/PresupuestosPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO"] as const;

export const feature: FeatureModule = {
  name: "presupuestos",
  routes: [
    {
      path: "/presupuestos",
      element: (
        <RequireRole roles={[...ROLES]}>
          <PresupuestosPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Presupuestos", path: "/presupuestos", roles: [...ROLES] }],
};
