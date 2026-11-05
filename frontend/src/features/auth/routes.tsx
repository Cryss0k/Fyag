import type { FeatureModule } from "@/shared/types/feature";
import { LoginPage } from "./pages/LoginPage";

export const feature: FeatureModule = {
  name: "auth",
  public: true,
  routes: [{ path: "/login", element: <LoginPage /> }],
};
