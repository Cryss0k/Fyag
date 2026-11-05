CREATE OR REPLACE VIEW vw_facturacion_mensual AS
SELECT date_trunc('month', fecha_emision)::date AS mes,
       SUM(monto)                               AS total_facturado,
       SUM(monto) FILTER (WHERE estado_pago = 'PAGADO') AS total_pagado
FROM facturas
WHERE estado_pago <> 'ANULADA'
GROUP BY 1
ORDER BY 1;
