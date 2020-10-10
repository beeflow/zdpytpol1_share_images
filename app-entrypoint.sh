#!/usr/bin/env bash
set -e

echo "Migrating..."
./manage.py makemigrations
./manage.py migrate

echo ""
echo "-------------------------------------"
echo "#  Creating superuser with:         #"
echo "#       username: admin             #"
echo "#       password: h98yt54y5rd       #"
echo "-------------------------------------"

# shellcheck disable=SC2002
cat entrypoint.py | python manage.py shell

exec "$@"