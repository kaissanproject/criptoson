# Usar uma imagem base oficial do Python (versão completa)
FROM python:3.10

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que o gunicorn vai usar
EXPOSE 5000

# Comando para rodar a aplicação quando o container iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]

