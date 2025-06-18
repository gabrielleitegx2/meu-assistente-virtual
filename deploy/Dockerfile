# Imagem base
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requirements
COPY deploy/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Define a porta que será exposta (opcional, Render detecta automaticamente)
EXPOSE 10000

# Comando para iniciar a aplicação FastAPI com uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "10000"]