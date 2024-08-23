FROM python:3.11-slim

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Cria um usuário não privilegiado chamado 'default'
RUN useradd default -m

# Instala o postgresql-client e netcat
RUN apt-get update && \
    apt-get install -y postgresql-client netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Cria o diretório do projeto
RUN mkdir /sistema_advocacia && chown default:default /sistema_advocacia
RUN chmod -R 775 /sistema_advocacia

# Define o diretório de trabalho
WORKDIR /sistema_advocacia

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do aplicativo e ajusta as permissões
COPY --chown=default:default . .

# Define o usuário padrão como 'default'
USER default
ENV PATH="/home/default/.local/bin:$PATH"

# Copia o script de entrada e define permissões
COPY --chown=default:default docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh

# Especifica o script de entrada
CMD ["/docker-entrypoint.sh"]