Sistema de Persistencia del TFM “100preOriginales”

Este repositorio contiene el desarrollo técnico del sistema de persistencia. Incluye el modelo físico en PostgreSQL, los datasets iniciales, los scripts de ingesta de datos externos y la documentación necesaria para reproducir el entorno en local.

El objetivo del repositorio es garantizar que cualquier evaluador pueda 
levantar el sistema sin dependencias externas, validar el modelo y ejecutar las consultas representativas del MVP.

?? Estructura del repositorio

proyecto/
?
??? docker/                 # Preparación para futura dockerización
?   ??? init/
?
??? docs/                   # Documentación técnica
?   ??? postgres - spo.png  # Diagrama ER exportado desde DBeaver
?
??? ingestion/              # Scripts de ingesta de datos externos
?   ??? api_prices/         # Ingesta desde API (eBay)
?   ??? web_scraping/       # Scraping desde PartsGeek
?   ??? readme ingestion.md # README específico del módulo de ingesta
?
??? postgres/               # Capa de persistencia en PostgreSQL
?   ??? ddl/                # Modelo físico completo (DDL)
?   ?   ??? spo_schema.sql
?   ??? datos/              # Datasets iniciales (CSV)
?   ?   ??? clientes.csv
?   ??? tablas/         # Consultas representativas y scripts auxiliares
?   ??? json/               # Espacio reservado para metadatos JSON
?
??? requirements.txt        # Dependencias Python para ingesta
??? README.md               # README principal (este archivo)

?? 1. Requisitos previos
Para ejecutar el sistema en local se necesita:
* PostgreSQL 14+
* Python 3.10+
* DBeaver (opcional, para visualizar el modelo)
* Librerías Python:

pip install -r requirements.txt


?? 2. Crear la base de datos
1. Abrir PostgreSQL (psql o PgAdmin).
2. Crear una base de datos vacía:

	CREATE DATABASE spo_db;
3. Ejecutar el script DDL:

	psql -d spo_db -f postgres/ddl/spo_schema.sql

Esto creará:
* el esquema spo,
* todas las tablas del MVP,
* secuencias,
* claves primarias y foráneas,
* índices,
* vistas auxiliares.

?? 3. Cargar datos iniciales (CSV)
Ejemplo para cargar clientes:

	\copy spo.clientes FROM 'postgres/datos/clientes.csv' CSV HEADER;
Los demás scripts de carga y consultas están en:

postgres/tablas/

?? 4. Ingesta de datos externos (API y scraping)

a) Precios desde eBay (API)
Ejecutar:

python ingestion/api_prices/ingesta_ebay.py
Esto:
* consulta la API,
* normaliza los datos,
* genera precios_ebay.csv,
* inserta registros en spo.precio_comparativo.

b) Precios desde PartsGeek (scraping)
Ejecutar:
bash
python ingestion/web_scraping/Importa partsgeek.py
Esto genera:
* precios_partsgeek.csv,
* registros listos para inserción en PostgreSQL.

?? 5. Consultas representativas
Las consultas del MVP están en:

postgres/tablas/
Incluyen:
* Leads por estado
* Inventario por concesionario
* Facturación detallada por cliente
* Comparación de precios externos
Estas consultas permiten validar el funcionamiento del modelo.

?? 6. Visualización del modelo
El diagrama ER se encuentra en:

docs/postgres - spo.png
Representa:
* entidades principales,
* relaciones,
* claves primarias y foráneas,
* vistas auxiliares.

? 7. Reproducibilidad
El sistema puede levantarse completamente en local siguiendo estos pasos:
1. Crear la base de datos.
2. Ejecutar el DDL.
3. Cargar los CSV.
4. Ejecutar los scripts de ingesta.
5. Validar con las consultas representativas.
No se requieren servicios externos, licencias privativas ni dependencias en la nube.


