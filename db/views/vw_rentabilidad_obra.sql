-- Rentabilidad = facturado (no anulado) - costos registrados (CPI-05).
CREATE OR REPLACE VIEW vw_rentabilidad_obra AS
SELECT o.id_obra, o.nombre_obra,
       COALESCE(fa.facturado, 0)                       AS facturado,
       COALESCE(co.costos, 0)                          AS costos,
       COALESCE(fa.facturado, 0) - COALESCE(co.costos, 0) AS rentabilidad
FROM obras o
LEFT JOIN (SELECT id_obra, SUM(monto) AS facturado FROM facturas WHERE estado_pago <> 'ANULADA' GROUP BY id_obra) fa
       ON fa.id_obra = o.id_obra
LEFT JOIN (SELECT id_obra, SUM(monto) AS costos FROM costos_obra GROUP BY id_obra) co
       ON co.id_obra = o.id_obra;
