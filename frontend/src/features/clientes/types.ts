export interface Cliente {
  id_cliente: number;
  rut: string;
  razon_social: string;
  contacto_nombre: string | null;
  telefono: string | null;
  email: string | null;
}
