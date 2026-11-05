import { api } from "@/shared/api/client";
import type { Paginated } from "@/shared/types/api";
import type { Cliente } from "./types";

export const listClientes = (search?: string) =>
  api<Paginated<Cliente>>("/clientes/", { query: { search } });
