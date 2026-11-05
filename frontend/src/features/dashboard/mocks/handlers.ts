import { http, HttpResponse, type RequestHandler } from "msw";
import kpis from "@contracts/examples/kpis.json";

export const handlers: RequestHandler[] = [
  http.get("/api/v1/dashboard/kpis/", () => HttpResponse.json(kpis)),
];
