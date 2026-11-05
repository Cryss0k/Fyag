-- "Vencida" se calcula (no se guarda): pendiente con fecha de vencimiento pasada.
CREATE OR REPLACE VIEW vw_cobranzas_pendientes AS
SELECT f.id_factura, f.numero_factura, f.monto, f.fecha_emision, f.fecha_vencimiento,
       (f.fecha_vencimiento < CURRENT_DATE) AS vencida,
       o.id_obra, o.nombre_obra, c.id_cliente, c.razon_social
FROM facturas f
JOIN obras o        ON o.id_obra = f.id_obra
JOIN presupuestos p ON p.id_presupuesto = o.id_presupuesto
JOIN clientes c     ON c.id_cliente = p.id_cliente
WHERE f.estado_pago = 'PENDIENTE';
