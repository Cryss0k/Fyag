import type { FeatureModule } from "@/shared/types/feature";

// Registro automático: toda carpeta src/features/<nombre>/index.ts que exporte `feature` se monta sola.
// Agregar o quitar una feature no obliga a tocar este archivo.
const modules = import.meta.glob<{ feature: FeatureModule }>("/src/features/*/index.ts", { eager: true });

export const features: FeatureModule[] = Object.values(modules).map((mod) => mod.feature);
