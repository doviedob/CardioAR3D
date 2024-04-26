# Como instalar MONAI Label en una instancia EC2 de AWS
## Configuración de la instancia EC2 creada
Para acceder a la instancia mediante la ventana de comandos de windows, nos dirigimos mediante el explorador de archivos a la carpeta donde está descargada la llave de seguridad de la instancia que creamos anteriormente, y desde la barra de direcciones del explorador de archivos escribimos ‘cmd’ y presionamos Enter, como se muestra a continuacion:

![cmd](https://github.com/doviedob/CardioAR3D/blob/main/Images/entrar%20cmd.png)

Posteriormente, solo será necesario copiar la línea de comando especificada en la conexión SSH de la consola de AWS, y luego copiar en la ventana de comandos donde nos pedirá autenticar para finalmente conectarse.

![conectarse_ssh](https://github.com/doviedob/CardioAR3D/blob/main/Images/conectar-ssh.png)
![cmd enlazado](https://github.com/doviedob/CardioAR3D/blob/main/Images/cmd_enlazado.png)

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
