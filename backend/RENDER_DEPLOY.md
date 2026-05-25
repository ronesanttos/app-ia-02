# Guia de Deploy no Render

## Pré-requisitos
- Conta no [Render](https://render.com)
- Repositório GitHub com o código
- Variáveis de ambiente configuradas

## Passo 1: Preparar o Repositório

Certifique-se de que os seguintes arquivos estão na raiz do `backend/`:
- ✅ `Procfile` - Define os processos (web, worker, release)
- ✅ `requirements.txt` - Dependências Python
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `manage.py` - Django management
- ✅ `project/settings.py` - Configurações (já otimizado para Render)

## Passo 2: Variáveis de Ambiente no Render

No painel do Render, configure as seguintes variáveis:

```env
# Segurança e Django
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<gere-uma-chave-segura-de-50+-caracteres>
DJANGO_ALLOWED_HOSTS=seu-app.onrender.com,seu-dominio.com.br
DJANGO_LOG_LEVEL=INFO

# Segurança HTTPS
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true

# CORS/CSRF (ajuste conforme seu frontend)
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=https://seu-frontend.onrender.com
CSRF_TRUSTED_ORIGINS=https://seu-frontend.onrender.com

# Database - PostgreSQL (Render fornece automaticamente em planos pagos)
# Se usar PostgreSQL gratuito do Render:
DATABASE_URL=postgresql://user:password@host:port/dbname

# Redis - Render fornece automaticamente
# REDIS_URL será injetado automaticamente pelo Render

# Celery
CELERY_TASK_TIME_LIMIT=300
CELERY_TASK_SOFT_TIME_LIMIT=270
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=true
```

### Como Gerar DJANGO_SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Passo 3: Criar Serviços no Render

### 3.1 Serviço Web (Django + Gunicorn)

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **New +** → **Web Service**
3. Configure:
   - **Repository**: seu repositório GitHub
   - **Branch**: `main` (ou sua branch principal)
   - **Root Directory**: `apps/IA/backend`
   - **Runtime**: Python 3.12
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     gunicorn project.wsgi
     ```
   - **Plan**: Standard (mínimo) ou superior

4. Clique em **Create Web Service**

### 3.2 Serviço Worker (Celery)

1. Clique em **New +** → **Background Worker**
2. Configure:
   - **Repository**: mesmo repositório
   - **Branch**: `main`
   - **Root Directory**: `apps/IA/backend`
   - **Runtime**: Python 3.12
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     celery -A project worker -l info
     ```

3. Clique em **Create Background Worker**

### 3.3 Banco de Dados (PostgreSQL)

1. Clique em **New +** → **PostgreSQL**
2. Configure o nome e plano
3. Copie a `DATABASE_URL` fornecida
4. Adicione como variável de ambiente nos serviços

### 3.4 Redis (Cache/Broker)

1. Clique em **New +** → **Redis**
2. Configure nome e plano
3. Copie a `REDIS_URL` fornecida
4. Adicione como variável de ambiente nos serviços

## Passo 4: Adicionar Variáveis de Ambiente

Para cada serviço (Web e Worker):

1. Acesse **Settings** do serviço
2. Scroll até **Environment**
3. Clique em **Add Environment Variable**
4. Adicione todas as variáveis listadas no **Passo 2**

## Passo 5: Deploy

O Render fará deploy automaticamente quando você:
- Fazer push para a branch configurada
- Clicar em **Manual Deploy** no painel

### Monitorar o Deploy

1. Acesse **Logs** na página do serviço
2. Verifique se:
   - ✅ Build passou
   - ✅ Migrações executaram
   - ✅ Static files foram coletados
   - ✅ Serviço está rodando

## Troubleshooting

### ❌ Erro: "DJANGO_SECRET_KEY não configurada"
- Verifique se a variável está definida no Render
- Regenere com o comando acima

### ❌ Erro: "Celery broker não responde"
- Redis_URL pode estar vazio
- Crie um serviço Redis no Render
- Adicione REDIS_URL como variável de ambiente

### ❌ Erro: "Database connection refused"
- Crie PostgreSQL no Render
- Adicione DATABASE_URL como variável de ambiente
- Execute migrations manualmente no painel

### ❌ Erro: "Arquivo estático não encontrado (404)"
- Execute no painel:
  ```bash
  python manage.py collectstatic --noinput
  ```

## Comandos Úteis no Painel Render

Acesse **Shell** para executar:

```bash
# Migrações
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Coletar static files
python manage.py collectstatic --noinput

# Listar migrations
python manage.py showmigrations
```

## Estrutura Recomendada no Git

```
apps/IA/
├── backend/                    # Este diretório
│   ├── Procfile               # ✅ Criado
│   ├── requirements.txt       # ✅ Verificado
│   ├── .env.example           # ✅ Atualizado
│   ├── manage.py
│   ├── project/
│   │   ├── settings.py        # ✅ Otimizado
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── core/
│   └── staticfiles/           # Será criado no build
└── frontend/                   # Se houver
```

## Verificação Final

Após o deploy, acesse:

1. **Admin Django**: `https://seu-app.onrender.com/admin`
2. **API**: `https://seu-app.onrender.com/api/`
3. **Status do Worker**: Verifique logs de `celery` na aba Logs

## Limpeza e Otimização

- ❌ Remova arquivos desnecessários do repositório:
  - `db.sqlite3` (local development)
  - `db_old.sqlite3`
  - `.env` (use `.env.example`)
  
- ✅ Mantenha no `.gitignore`:
  ```
  .env
  db.sqlite3
  staticfiles/
  __pycache__/
  .venv/
  ```

## Próximos Passos

1. Teste localmente com `docker-compose`
2. Commit e push para GitHub
3. Configure os serviços no Render
4. Monitore os logs
5. Configure domínio customizado (opcional)

---

**Dúvidas?** Consulte a [documentação oficial do Render](https://render.com/docs)
