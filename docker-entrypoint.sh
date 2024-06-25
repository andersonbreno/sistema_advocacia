#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! pg_isready -q -U $POSTGRES_USER -d $POSTGRES_DB -h $POSTGRES_HOST -p $POSTGRES_PORT
do
  echo "Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
  sleep 2
done

echo "Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

#python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000 --noreload
