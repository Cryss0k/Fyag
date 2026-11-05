CREATE OR REPLACE VIEW vw_obras_por_tipo AS
SELECT ts.id_tipo_servicio, ts.nombre AS tipo_servicio, COUNT(o.id_obra) AS cantidad_obras
FROM tipos_servicio ts
LEFT JOIN obras o ON o.id_tipo_servicio = ts.id_tipo_servicio
GROUP BY ts.id_tipo_servicio, ts.nombre
ORDER BY ts.nombre;
