import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { ReportesPage } from "./pages/ReportesPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO", "SUPERVISOR"] as const;

export const feature: FeatureModule = {
  name: "reportes",
  routes: [
    {
      path: "/reportes",
      element: (
        <RequireRole roles={[...ROLES]}>
          <ReportesPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Reportes", path: "/reportes", roles: [...ROLES] }],
};
