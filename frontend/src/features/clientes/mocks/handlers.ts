import { http, HttpResponse, type RequestHandler } from "msw";
import clientes from "@contracts/examples/clientes_list.json";

export const handlers: RequestHandler[] = [
  http.get("/api/v1/clientes/", () => HttpResponse.json(clientes)),
];
