# Gestor de Usuarios con Django REST Framework

API educativa para aprender autenticación, autorización y operaciones CRUD con
Django. El proyecto administra el modelo `User` incluido en Django, emite JSON
Web Tokens firmados con RSA (RS256), invalida refresh tokens al cerrar sesión y
expone documentación OpenAPI interactiva.

Está pensado como laboratorio: conserva una arquitectura pequeña y explícita,
pero incorpora configuración por entorno, pruebas, Docker y automatización de
desarrollo similares a las de un proyecto real.

## Qué aprenderás

- cómo Django enruta una petición hacia una vista;
- cómo un `ModelViewSet` conecta modelos, serializers y respuestas JSON;
- cómo Django almacena contraseñas de forma segura y aplica sus validadores;
- cómo DRF autentica JWT y restringe endpoints mediante permisos;
- cómo funcionan access tokens, refresh tokens y una blacklist de logout;
- cómo explorar usuarios, grupos y permisos desde Django Admin;
- cómo comprobar una API con tests automatizados, OpenAPI y Docker.

## Funcionalidades

- login, renovación y logout con JWT;
- claims `username`, `grupos` y `permisos` dentro del access token;
- CRUD de usuarios reservado a cuentas con `is_staff=True`;
- validación y hash seguro de contraseñas al crear o actualizar usuarios;
- Swagger UI, ReDoc y esquema OpenAPI;
- creación idempotente de un superusuario educativo;
- migraciones automáticas al iniciar el contenedor;
- 13 pruebas sobre autenticación, autorización, CRUD y comandos.

## Tecnologías y requisitos

- Python 3.12 (Django 6 requiere Python 3.12 o superior);
- Django 6, Django REST Framework, SimpleJWT y drf-spectacular;
- SQLite, suficiente para este laboratorio de una sola instancia;
- Git;
- Docker con Compose, opcional.

Las versiones exactas están fijadas en `requirements.txt`.

## Instalación local

```bash
git clone https://github.com/Blandskron/gestor-de-usuarios-django.git
cd gestor-de-usuarios-django
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux o macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala, prepara la base y crea una cuenta administrativa:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visita:

- API/Swagger: <http://localhost:8000/>;
- Django Admin: <http://localhost:8000/admin/>;
- ReDoc: <http://localhost:8000/docs/api/schema/redoc/>;
- esquema OpenAPI: <http://localhost:8000/docs/api/schema/>.

En Admin puedes estudiar el modelo `User` nativo, grupos, permisos y refresh
tokens bloqueados. No hay modelos propios ni datos iniciales obligatorios.

## Variables de entorno

El proyecto funciona localmente con valores de desarrollo. Las variables son
opcionales al usar `runserver` y obligatorias cuando se prepare un despliegue:

| Variable | Propósito | Default educativo |
| --- | --- | --- |
| `DJANGO_DEBUG` | Activa el modo de depuración | `True` |
| `DJANGO_SECRET_KEY` | Firma sesiones y datos internos de Django | valor inseguro local |
| `DJANGO_ALLOWED_HOSTS` | Hosts separados por comas | hosts locales |
| `DJANGO_DB_PATH` | Ruta del archivo SQLite | `db.sqlite3` |
| `JWT_KEY_DIR` | Directorio del par RSA generado | `.keys/` |
| `DJANGO_SUPERUSER_*` | Credenciales para `ensure_superuser` | sin valor local |

Las variables `DJANGO_SECURE_*` y de cookies incluidas en `.env.example`
permiten activar el perfil HTTPS. HSTS requiere comprender sus efectos antes de
usarlo y por eso está desactivado en desarrollo.

`.env.example` contiene un ejemplo para Docker. Compose lee automáticamente un
archivo `.env` en la raíz, pero Django no lo carga directamente en ejecución
local. En PowerShell puedes definir una variable con
`$env:DJANGO_DEBUG = "False"`; en Bash, con `export DJANGO_DEBUG=False`.

Las claves RSA se crean en el primer arranque dentro de `JWT_KEY_DIR`. `.keys/`,
`*.pem`, `.env` y la base local están ignorados por Git. Nunca publiques estos
archivos. Al regenerar las claves, todos los JWT anteriores dejan de ser válidos.

## Ejecución con Docker

Docker usa un único servicio web y un volumen persistente para SQLite y las
claves RSA; PostgreSQL no aportaría valor al objetivo introductorio.

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/macOS
docker compose up --build
```

