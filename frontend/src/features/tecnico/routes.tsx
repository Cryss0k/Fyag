import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { MisObrasPage } from "./pages/MisObrasPage";

const ROLES = ["TECNICO"] as const;

export const feature: FeatureModule = {
  name: "tecnico",
  routes: [
    {
      path: "/mis-obras",
      element: (
        <RequireRole roles={[...ROLES]}>
          <MisObrasPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Mis obras", path: "/mis-obras", roles: [...ROLES] }],
};
