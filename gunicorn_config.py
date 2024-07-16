# gunicorn_config.py

bind = "0.0.0.0:8000"
workers = 3  # Ajuste conforme necessário, geralmente 2-4x o número de CPUs disponíveis
