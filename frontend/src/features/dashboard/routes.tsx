import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { DashboardPage } from "./pages/DashboardPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO", "SUPERVISOR"] as const;

export const feature: FeatureModule = {
  name: "dashboard",
  routes: [
    {
      path: "/dashboard",
      element: (
        <RequireRole roles={[...ROLES]}>
          <DashboardPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Dashboard", path: "/dashboard", roles: [...ROLES] }],
};
