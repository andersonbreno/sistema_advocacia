FROM python:3.11-slim

# Cria um usuário não privilegiado chamado 'default'
RUN useradd default -m && \
mkdir /sistema_advocacia && chown default /sistema_advocacia

WORKDIR /sistema_advocacia
# Define o usuário padrão como 'default'
USER default
ENV PATH="/home/default/.local/bin:$PATH"

# Copia o arquivo requirements.txt
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do aplicativo
COPY . .

# Copia o script de entrada e define permissões
COPY --chown=default:default docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh

# Especifica o script de entrada
CMD ["/docker-entrypoint.sh"]
