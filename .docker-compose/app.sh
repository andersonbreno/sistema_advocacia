#!/bin/sh

while ! python -c 'import socket; socket.create_connection(("127.0.0.1", 15432))' 2> /dev/null
do
  echo 'Aguardando DB...'
  sleep 5
done

python manage.py migrate
exec python manage.py runserver
