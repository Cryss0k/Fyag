import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { CobranzasPage } from "./pages/CobranzasPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO"] as const;

export const feature: FeatureModule = {
  name: "cobranzas",
  routes: [
    {
      path: "/cobranzas",
      element: (
        <RequireRole roles={[...ROLES]}>
          <CobranzasPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Cobranzas", path: "/cobranzas", roles: [...ROLES] }],
};
