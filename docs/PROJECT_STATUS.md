# Estado del proyecto

Última revisión: 2026-08-27.

## Estado actual

- API de usuarios basada en el modelo `User` nativo.
- Login, refresh y logout JWT con RS256 y blacklist.
- CRUD protegido por `IsAdminUser`.
- Swagger, ReDoc y esquema OpenAPI.
- Configuración local y Docker con SQLite.
- Superusuario educativo opcional e idempotente.
- Suite de pruebas de API, routing y management command.

## Decisiones

- Django idiomático sin modelo de usuario propio ni capa de servicios artificial.
- SQLite y un solo contenedor para mantener el foco pedagógico.
- claves RSA generadas en `.keys/` o en el volumen, nunca en el árbol versionado.
- defaults cómodos solo para desarrollo; producción exige endurecimiento.

## Restricciones y deuda conocida

- La clave privada que estuvo en la historia Git anterior debe considerarse
  comprometida. No se reescribió historia para evitar una operación destructiva
  sin coordinación con todos los clones.
- Docker usa `runserver`, deliberadamente limitado a desarrollo.
- No existe UI de aplicación ni registro público.

## Últimas validaciones

Ejecutadas el 2026-08-27:

- `python manage.py check`: OK, sin problemas.
- `python manage.py check --deploy` con perfil HTTPS: OK, sin advertencias.
- `python manage.py makemigrations --check --dry-run`: OK, sin cambios.
- `python manage.py test`: OK, 13 pruebas.
- esquema OpenAPI: generado y validado sin errores.
- `docker-compose config`: OK.
- construcción/arranque Docker: no comprobado; el daemon local quedó sin
  responder incluso a `docker info`. Reintentar con Docker Desktop operativo.

## Criterio mínimo antes de cambiar el proyecto

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py spectacular --validate --file "API de Gestión de Usuarios.yaml"
docker compose config
```

## Próximo paso recomendado

Implementar un perfil relacionado uno a uno con `User`, incluyendo migración,
serializer y pruebas de permisos, sin reemplazar prematuramente la autenticación.
