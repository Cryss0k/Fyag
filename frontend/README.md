# Frontend (React 19 + TypeScript + Vite + Tailwind 4)

```bash
cd frontend
pnpm install
cp .env.example .env.local
pnpm dlx msw init public/ --save   # una sola vez: crea public/mockServiceWorker.js (subirlo al repo)
pnpm dev                           # http://localhost:5173
```

Sin backend: con `VITE_USE_MOCKS_*=true` cada feature usa sus datos simulados. En `/login` elige un rol de
desarrollo para ver el menú de cada perfil.

## Cómo está organizado

```
src/
├─ app/        shell: router, layout y registro automático de features (Front 1)
├─ shared/     api/client.ts, auth/, mocks/, types/, ui-kit/ (Front 1)
├─ features/   una carpeta por módulo; NO se importan entre sí
│  └─ <nombre>/  index.ts, routes.tsx, api.ts, types.ts, pages/, components/, hooks/, mocks/handlers.ts
└─ prototype/  tu prototipo de Figma Make, como referencia (excluido de tsc y eslint; se va vaciando)
```

- Una feature **solo importa de `shared/`** y de sí misma con rutas relativas. ESLint lo exige.
- Para **agregar una feature**: crear `src/features/<nombre>/` con `index.ts` que exporte `feature`. El shell la monta sola.
- Para **pasar una feature a la API real**: `VITE_USE_MOCKS_<NOMBRE>=false` en `.env.local`.
- Las rutas de la API llevan barra final: `api("/clientes/")`.
- El perfil Técnico usa tipos **sin campos de monto** (`features/tecnico/types.ts`).

## Migrar tu prototipo (`figmaxvscode`)

1. Copia el contenido de la carpeta `src/` del prototipo a `frontend/src/prototype/`.
2. Si el prototipo usa CSS propio de Tailwind o fuentes, pásalos a `src/index.css` (tokens en `@theme`).
3. Mueve cada pantalla a su feature (por ejemplo, las de clientes a `features/clientes/pages/`) y reemplaza sus
   datos simulados internos por llamadas a `api.ts` + mocks MSW.
4. Cuando `src/prototype/` quede vacío, bórralo.

## Pendiente del Sprint 0 (Front 1)

```bash
# Pruebas: instalar y fijar versiones compatibles con tu Vite
pnpm add -D vitest jsdom @testing-library/react @testing-library/jest-dom
pnpm pkg set scripts.test="vitest run"
```

Después de `pnpm install`, sube `pnpm-lock.yaml` (el CI lo usará con `--frozen-lockfile`).
Borra `package-lock.json` del prototipo: usamos solo pnpm.
