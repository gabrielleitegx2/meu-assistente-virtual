# Use imagem oficial do Python
FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia apenas os arquivos necessários primeiro para aproveitar cache de dependências
COPY ./deploy/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta do FastAPI (por padrão é 8000)
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]