El entrypoint aplica migraciones, ejecuta `ensure_superuser` y luego inicia el
servidor. Con el `.env.example`, las credenciales educativas son `admin` /
`AdminEducativo-2026`; cámbialas si el entorno será compartido.

Comandos cotidianos:

```bash
docker compose down
docker compose logs -f web
docker compose exec web python manage.py test
```

Para reiniciar completamente los datos del laboratorio:

```bash
docker compose down --volumes
docker compose up --build
```

`runserver` y estas credenciales son solo para educación/desarrollo, no un
servidor ni una estrategia de secretos aptos para producción.

## Usar la API

Primero inicia sesión:

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminEducativo-2026"}'
```

Envía el access token en `Authorization: Bearer <access>` para acceder al CRUD.
El refresh token se usa únicamente en `/token/refresh/` y `/logout/`.

| Método y ruta | Función | Acceso |
| --- | --- | --- |
| `POST /api/users/login/` | emitir tokens | público |
| `POST /api/users/token/refresh/` | renovar access token | refresh válido |
| `POST /api/users/logout/` | bloquear refresh token | autenticado |
| `/api/users/crud/` | listar y crear usuarios | administrador |
| `/api/users/crud/<id>/` | consultar, editar o eliminar | administrador |

## Flujo educativo

```text
HTTP / URL
    ↓ core/urls.py y users/urls.py
View (LoginView, LogoutView o UserViewSet)
    ↓
Serializer valida entrada y transforma el modelo User
    ↓
ORM de Django ↔ SQLite
    ↓
Response JSON documentada por OpenAPI
```

Esta API no usa templates propios para sus respuestas. Los templates visibles
pertenecen al Admin, al navegador de DRF, Swagger y ReDoc.

## Estructura

```text
.
├── core/                     # settings, URLs y entrypoints WSGI/ASGI
├── users/                    # API, serializer, URLs, tests y comando educativo
├── docs/                     # app de documentación OpenAPI y guías del proyecto
├── .github/workflows/        # validación continua sencilla
├── Dockerfile
├── compose.yaml
├── docker-entrypoint.sh
├── .env.example
├── manage.py
└── requirements.txt
```

- modifica endpoints y permisos en `users/views.py`;
- modifica campos JSON y validaciones en `users/serializers.py`;
- modifica configuración en `core/settings.py`;
- añade pruebas en `users/tests.py`;
- no elimines las migraciones históricas de Django ni publiques claves.

## Tests y controles de calidad

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py spectacular --validate --file openapi.yaml
```

GitHub Actions ejecuta los tres primeros controles en cada push y pull request.
El archivo `API de Gestión de Usuarios.yaml` es una instantánea versionada del
esquema y debe regenerarse cuando cambie el contrato HTTP.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| `ModuleNotFoundError: django` | entorno inactivo o dependencias ausentes | activa `.venv` e instala `requirements.txt` |
| `no such table` | faltan migraciones | ejecuta `python manage.py migrate` |
| `401` en el CRUD | access token ausente o vencido | inicia sesión y envía el header Bearer |
| `403` en el CRUD | usuario autenticado sin `is_staff` | usa un superusuario o habilita staff desde Admin |
| puerto 8000 ocupado | otro proceso usa el puerto | usa `runserver 8001` o cambia el puerto de Compose |
| superusuario Docker ausente | variables incompletas o volumen antiguo | revisa `.env` y ejecuta `ensure_superuser` |
| JWT dejan de validar | se regeneró `.keys/` | vuelve a iniciar sesión |
| Docker no responde | daemon apagado | inicia Docker Desktop y reintenta |

Consulta [DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md) para profundizar
en las decisiones de seguridad y [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
para conocer el estado verificable del repositorio.

## Próximo paso sugerido

Añade perfiles de usuario mediante un modelo `OneToOneField` y pruebas de sus
permisos. Es un buen ejercicio para aprender relaciones sin reemplazar el modelo
de autenticación antes de comprenderlo.

## Licencia

Consulta [LICENSE](LICENSE).
