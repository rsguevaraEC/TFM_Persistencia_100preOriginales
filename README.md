Sistema de Persistencia del TFM ‚Äú100preOriginales‚Äù

Este repositorio contiene el desarrollo t√©cnico del sistema de persistencia. Incluye el modelo f√≠sico en PostgreSQL, los datasets iniciales, los scripts de ingesta de datos externos y la documentaci√≥n necesaria para reproducir el entorno en local.

El objetivo del repositorio es garantizar que cualquier evaluador pueda 
levantar el sistema sin dependencias externas, validar el modelo y ejecutar las consultas representativas del MVP.

<<<<<<< HEAD
Estructura del repositorio:

proyecto/
|
+--docker/                 # PreparaciÛn para futura dockerizaciÛn
|   +-init/
|
+--docs/                   # DocumentaciÛn tÈcnica
|   +- postgres - spo.png  # Diagrama ER exportado desde DBeaver
|
+-- ingestion/              # Scripts de ingesta de datos externos
|   +- api_prices/         # Ingesta desde API (eBay)
|   +- web_scraping/       # Scraping desde PartsGeek
|   +- readme ingestion.md # README especÌfico del mÛdulo de ingesta
|
+-- postgres/               # Capa de persistencia en PostgreSQL
|   +- ddl/                # Modelo fÌsico completo (DDL)
|   |   +- spo_schema.sql
|   +- datos/              # Datasets iniciales (CSV)
|   |   +- clientes.csv
|   +- tablas/         # Consultas representativas y scripts auxiliares
|   +- json/               # Espacio reservado para metadatos JSON
|
+-- requirements.txt        # Dependencias Python para ingesta
+-- README.md               # README principal (este archivo)
=======
Estructura del repositorio

proyecto/
|
??? docker/                 # Preparaci√≥n para futura dockerizaci√≥n
?   ??? init/
?
??? docs/                   # Documentaci√≥n t√©cnica
?   ??? postgres - spo.png  # Diagrama ER exportado desde DBeaver
?
??? ingestion/              # Scripts de ingesta de datos externos
?   ??? api_prices/         # Ingesta desde API (eBay)
?   ??? web_scraping/       # Scraping desde PartsGeek
?   ??? readme ingestion.md # README espec√≠fico del m√≥dulo de ingesta
?
??? postgres/               # Capa de persistencia en PostgreSQL
?   ??? ddl/                # Modelo f√≠sico completo (DDL)
?   ?   ??? spo_schema.sql
?   ??? datos/              # Datasets iniciales (CSV)
?   ?   ??? clientes.csv
?   ??? tablas/         # Consultas representativas y scripts auxiliares
?   ??? json/               # Espacio reservado para metadatos JSON
?
??? requirements.txt        # Dependencias Python para ingesta
??? README.md               # README principal (este archivo)
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16

1. Requisitos previos
Para ejecutar el sistema en local se necesita:
<<<<<<< HEAD
- PostgreSQL 14+
- Python 3.10+
- DBeaver (opcional, para visualizar el modelo)
- LibrerÌas Python:
=======
* PostgreSQL 14+
* Python 3.10+
* DBeaver (opcional, para visualizar el modelo)
* Librer√≠as Python:
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16

pip install -r requirements.txt


<<<<<<< HEAD
2. Crear la base de datos
	2.1  Abrir PostgreSQL (psql o PgAdmin).
	2.2 Crear una base de datos vacÌa:
		CREATE DATABASE spo_db;
	2.3 Ejecutar el script DDL:
		psql -d spo_db -f postgres/ddl/spo_schema.sql

Esto crear·:
	- el esquema spo,
	- todas las tablas del MVP,
	- secuencias,
	- claves primarias y for·neas,
	- Ìndices,
	- vistas auxiliares.
=======
?? 2. Crear la base de datos
1. Abrir PostgreSQL (psql o PgAdmin).
2. Crear una base de datos vac√≠a:

	CREATE DATABASE spo_db;
3. Ejecutar el script DDL:

	psql -d spo_db -f postgres/ddl/spo_schema.sql

Esto crear√°:
* el esquema spo,
* todas las tablas del MVP,
* secuencias,
* claves primarias y for√°neas,
* √≠ndices,
* vistas auxiliares.
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16

3. Cargar datos iniciales (CSV)
Ejemplo para cargar clientes:
	\copy spo.clientes FROM 'postgres/datos/clientes.csv' CSV HEADER;
<<<<<<< HEAD
Los dem·s scripts de carga y consultas est·n en:
	postgres/tablas/
=======
Los dem√°s scripts de carga y consultas est√°n en:
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16

4. Ingesta de datos externos (API y scraping)

	a) Precios desde eBay (API)
	Ejecutar:

	python ingestion/api_prices/ingesta_ebay.py
	Esto:
	- consulta la API,
	- normaliza los datos,
	- genera precios_ebay.csv,
	- inserta registros en spo.precio_comparativo.

	b) Precios desde PartsGeek (scraping)
	Ejecutar:
	python ingestion/web_scraping/Importa partsgeek.py
	Esto genera:
	- precios_partsgeek.csv,
	- registros listos para inserciÛn en PostgreSQL.

<<<<<<< HEAD
5. Consultas representativas
Las consultas del MVP est·n en:

postgres/tablas/
Incluyen:
- Leads por estado
- Inventario por concesionario
- FacturaciÛn detallada por cliente
- ComparaciÛn de precios externos
Estas consultas permiten validar el funcionamiento del modelo.

6. VisualizaciÛn del modelo
=======
b) Precios desde PartsGeek (scraping)
Ejecutar:
bash
python ingestion/web_scraping/Importa partsgeek.py
Esto genera:
* precios_partsgeek.csv,
* registros listos para inserci√≥n en PostgreSQL.

?? 5. Consultas representativas
Las consultas del MVP est√°n en:

postgres/tablas/
Incluyen:
* Leads por estado
* Inventario por concesionario
* Facturaci√≥n detallada por cliente
* Comparaci√≥n de precios externos
Estas consultas permiten validar el funcionamiento del modelo.

?? 6. Visualizaci√≥n del modelo
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16
El diagrama ER se encuentra en:
docs/postgres - spo.png
<<<<<<< HEAD
=======
Representa:
* entidades principales,
* relaciones,
* claves primarias y for√°neas,
* vistas auxiliares.
>>>>>>> 5ce82c5e1701214f724f0a82fd84646305ec2e16

Representa:
- entidades principales,
- relaciones,
- claves primarias y for·neas,
- vistas auxiliares.

7. Reproducibilidad
El sistema puede levantarse completamente en local siguiendo estos pasos:
1. Crear la base de datos.
2. Ejecutar el DDL.
3. Cargar los CSV.
4. Ejecutar los scripts de ingesta.
5. Validar con las consultas representativas.
No se requieren servicios externos, licencias privativas ni dependencias en la nube.


