# Guía para agentes

## Objetivo

Mantener una API Django educativa, pequeña y reproducible que enseñe gestión de
usuarios, JWT RS256, permisos, OpenAPI, pruebas y Docker.

## Mapa rápido

- `core/settings.py`: entorno, SQLite, DRF, SimpleJWT y generación de claves.
- `core/urls.py`: entrypoint HTTP.
- `users/views.py`: endpoints y permisos.
- `users/serializers.py`: contrato JSON, claims y contraseñas.
- `users/tests.py`: comportamiento esperado.
- `users/management/commands/ensure_superuser.py`: bootstrap opcional.
- `docs/urls.py`: Swagger, ReDoc y esquema.
- `compose.yaml` y `docker-entrypoint.sh`: arranque reproducible.
- `docs/PROJECT_STATUS.md`: estado y deuda conocida.

## Antes de modificar

1. Lee `README.md` y `DOCUMENTACION_TECNICA.md`.
2. Revisa `git status`; conserva cambios ajenos.
3. No elimines migraciones históricas.
4. No publiques `.env`, SQLite ni archivos PEM.
5. No añadas PostgreSQL, frontend, servicios o dependencias sin una necesidad
   verificable del ejercicio.
6. Mantén compatibilidad local y Docker y actualiza OpenAPI si cambia un endpoint.

## Comandos

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test
docker compose up --build
```

## Validación obligatoria

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py spectacular --validate --file "API de Gestión de Usuarios.yaml"
docker compose config
```

No afirmes que Docker se construye o inicia si solo validaste Compose. Documenta
cualquier control que el entorno no permita ejecutar.

## Convenciones

- Código explícito, nombres claros y comentarios sobre decisiones, no sintaxis.
- Usa URLs nombradas y tests por comportamiento.
- El permiso del CRUD debe comprobarse en servidor.
- Toda escritura de contraseña pasa por validadores y `set_password` o
  `create_user`.
- Las claves RSA son estado local/operacional, no código fuente.
