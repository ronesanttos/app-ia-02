# Este Dockerfile é para desenvolvimento local com Docker/Docker-Compose
# Para deploy no Render, use o Procfile e variáveis de ambiente
#
# Build: docker build -t meu-app .
# Run: docker run -p 8000:8000 meu-app

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Para desenvolvimento, use docker-compose com volumes
# Para produção, use Render com Procfile

# Web server (Gunicorn)
EXPOSE 8000
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]

