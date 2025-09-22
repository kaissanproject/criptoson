# Etapa 1: Base - Use uma imagem Python oficial e leve.
FROM python:3.10-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para o Flask
# FLASK_APP: aponta para o arquivo de entrada da aplicação
# FLASK_ENV: 'development' ativa o modo de debug e recarregamento automático
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
# Garante que o output do Python não seja bufferizado, útil para ver logs em tempo real
ENV PYTHONUNBUFFERED=1

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta 5000, que é a porta padrão do Flask
EXPOSE 5000

# Comando para rodar a aplicação quando o container iniciar.
# O host 0.0.0.0 é essencial para que a aplicação seja acessível de fora do container.
CMD ["flask", "run", "--host=0.0.0.0"]
