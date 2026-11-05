// Vista del Técnico: este tipo NO tiene campos de monto a propósito (HDU-02).
export interface ObraAsignada {
  id_obra: number;
  nombre_obra: string;
  tipo_servicio: string;
  ubicacion: string;
  fecha_inicio: string;
  fecha_fin_estimada: string | null;
  estado_operativo: string;
}
