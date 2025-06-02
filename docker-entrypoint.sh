#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Verificar se as variáveis de ambiente estão definidas
: "${POSTGRES_HOST:?Variável de ambiente POSTGRES_HOST não definida}"
: "${POSTGRES_PORT:?Variável de ambiente POSTGRES_PORT não definida}"
: "${DJANGO_SUPERUSER_USERNAME:?Variável de ambiente DJANGO_SUPERUSER_USERNAME não definida}"
: "${DJANGO_SUPERUSER_EMAIL:?Variável de ambiente DJANGO_SUPERUSER_EMAIL não definida}"
: "${DJANGO_SUPERUSER_PASSWORD:?Variável de ambiente DJANGO_SUPERUSER_PASSWORD não definida}"

# Esperar até que o PostgreSQL esteja disponível
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Verifica permissões
#echo "Verificando permissões no diretório do projeto..."
#ls -l /sistema_advocacia

#echo "Verificando permissões no diretório de migrações..."
#ls -l /sistema_advocacia/parceiros/migrations

python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Criar o superusuário se ele não existir
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
EOF

#exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
python3 manage.py runserver 0.0.0.0:8000 --noreload