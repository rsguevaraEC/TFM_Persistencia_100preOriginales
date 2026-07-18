-- DROP SCHEMA spo;

CREATE SCHEMA spo AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA spo IS 'standard public schema';

-- DROP SEQUENCE spo.clientes_id_cliente_seq;

CREATE SEQUENCE spo.clientes_id_cliente_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE spo.clientes_id_cliente_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE spo.clientes_id_cliente_seq TO postgres;

-- DROP SEQUENCE spo.factura_cabecera_id_factura_seq;

CREATE SEQUENCE spo.factura_cabecera_id_factura_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE spo.factura_cabecera_id_factura_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE spo.factura_cabecera_id_factura_seq TO postgres;

-- DROP SEQUENCE spo.factura_detalle_id_detalle_seq;

CREATE SEQUENCE spo.factura_detalle_id_detalle_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE spo.factura_detalle_id_detalle_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE spo.factura_detalle_id_detalle_seq TO postgres;

-- DROP SEQUENCE spo.leads_id_lead_seq;

CREATE SEQUENCE spo.leads_id_lead_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE spo.leads_id_lead_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE spo.leads_id_lead_seq TO postgres;

-- DROP SEQUENCE spo.precio_comparativo_id_precio_seq;

CREATE SEQUENCE spo.precio_comparativo_id_precio_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE spo.precio_comparativo_id_precio_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE spo.precio_comparativo_id_precio_seq TO postgres;
-- spo.clientes definition

-- Drop table

-- DROP TABLE spo.clientes;

CREATE TABLE spo.clientes ( id_cliente serial4 NOT NULL, cli_identificacion varchar(20) NOT NULL, cli_nombre varchar(100) NOT NULL, cli_apellido varchar(100) NULL, cli_email varchar(100) NULL, cli_telefono varchar(20) NULL, cli_direccion text NULL, cli_ciudad varchar(50) NULL, cli_pais varchar(50) NULL, cli_metadata jsonb NULL, fecha_registro timestamp DEFAULT now() NULL, CONSTRAINT clientes_cli_identificacion_key UNIQUE (cli_identificacion), CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente));

-- Permissions

ALTER TABLE spo.clientes OWNER TO postgres;
GRANT ALL ON TABLE spo.clientes TO postgres;


-- spo.conce definition

-- Drop table

-- DROP TABLE spo.conce;

CREATE TABLE spo.conce ( "Conce_Codigo" bpchar(6) NOT NULL, "Concesionario" varchar(100) NOT NULL, "Conce_Direccion" varchar(255) NULL, "Conce_Ciudad" bpchar(50) NULL, "Conce_ruc" bpchar(13) NOT NULL, "Conce_telefono" bpchar(12) NOT NULL, "Conce_cuenta_banco" bpchar(20) NOT NULL, "Conce_Activo" bool NOT NULL, "Conce_nombre_banco" bpchar(50) NOT NULL, "Conce_tipo_cuenta" bpchar(1) NULL, "Conce_pais" bpchar(50) NULL, contacto bpchar(50) NULL, movil int4 NULL, CONSTRAINT concesionarias_pkey PRIMARY KEY ("Conce_Codigo"));

-- Permissions

ALTER TABLE spo.conce OWNER TO postgres;
GRANT ALL ON TABLE spo.conce TO postgres;


-- spo.precio_comparativo definition

-- Drop table

-- DROP TABLE spo.precio_comparativo;

CREATE TABLE spo.precio_comparativo ( id_precio serial4 NOT NULL, codigo varchar(50) NOT NULL, descripcion text NULL, precio_usa numeric(10, 2) NULL, precio_partsgeek numeric(10, 2) NULL, fuente varchar(50) NULL, fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NULL, origen_datos varchar(50) NULL, metadata jsonb NULL, description varchar(50) NULL, CONSTRAINT precio_comparativo_pkey PRIMARY KEY (id_precio));

-- Permissions

ALTER TABLE spo.precio_comparativo OWNER TO postgres;
GRANT ALL ON TABLE spo.precio_comparativo TO postgres;


-- spo.preinvec definition

-- Drop table

-- DROP TABLE spo.preinvec;

CREATE TABLE spo.preinvec ( conce_codigo bpchar(6) NULL, inv_cod_fab varchar NULL, inv_cod_conc varchar NULL, inv_repuesto varchar NULL, inv_marca varchar NULL, inv_modelo_aplica varchar NULL, inv_anio_modelo varchar NULL, inv_cantidad int4 NULL, inv_precio_vta float8 NULL, inv_ubica_repu text NULL, inv_fecha_compra date NULL, inv_fecha_venta date NULL, inv_calificacion bpchar(25) NULL, fecha date NULL, inv_observacion varchar NULL, inv_costo float8 NULL, inv_precio_fabrica float8 NULL, inv_dscto float8 NULL, inv_costo_real float8 NULL, inv_margen_real float8 NULL);

-- Permissions

ALTER TABLE spo.preinvec OWNER TO postgres;
GRANT ALL ON TABLE spo.preinvec TO postgres;


-- spo.factura_cabecera definition

-- Drop table

