#!/usr/bin/env bash
# Script de build para deploy (compatible com Render)
# Render executa este script automaticamente se existir
# Caso contrário, usa o Build Command definido no painel

set -e  # Exit on error

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "🧹 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🗄️  Executando migrações..."
python manage.py migrate

echo "✅ Build concluído com sucesso!"
