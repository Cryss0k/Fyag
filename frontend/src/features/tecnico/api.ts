import { api } from "@/shared/api/client";
import type { Paginated } from "@/shared/types/api";
import type { ObraAsignada } from "./types";

export const listMisObras = () => api<Paginated<ObraAsignada>>("/obras/mis-obras/");
