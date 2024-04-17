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

Con el conocimiento previo de los pasos anteriores, se continuará con la configuración de la instancia usada para este proyecto:

