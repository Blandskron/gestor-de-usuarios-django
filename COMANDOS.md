# Guía de Comandos y Puesta en Marcha

Sigue estos pasos en orden para levantar el entorno de desarrollo localmente.

### 1. Entorno Virtual y Dependencias
Crea y activa tu entorno virtual, luego instala las dependencias necesarias:
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate 
# En macOS/Linux usarías: source venv/bin/activate

pip install djangorestframework drf-spectacular djangorestframework-simplejwt cryptography
```

### 2. Base de datos y Migraciones
Aplica las migraciones para crear las tablas de usuarios y de la lista negra (Blacklist) de JWT.
```bash
python manage.py migrate
```

### 3. Creación del Administrador y Ejecución
Crea tu primer usuario administrador (necesario para usar el CRUD) e inicia el servidor de desarrollo.
```bash
python manage.py createsuperuser
python manage.py runserver
```
