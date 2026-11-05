import type { RequestHandler } from "msw";

/**
 * Cada feature define sus mocks en features/<nombre>/mocks/handlers.ts (export const handlers).
 * Se activan con VITE_USE_MOCKS_<NOMBRE>=true en .env.local, de modo que cada módulo pasa a la API
 * real por separado.
 */
const modules = import.meta.glob<{ handlers: RequestHandler[] }>("/src/features/*/mocks/handlers.ts", {
  eager: true,
});

function enabled(feature: string): boolean {
  const env = import.meta.env as unknown as Record<string, string | undefined>;
  return env[`VITE_USE_MOCKS_${feature.toUpperCase()}`] === "true";
}

export async function startMocks(): Promise<void> {
  const handlers = Object.entries(modules)
    .filter(([path]) => enabled(path.split("/")[3]))
    .flatMap(([, mod]) => mod.handlers);
  if (handlers.length === 0) return;
  const { setupWorker } = await import("msw/browser");
  await setupWorker(...handlers).start({ onUnhandledRequest: "bypass" });
}