-- DROP TABLE spo.factura_cabecera;

CREATE TABLE spo.factura_cabecera ( id_factura serial4 NOT NULL, id_cliente int4 NULL, fecha_factura date NOT NULL, metodo_pago varchar(30) NULL, estado varchar(20) DEFAULT 'pendiente'::character varying NULL, total numeric(10, 2) NULL, factura_json jsonb NULL, fecha_registro timestamp DEFAULT now() NULL, CONSTRAINT factura_cabecera_pkey PRIMARY KEY (id_factura), CONSTRAINT factura_cabecera_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES spo.clientes(id_cliente));

-- Permissions

ALTER TABLE spo.factura_cabecera OWNER TO postgres;
GRANT ALL ON TABLE spo.factura_cabecera TO postgres;


-- spo.factura_detalle definition

-- Drop table

-- DROP TABLE spo.factura_detalle;

CREATE TABLE spo.factura_detalle ( id_detalle serial4 NOT NULL, id_factura int4 NULL, inv_cod_fab varchar(50) NULL, cantidad int4 DEFAULT 1 NULL, precio_unitario numeric(10, 2) NULL, subtotal numeric(10, 2) NULL, impuestos numeric(10, 2) NULL, total numeric(10, 2) NULL, inv_repuesto varchar(50) NULL, CONSTRAINT factura_detalle_pkey PRIMARY KEY (id_detalle), CONSTRAINT factura_detalle_id_factura_fkey FOREIGN KEY (id_factura) REFERENCES spo.factura_cabecera(id_factura));

-- Permissions

ALTER TABLE spo.factura_detalle OWNER TO postgres;
GRANT ALL ON TABLE spo.factura_detalle TO postgres;


-- spo.invec definition

-- Drop table

-- DROP TABLE spo.invec;

CREATE TABLE spo.invec ( conce_codigo bpchar(6) NOT NULL, inv_cod_fab varchar NOT NULL, inv_cod_conc varchar NULL, inv_repuesto varchar NOT NULL, inv_marca varchar NOT NULL, inv_modelo_aplica varchar NOT NULL, inv_anio_modelo varchar NULL, inv_cantidad int4 NULL, inv_precio_vta float8 NULL, inv_ubica_repu text NULL, inv_fecha_compra date NULL, inv_fecha_venta date NULL, inv_calificacion bpchar(25) NULL, fecha date NOT NULL, inv_observacion varchar NULL, inv_costo float8 NULL, inv_precio_fabrica float8 NULL, inv_dscto float8 NULL, inv_costo_real float8 NULL, inv_margen_real float8 NULL, inv_refe varchar(20) NULL, CONSTRAINT "Inventarios_pkey" PRIMARY KEY (conce_codigo, inv_cod_fab, fecha), CONSTRAINT fk_invec_conce FOREIGN KEY (conce_codigo) REFERENCES spo.conce("Conce_Codigo") ON DELETE RESTRICT ON UPDATE CASCADE);
COMMENT ON TABLE spo.invec IS 'Tiene los inventarios de los concesionarios';

-- Permissions

ALTER TABLE spo.invec OWNER TO postgres;
GRANT ALL ON TABLE spo.invec TO postgres;


-- spo.leads definition

-- Drop table

-- DROP TABLE spo.leads;

CREATE TABLE spo.leads ( id_lead serial4 NOT NULL, lead_identificacion varchar(20) NULL, lead_nombre varchar(100) NULL, lead_apellido varchar(100) NULL, lead_email varchar(150) NULL, lead_telefono varchar(20) NULL, lead_direccion varchar(255) NULL, lead_ciudad varchar(100) NULL, lead_pais varchar(100) NULL, lead_fuente varchar(50) NULL, lead_estado varchar(30) DEFAULT 'prospecto'::character varying NULL, lead_metadata jsonb NULL, lead_contexto jsonb NULL, fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NULL, id_cliente int4 NULL, fecha_actualizacion timestamp DEFAULT CURRENT_TIMESTAMP NULL, CONSTRAINT leads_pkey PRIMARY KEY (id_lead), CONSTRAINT leads_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES spo.clientes(id_cliente) ON DELETE SET NULL ON UPDATE CASCADE);
CREATE INDEX idx_leads_estado_fuente ON spo.leads USING btree (lead_estado, lead_fuente);

-- Permissions

ALTER TABLE spo.leads OWNER TO postgres;
GRANT ALL ON TABLE spo.leads TO postgres;


-- spo.v_leads_clientes source

CREATE OR REPLACE VIEW spo.v_leads_clientes
AS SELECT l.id_lead,
    l.lead_nombre,
    l.lead_fuente,
    l.lead_estado,
    c.cli_nombre,
    c.cli_email,
    c.cli_ciudad
   FROM spo.leads l
     LEFT JOIN spo.clientes c ON l.id_cliente = c.id_cliente;

-- Permissions

ALTER TABLE spo.v_leads_clientes OWNER TO postgres;
GRANT ALL ON TABLE spo.v_leads_clientes TO postgres;




-- Permissions

GRANT ALL ON SCHEMA spo TO pg_database_owner;