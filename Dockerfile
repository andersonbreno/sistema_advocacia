FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /djangoapp

COPY /djangoapp/requirements.txt /djangoapp/

RUN pip install --no-cache-dir -r /djangoapp/requirements.txt

COPY . /djangoapp/

CMD ["scripts/docker-entrypoint.sh"]
