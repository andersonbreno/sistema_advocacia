FROM python:3.11-slim

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Cria um usuário não privilegiado chamado 'default'
RUN useradd default -m && \
mkdir /sistema_advocacia && chown default /sistema_advocacia

# Instala o postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# Instala o nc para o postgresql
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia o restante do código do aplicativo
COPY . .

WORKDIR /sistema_advocacia

# Define o usuário padrão como 'default'
USER default
ENV PATH="/home/default/.local/bin:$PATH"

# Copia o arquivo requirements.txt
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script de entrada e define permissões
COPY --chown=default:default docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh

# Especifica o script de entrada
CMD ["/docker-entrypoint.sh"]
