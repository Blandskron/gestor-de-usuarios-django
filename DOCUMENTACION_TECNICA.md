# Arquitectura y seguridad

## Alcance

El repositorio es una API monolítica educativa. `core` configura Django,
`users` contiene el contrato HTTP y `docs` publica OpenAPI. Se reutiliza el
modelo `django.contrib.auth.models.User`; `users/models.py` permanece vacío de
forma intencional y no necesita migraciones propias.

## Autenticación JWT con RS256

SimpleJWT emite un access token de 60 minutos y un refresh token de un día. El
servidor firma con una clave RSA privada y valida con la pública. El par se crea
en `JWT_KEY_DIR` al primer arranque, nunca se guarda en Git y persiste en el
volumen Docker.

`MyTokenObtainPairSerializer` añade `username`, grupos y permisos al payload.
Estos claims son útiles para interfaces cliente, pero la autorización real se
vuelve a comprobar en el servidor mediante `IsAdminUser`; nunca debe confiarse
solo en datos decodificados por el navegador.

Logout agrega el refresh token a las tablas de blacklist. Un access token ya
emitido sigue siendo válido hasta expirar, por eso su vida es corta. El cliente
debe borrar ambos tokens al cerrar sesión.

## Sesiones y CSRF

DRF admite JWT mediante header y sesiones para el navegador de la API. Los
headers Bearer no son enviados automáticamente por el navegador y no dependen
de CSRF. Cuando se autentica con una cookie de sesión, `SessionAuthentication`
sí exige un token CSRF en métodos inseguros. Emitir una cookie `csrftoken` junto
al JWT no convierte por sí solo a JWT en una estrategia CSRF.

La seguridad frente a XSS depende de cómo el cliente almacene los tokens y está
fuera del alcance de este backend. Una aplicación web real debe definir una
estrategia explícita de almacenamiento y una política de contenido.

## CRUD y contraseñas

`UserViewSet` usa `ModelViewSet`, por lo que DRF proporciona list, create,
retrieve, update, partial update y destroy. `IsAdminUser` exige `is_staff`; no
basta con estar autenticado.

`UserSerializer` ejecuta los validadores configurados por Django y usa
`create_user`/`set_password`. Guardar el texto directamente en el campo
`password` rompería autenticación y expondría la contraseña.

## Configuración

`core/settings.py` incluye defaults explícitos para local y variables para los
valores que varían. SQLite se eligió porque el laboratorio tiene un servicio y
no enseña concurrencia de base de datos. En un despliegue real se deben definir
secreto, hosts, HTTPS, cookies seguras y una base administrada, además de usar un
servidor WSGI/ASGI de producción en lugar de `runserver`.

## Docker

La imagen usa Python 3.12 slim y un usuario sin privilegios. El volumen
`django_data` contiene `db.sqlite3` y las claves; el código vive en la imagen.
El entrypoint ejecuta, de forma visible y ordenada:

1. `migrate --noinput`;
2. `ensure_superuser`;
3. el comando configurado en `CMD`.

Esta automatización es idempotente y evita ocultar lógica en `settings.py`.

## Límites conocidos

- `runserver` y SQLite son apropiados para el laboratorio, no para producción;
- no existe registro público: solo un administrador crea usuarios;
- logout no revoca access tokens ya emitidos;
- una clave privada existió en el historial inicial y debe considerarse
  comprometida; la versión actual genera un par nuevo fuera de Git, pero limpiar
  historia requiere una operación coordinada y destructiva que no se realiza aquí.
