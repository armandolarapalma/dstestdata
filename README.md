# Test Arquitecto de datos
Prueba tecnica arquitecto de datos

### Ejercicio 1
## RESPUESTA A EJERCICIO 1 PASO V

Maquina serie N1 tipo standard-2 (2cpus, 7.5 Ram) 
OS Debian se opta por este OS ya que es ligero y dado que se elige un tipo de maquina con especificaciones limitidas para ahorrar en costos me peracio la mejor opcion

Creación de maquina virtual habilitada para trabajar con Notebook.
para la creacion de la maquina virtual, se pude ejecutar en el bash de GCP, antes de ejecutar se debe crear o elegir un projecto y actualizar la etiqueta "-project" del codigo, se debe crear cueta de servicio y modicicar en la entiqueta "--service-accout"

# Create MV
```bash
gcloud compute instances create beam-20220916-153758 
--project=bs-bigdata-poc 
--zone=us-west1-b 
--machine-type=n1-standard-2 
--network-interface=network-tier=PREMIUM,subnet=default 
--metadata=
    container=gcr.io/deeplearning-platform-release/beam-notebooks:latest,
    enable-guest-attributes=TRUE,framework=Apache\ Beam,
    notebooks-api=PROD,
    proxy-mode=service_account,p
    roxy-url=7be9b4bd7d2024bf-dot-us-west1.notebooks.googleusercontent.com,
    report-container-health=true,report-system-health=true,
    restriction=,shutdown-script=/opt/deeplearning/bin/shutdown_script.sh,title=,
    version=96 
--maintenance-policy=MIGRATE 
--provisioning-model=STANDARD 
--service-account=test-compute@developer.gserviceaccount.com 
--scopes=https://www.googleapis.com/auth/cloud-platform 
--tags=
    deeplearning-vm,
    notebook-instance 
--create-disk=a
    uto-delete=yes,
    boot=yes,
    device-name=boot,
    image=projects/deeplearning-platform-release/global/images/dataflow-container-v20220825,
    mode=rw,
    size=100,
    type=projects/ghdz-grupo-bigdata-poc/zones/us-west1-b/diskTypes/pd-standard 
--no-shielded-secure-boot
--shielded-vtpm 
--shielded-integrity-monitoring 
--labels=goog-caip-notebook= 
--reservation-affinity=any
```
Una vez creada la maquina virtual se debe registrar la instancia con la nueva API de Notebooks
Pasos: 
    1- En la consola de GCP dirigirse al servicio Vertex AI. 
    2- seleccionar Workbench. 
    3-Marcar la casilla Incluir instancias heredadas. 
    4- Click en REGISTER ALL
    
## RESPUESTA EJERCICIO 1 PASO II

Bash para crea el bucket "anoc001-test-armandolara" en google cloud storage, se pude ejecutar en el bash de GCP en este paso los Buckes nacen con la propiedad de monitorear eventos atraves de Cloud Logging por lo que podemos crear procesos que se ejecuten atraves de eventos que sucedan dentro del bucket.

```bash
gcloud alpha storage buckets create gs://anoc001-test-armandolara
```

## RESPUESTA EJERCICIO 1 PASO III
Bash para crea el bucket "anoc001-test-data-armandolara" en google cloud storage, se pude ejecutar en el bash de GCP  en este paso los Buckes nacen con la propiedad de monitorear eventos atraves de Cloud Logging por lo que podemos crear procesos que se ejecuten atraves de eventos que sucedan dentro del bucket

```bash
gcloud alpha storage buckets create gs://anoc001-test-armandolara
```

## Notebook
# Inicia desarrollo de proceso ETL, incluye respuestas a ejercicio 1 pasos: III,VI, VIII, IX, X

El archivo DSTESTEDATA.ipynb de la carpeta Ejercicio1 contine el desarrolle del proceso ETL.

El codigo de este notebook se deja listo para ser desplegado en Cloud funtions y que su ejecucion sea desencadenada a traves de eventos monitereando los cambios ocurridos en la carpeta raw del bucket de storage. 
-Ejercicio
--Funcions

### Ejercicio 2

Se proponen dos capas de almacenamiento para el procesamiento de datos

## Capa de Almacén de datos crudos

 Se plantea realizar réplicas de las bases sql haciendo uso del CDC para extraer los eventos de cambio de la base de datos, transformarlos y cargarlos de forma tabular en una capa que almacene la información cruda y de esta manera lograr tener en tiempo real todos los cambios realizados por los sistemas transaccionales. 

El objetivo de crear estas réplicas es para no interferir o degradar el performance de los servidores transaccionales.

# F2 PostgresSQL 
- Se haría uso del servicio DataStream para extraer el CDC y depositarlo en un bucket de storage.Un pipeline en Apache beam usado Dataflow como runner, se encargaría de leer, transformar y cargar los eventos de cambio de la base de datos en la capa de crudos. La ejecución del proceso sería desencadenada cada que se detecte un cambio en el bucket que almacena el CDC
En caso de usar infraestructura onpremise se haría uso de spark como runner para el pipeline de Apache beam

# F3 MS sql server 
- Se puede ir al leer el CDC con un pipeline en Apache beam usado Dataflow como runner, se encargaría de leer, transformar y cargar los eventos de cambio de la base de datos en la capa de crudos. La ejecución sería programada por medio de un scheduler dentro de GCP.
En caso de usar infraestructura onpremise se haría uso de spark como runner para el pipeline de Apache beam y sería orquestado en Air Flow

# CRM 
- Serán almacenados en esta misma capa por medio de proceso batch. El proceso batch sería un pipeline en Apache beam usado Dataflow como runner y sería orquestado en Air Flow desplegado en el servicio Cloud Composer de GCP. 

En caso de usar infraestructura onpremise se haría uso de spark como runner para el pipeline de Apache beam y sería orquestado en Air Flow

## Capa de consumo

En esta capa se almacenarán las tablas finales listas para su consumo.

El procesamiento y carga de los datos se realizará por medio de proceso batch sql haciendo uso de hadoop y spark y serían orquestados por Air Flow desplegado en el servicio Cloud Composer de GCP.

La Capa de consumo cumpliría dos propósitos.
# 1 Se habilitará el acceso a los objetos procesados para los usuarios operativos y serían capaces de realizar consultas sql a través de bigquery.
# 2 El equipo de ciencia de datos podría realizar peticiones de datos por medio de la API de Bigquery y usarlos dentro de sus modelos de ML.

	
Se opta por Bigquery como medio de almacenamiento por el rendimiento y costos, además que los usuarios operativos pueden hacer consultas sql  desde la consola de bigquery y el equipo de científicos puede acceder por medio de una API.

<img width="1064" alt="Captura de Pantalla 2022-09-21 a la(s) 5 37 38 p m" src="https://user-images.githubusercontent.com/113946771/191806629-0f69b9cf-b3c7-4760-8fa9-01b1aecdb507.png">




