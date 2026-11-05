import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { ObrasPage } from "./pages/ObrasPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO", "SUPERVISOR"] as const;

export const feature: FeatureModule = {
  name: "obras",
  routes: [
    {
      path: "/obras",
      element: (
        <RequireRole roles={[...ROLES]}>
          <ObrasPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Obras", path: "/obras", roles: [...ROLES] }],
};
