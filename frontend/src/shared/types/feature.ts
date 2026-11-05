import type { RouteObject } from "react-router-dom";
import type { Rol } from "./roles";

export interface NavItem {
  label: string;
  path: string;
  roles: Rol[];
}

/** Lo que cada feature exporta como `feature` desde su index.ts. El shell las registra solo. */
export interface FeatureModule {
  name: string;
  /** true = ruta pública (fuera del layout con sesión), p. ej. el login */
  public?: boolean;
  routes: RouteObject[];
  nav?: NavItem[];
}
