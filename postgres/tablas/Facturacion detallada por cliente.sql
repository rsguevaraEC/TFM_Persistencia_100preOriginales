SELECT c.cli_nombre, c.cli_apellido , fc.fecha_factura , fd.inv_cod_fab , fd.cantidad, fd.precio_unitario
FROM spo.factura_cabecera fc
JOIN spo.clientes c ON fc.id_cliente = c.id_cliente
JOIN spo.factura_detalle fd ON fc.id_factura = fd.id_factura
WHERE c.cli_identificacion <> '1234567890';
