-- KPIs de la HDU-08: ventas del mes, por cobrar, obras activas y presupuestos aprobados/rechazados.
CREATE OR REPLACE VIEW vw_kpis_mes AS
SELECT
    COALESCE((SELECT SUM(monto) FROM facturas
              WHERE estado_pago <> 'ANULADA'
                AND date_trunc('month', fecha_emision) = date_trunc('month', CURRENT_DATE)), 0) AS ventas_facturadas_mes,
    COALESCE((SELECT SUM(monto) FROM facturas WHERE estado_pago = 'PENDIENTE'), 0)               AS por_cobrar,
    (SELECT COUNT(*) FROM obras WHERE estado_operativo = 'EN_PROCESO')                           AS obras_en_proceso,
    (SELECT COUNT(*) FROM presupuestos WHERE estado = 'APROBADO')                                AS presupuestos_aprobados,
    (SELECT COUNT(*) FROM presupuestos WHERE estado = 'RECHAZADO')                               AS presupuestos_rechazados;
