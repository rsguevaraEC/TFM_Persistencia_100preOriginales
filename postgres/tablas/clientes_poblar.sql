\copy spo.clientes (
    cli_identificacion,
    cli_nombre,
    cli_apellido,
    cli_email,
    cli_telefono,
    cli_direccion,
    cli_ciudad,
    cli_pais
)
FROM 'C:\Users\Asus\OneDrive\Isabel I\TFM_Persistencia_100preOriginales\proyecto\postgres\datos\clientes.csv'
DELIMITER ','
CSV HEADER;
