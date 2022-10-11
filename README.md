# Inventario de vacunación de empleados
## Reto Kruger

API Rest que permite al usuario administrador o superuser crear un registro parcial con sus datos, generar un usuario [cédula] y contraseña [cédula], actualizar, listar y eliminar empleados. Además cuenta con el registro, actualización, filtrado y eliminación de las vacunas del empleado.
## Requirements

>- Python v3.10.*
>- Postgresql 14
>- Django
```sh
    pip install Django==4.1.2
```
>- Crear un entorno virtual y activarlo
```sh
    python3 -m venv /path/to/new/virtual/environment
    cd /path/to/new/virtual/environment/activate
```

## Installation
Crear la base de datos en postgresql y subir el archivo __vacunacion_empleados.sql__
Descomprimir __inventario_vacunas_empleados.zip__ dentro del entorno virtual, ingresar a la carpeta __empleados_vacunados__ y editar el archivo __settings.py__
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
```
- ### Instalar Dependencias
    ```sh
    pip install djangorestframework==3.14.0 #Paquete provee herramientas para crear APIs
    pip install djangorestframework-simplejwt==5.2.1 #Paquete para utilizar un Token para validar endpoints
    pip install drf-extensions==0.7.1
    pip install drf-spectacular==0.24.2 #Paquete que permite usar swagger
    pip install psycopg2==2.9.3 #Paquete para conectar con nuestra base de datos postgresql
    ```
    o digitar el siguiente comando para instalar todas las dependencias para el funcionamiento de la aplicacion
    
    ```sh
    pip intall -r requirementes.txt
    ```
    ### Crear el usuario administrador
    ```sh 
    python manage.py createsuperuser    
    ```
     ### Desplegar la aplicación
    ```sh 
    python manage.py runserver
    ```
    URL para acceder a la documentacion de swagger
    ```sh
    http://127.0.0.0:8000/api/swagger/
    ```