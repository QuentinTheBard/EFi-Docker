# EpicBlogSpot

## Instalar Requerimientos - Comando para instalar Flask, SQLAlchemy, Flask-Migrate.
- pip install -r requirements.txt

## XAMPP - Crear base de datos
Primero debes crear tu base de datos local en XAMPP, en este caso el nombre de la base de datos es blog_python
El nombre es importante al momento de queres obtener o agregar datos a las diferentes tablas
Ejemplo de como llamar la base de datos en tu código:
<!-- app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/nombredelabasededatos' -->
- app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/blog_python'

## FLASK MIGRATE - Comando para generar los modelados de las tablas.
Nos movemos a la carpeta models para ejecutar las migraciones
- cd app/models

Iniciar Migraciones
- flask db init

Generar la migracion
- flask db migrate -m "Descripcion del cambio."

Migrar los cambios a la db
- flask db upgrade

Luego de que las migraciones finalicen volvemos a la raiz del projecto (EFI_Blog)
- cd ../
-cd ../
Ejecutar esos comandos.
## FLASK & Docker Compose - Comando para ejecutar la Aplicacion
Primero construimos nuestros Docker
- docker compose build

Luego de que el comando build termine, ejecutamos el siguiente para dar inicio a la aplicación
- docker compose up -d 

Para visualizar nuestro contenedor activo
- docker compose ps



### Finalmente abre tu navegador para visualizar la aplicación.
- localhost:8000
![home_page](https://user-images.githubusercontent.com/89541868/203129368-b1fb14ff-7574-4ae2-8795-5b17ac00d5a5.png)
