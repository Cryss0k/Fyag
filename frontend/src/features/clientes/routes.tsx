import { RequireRole } from "@/shared/auth/RequireRole";
import type { FeatureModule } from "@/shared/types/feature";
import { ClientesPage } from "./pages/ClientesPage";

const ROLES = ["GERENCIA", "ADMINISTRATIVO"] as const;

export const feature: FeatureModule = {
  name: "clientes",
  routes: [
    {
      path: "/clientes",
      element: (
        <RequireRole roles={[...ROLES]}>
          <ClientesPage />
        </RequireRole>
      ),
    },
  ],
  nav: [{ label: "Clientes", path: "/clientes", roles: [...ROLES] }],
};
