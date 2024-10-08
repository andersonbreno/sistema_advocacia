# Sistema de Gestão para Escritórios de Advocacia

# Projeto em Andamento

# Sobre o projeto

- Introdução
  
Este sistema é uma solução desenvolvida para otimizar a gestão de escritórios de advocacia. O projeto foi concebido como parte do trabalho de conclusão do curso de Sistemas para Internet e está atualmente em estágio de MVP (Produto Mínimo Viável). Utilizando a interface AdminLTE, o sistema oferece funcionalidades completas de CRUD para Clientes, Processos e Tarefas, além de telas de login, logout e recuperação de senha. A ideia é futuramente transformá-lo em uma plataforma SaaS (Software as a Service).

- Funcionalidades Principais
  
CRUD de Clientes: Gerenciamento completo de informações dos clientes.
CRUD de Processos: Controle e acompanhamento de processos jurídicos.
CRUD de Tarefas: Organização e gestão de tarefas diárias.
Segurança: Páginas de login, logout e recuperação de senha.
Permissões Personalizadas: Controle de acesso baseado em tipos de usuários.
Tecnologias Utilizadas
Linguagem: Python
Framework: Django
Banco de Dados: Postgresql
Frontend: HTML5, CSS3, Bootstrap 5
Backend: Django
Hospedagem: AWS

Este projeto é um desenvolvimento contínuo e está alinhado com as necessidades específicas de escritórios de advocacia, buscando sempre melhorar a eficiência e a gestão dos processos internos. 


- Tecnologias utilizadas

Back end
Python
Django
Banco de dados: Postgresql
Front end
HTML / CSS /
Bootstrap 5

# Como executar o projeto nas distrinuições Debian/Ubuntu

* Instale o python3.12
```
apt install python3.12
```
* Instale o python3.12-venv
```
apt install python3.12-venv
```
* Criar virtualenv
```
python3.12 -m venv .venv
```
```
source .venv/bin/activate
```
* Instalar dependências de desenvolvimento
```
pip install -r requirements.txt
```
* Compilar e Sincronizar as atualizações das bibliotecas
```
pip-compile
```
```
pip-sync
```
* Copiar arquivo de variáveis de ambiente
```
cp .env-example .env
```
* Instale os arquivos estáticos
```
python3 manage.py collectstatic --no-input
```
* Execute o Docker Compose
```
docker compose up -d
```
* Credenciais do Superusuário Administrador

Usuário: admin
Senha: sysadv123

Autor
Anderson Breno de Aguiar Azevedo

https://www.linkedin.com/in/anderson-azevedo-tech/
