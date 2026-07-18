La carpeta **ingestion/** contiene dos carpetas **api\_prices/** y **web\_scraping/**.



La primera carpeta contiene (al momento) el programa de  Python **eBay.py** que ejecuta la rutina para conectarse con eBay, buscar los códigos de partes que contiene el archivo ORGU.CSV y graba en la tabla **spo.precio\_comparativo** en nuestro sistema de persistencia. El archivo que se migra a la tabla es **precios\_ebay.csv**



En esta carpeta también encontrará el archivo **ingesta\_ebay**, que fue ejecutado en su momento por aparte para probar la conexión con la BDD, y las líneas de este código fue integrado a **eBay.py**. Entonces al momento sirve como parte de los programas de prueba.



El archivo **orgu\_original.csv** es el que envía el concesionario conteniendo sus códigos y descripciones



**importa partsgeek.py** realiza web scrappin en **partsgeek.com** y graba en nuestro sistema de persistencia. El archivo que se migra a la tabla es **precios\_partsgeek.csv**  

Al momento el web site nos está bloqueando la solicitud de búsqueda, hemos realizado el pedido formal para realizar el web scrapping pero a la fecha no hemos tenido respuesta. Al momento que tengamos la aprobación podremos obtener los datos. De no ser así, estamos en búsqueda de otra fuente de datos que podamos automatizar.

