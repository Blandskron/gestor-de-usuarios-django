#!/bin/sh
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Comprobando superusuario educativo..."
python manage.py ensure_superuser

exec "$@"
