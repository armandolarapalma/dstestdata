# Test Arquitecto de datos
Prueba tecnica arquitecto de datos

## RESPUESTA A EJERCICIO 2 PASO V

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
