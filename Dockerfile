FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /sistema_advocaria

COPY /sistema_advocaria/requirements.txt /djangoapp/

RUN pip install --no-cache-dir -r /sistema_advocaria/requirements.txt

COPY . /sistema_advocaria//

CMD ["scripts/docker-entrypoint.sh"]
