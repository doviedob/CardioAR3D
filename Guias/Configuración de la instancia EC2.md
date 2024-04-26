## Configuración de la instancia EC2 en los servicios de AWS
## Selección de la instancia
Inicialmente, es necesario escoger la instancia correcta para el despliegue de MONAI Label, pues ecisten requisitos minimos de hardware necesarios para que funcione correctamente.

Los requisitos necesarios se encuentran en el repositorio de [MONAI Label](https://github.com/Project-MONAI/MONAILabel) 

## 1. Crear una cuenta de Amazon Web Services (AWS)

Para acceder a los servicios de computación en la nube, será necesario crear nuestra cuenta personal de AWS en su [sitio web oficial](https://aws.amazon.com/es/) y dando en la pestaña 'Inicie sesión en la consola' en la parte superior derecha. Allí podrá llenar los datos de nuevo usuario para tener acceso a la consola.

Adicionalmente, consulte los precios de los servicios ofrecidos por AWS en su [sección de precios y capa gratuita](https://aws.amazon.com/es/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23desktop-app-streaming).

## 2. Aprender a usar la consola de AWS

Con la finalidad de familiarizarse con el entorno de AWS y del manejo básico de la consola, puede observar los siguientes videos:

[![All text](https://img.youtube.com/vi/4TJN_YWHk6E/0.jpg)](https://www.youtube.com/watch?v=4TJN_YWHk6E)

Adicionalmente, se usarán los servicios de Elastic Cloud Compute (EC2), y el siguiente video explica su funcionamiento:

[![All text](https://img.youtube.com/vi/esafjvnPUZA/0.jpg)](https://www.youtube.com/watch?v=esafjvnPUZA)

## 3. Lanzamiento de la instancia

Con el conocimiento previo de los pasos anteriores, se continuará con la configuración de la instancia usada para este proyecto. Inicialmente, será necesario buscar en la [consola principal de AWS](https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1) el módulo EC2 y dar click en "Lanzar instancia".

- Desde allí configuraremos primero el nombre dela instancia y la imagen de OS sobre la que correra dicha instancia:

![nombre e imagen base](https://github.com/doviedob/CardioAR3D/blob/main/Images/nombre%20y%20plantilla.png)

- Posteriomente, requeriremos seleccionar el tipo de instancia. Para este proyecto, debido a que se entrenará un modelo de Deep Learning con la herramienta de MONAI, será necesario seleccionar algún tipo de instancia de tipo 'g' que cuenta con tarjeta gráfica dedicada, en este caso se eligió una de tipo 'g4dn.xlarge' que cuenta con una NVIDIA T4 con 16Gb de capacidad de GPU:

![Tipo de instancia](https://github.com/doviedob/CardioAR3D/blob/main/Images/tipo%20de%20instancia.png)

***NOTA:*** Para conocer más acerca de los tipos de instancia, dirigirse a la [página oficial de AWS](https://aws.amazon.com/es/ec2/instance-explorer/?ec2-instances-cards.sort-by=item.additionalFields.category-order&ec2-instances-cards.sort-order=desc&awsf.ec2-instances-filter-category=*all&awsf.ec2-instances-filter-processors=*all&awsf.ec2-instances-filter-accelerators=*all&awsf.ec2-instances-filter-additional-capabilities=*all&awsf.ec2-instances-filter-workload-tags=*all) que cuenta con la explicación detallada de cada una de ellas.

- Con lo anterior, será necesario escoger los permisos de red, así como configurar una red privada si así se desea. En este caso, se dejó una dirección IP 0.0.0.0 para facilitar el acceso a la instancia:

![Seguridad](https://github.com/doviedob/CardioAR3D/blob/main/Images/seguridad.png)
