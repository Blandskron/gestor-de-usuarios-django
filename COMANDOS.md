# Comandos rápidos

La explicación completa está en `README.md`. Esta hoja sirve como referencia
durante el laboratorio.

```bash
# Preparación local
python -m venv .venv
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Desarrollo
python manage.py runserver
python manage.py ensure_superuser

# Validación
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py spectacular --validate --file "API de Gestión de Usuarios.yaml"

# Docker
docker compose up --build
docker compose logs -f web
docker compose exec web python manage.py test
docker compose down
```

`ensure_superuser` solo crea la cuenta si están definidas las tres variables
`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y
`DJANGO_SUPERUSER_PASSWORD`. Volver a ejecutarlo no crea duplicados.
