SELECT con."Concesionario" , i.conce_codigo codigo, i.inv_repuesto ,i.inv_costo as costo,  i.inv_precio_vta as pvp
FROM spo.invec i
JOIN spo.conce con ON i.conce_codigo = con."Conce_Codigo"
WHERE i.inv_marca <> 'MULTIMARCA';
