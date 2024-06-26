#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! pg_isready -q -U $POSTGRES_USER -d $POSTGRES_DB -h $POSTGRES_HOST -p $POSTGRES_PORT
do
  echo "Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
  sleep 2
done

echo "Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py runserver 0.0.0.0:8000 --noreload
