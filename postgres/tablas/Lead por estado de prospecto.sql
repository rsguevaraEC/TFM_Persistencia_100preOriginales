SELECT l.lead_nombre, l.lead_apellido , l.lead_estado, l.fecha_registro as fecha
FROM spo.leads l
WHERE l.lead_estado = 'contactado' or l.lead_estado= 'interesado'
ORDER BY fecha DESC;
