SELECT codigo, descripcion, precio_usa, fuente, fecha_registro
FROM spo.precio_comparativo
WHERE precio_usa <>0 
ORDER BY fecha_registro DESC;
