import { tokenStore } from "@/shared/auth/tokenStore";
import type { ApiErrorBody } from "@/shared/types/api";

const BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export class ApiError extends Error {
  status: number;
  code: string;
  details: unknown;

  constructor(status: number, code: string, message: string, details: unknown = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

type Query = Record<string, string | number | boolean | undefined>;

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  body?: unknown;
  query?: Query;
  signal?: AbortSignal;
}

function buildUrl(path: string, query?: Query): string {
  const params = new URLSearchParams();
  Object.entries(query ?? {}).forEach(([key, value]) => {
    if (value !== undefined && value !== "") params.set(key, String(value));
  });
  const qs = params.toString();
  return `${BASE_URL}${path}${qs ? `?${qs}` : ""}`;
}

function authHeaders(): Record<string, string> {
  const token = tokenStore.getToken();
  if (token) return { Authorization: `Bearer ${token}` };
  const devRole = tokenStore.getDevRole();
  if (devRole && import.meta.env.DEV) return { "X-Dev-Role": devRole };
  return {};
}

async function send(path: string, opts: RequestOptions): Promise<Response> {
  const response = await fetch(buildUrl(path, opts.query), {
    method: opts.method ?? "GET",
    headers: {
      ...(opts.body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...authHeaders(),
    },
    body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
    signal: opts.signal,
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as ApiErrorBody | null;
    throw new ApiError(
      response.status,
      body?.error?.code ?? "ERROR",
      body?.error?.message ?? "Error en la solicitud",
      body?.error?.details,
    );
  }
  return response;
}

/** Llamada JSON a la API. Las rutas llevan barra final: api("/clientes/"). */
export async function api<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const response = await send(path, opts);
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

/** Descarga de archivos (PDF, Excel): apiBlob("/reportes/obras/", { query: { formato: "xlsx" } }). */
export async function apiBlob(path: string, opts: RequestOptions = {}): Promise<Blob> {
  return (await send(path, opts)).blob();
}
