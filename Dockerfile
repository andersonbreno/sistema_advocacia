FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /sistema_advocacia
USER default


# Copy the requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /sistema_advocacia/requirements.txt

# Copy the rest of the application code
COPY . .

COPY --chown=default:default docker-entrypoint.sh /docker-entrypoint.sh
COPY libnitgen/lib/libNBioBSP.so /usr/lib
COPY libnitgen/lib/NBioBSP.lic /usr/lib


RUN chmod 755 /docker-entrypoint.sh

ENV DJANGO_RUN_MIGRATE=1

# Specify the entrypoint script
CMD ["scripts/docker-entrypoint.sh"]