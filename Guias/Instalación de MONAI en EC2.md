# Como instalar MONAI Label en una instancia EC2 de AWS
## En una instancia de Ubuntu

Para realizar esto es necesario haber configurado la instancia EC2 de la guia anterior. Nuevamente, desde la consola ejecutaremos los siguientes comandos:

- Verificamos la versión de conda instalada en la instancia:
```
conda --version
```
- Crearemos el entorno virtual donde se correrá MONAI Label:
```
conda create -n monailabel-env python=3.9
```
- Ejecutaremos el entorno:
```
conda activate monailabel-env
```
- Instalaremos el controlador de ‘gcc’ que necesitaremos para los pasos siguientes:
```
sudo apt-get install gcc
```
- Instalamos MONAI Label
```
pip install monailabel
```
- Verificamos que se encuentre instalado mediante el siguiente comando:
```
pip freeze
```
- Revisamos lo que se encuentra disponible al instalar MONAI:
```
monailabel -h
```
- Descargamos la app de radiología:
```
monailabel apps --download --name radiology --output apps
```
- Revisamos los datasets disponibles para probar MONAI:
```
monailabel datasets
```
- Con el siguiente comando guardamos uno de los datasets disponibles simplemente agregando el nombre en la parte subrayada:
```
monailabel datasets --download --name Task02_Heart --output datasets
```
- Para ejecutar correctamente el comando ‘wheel’ es necesario instalar el servidor Dicom web:
```
pip install dicomweb-client[gcp]
```
- Finalmente, arrancaremos el servidor donde se encuentra MONAI:
```
monailabel start_server --app apps/radiology --studies datasets/Task02_Heart/imagesTr --conf models segmentation
```
