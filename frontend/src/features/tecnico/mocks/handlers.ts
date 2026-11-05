import { http, HttpResponse, type RequestHandler } from "msw";
import misObras from "@contracts/examples/mis_obras.json";

export const handlers: RequestHandler[] = [
  http.get("/api/v1/obras/mis-obras/", () => HttpResponse.json(misObras)),
];
