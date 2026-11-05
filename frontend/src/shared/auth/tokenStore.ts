/**
 * El token de acceso vive SOLO en memoria (Normas §7.7): no se guarda en localStorage.
 * devRole es para desarrollo local con el backend en modo DEV_AUTH (cabecera X-Dev-Role).
 */
let accessToken: string | null = null;
let devRole: string | null = import.meta.env.VITE_DEV_ROLE || null;

export const tokenStore = {
  getToken: () => accessToken,
  setToken: (token: string | null) => {
    accessToken = token;
  },
  getDevRole: () => devRole,
  setDevRole: (rol: string | null) => {
    devRole = rol;
  },
};
