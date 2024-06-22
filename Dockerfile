FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /sistema_advocacia

# Copy the requirements file
COPY ./requirements.txt /sistema_advocacia/

# Install the dependencies
RUN pip install --no-cache-dir -r /sistema_advocacia/requirements.txt

# Copy the rest of the application code
COPY . /sistema_advocacia/

# Specify the entrypoint script
CMD ["scripts/docker-entrypoint.sh"]