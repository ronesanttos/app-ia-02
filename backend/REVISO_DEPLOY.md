# 📋 Revisão Completa - Deploy Render

## ✅ Alterações Realizadas

### 1. **Procfile** (Novo)
- ✅ Definido release command com migrações
- ✅ Configurado web process com Gunicorn
- ✅ Configurado worker process com Celery

```
release: python manage.py migrate
web: gunicorn project.wsgi
worker: celery -A project worker -l info
```

### 2. **.env.example** (Atualizado)
Adicionadas variáveis faltantes:
- ✅ `DJANGO_DEBUG=false` para produção
- ✅ `DJANGO_ALLOWED_HOSTS` com exemplo de domínio Render
- ✅ `SECURE_SSL_REDIRECT=true` para HTTPS
- ✅ `SESSION_COOKIE_SECURE=true`
- ✅ `CSRF_COOKIE_SECURE=true`
- ✅ `REDIS_URL` com documentação
- ✅ `DATABASE_URL` para PostgreSQL
- ✅ `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS`
- ✅ Comentários explicativos para cada seção

### 3. **project/settings.py** (Otimizado)
- ✅ REDIS_URL com fallback para localhost em dev
- ✅ CACHES melhorado com timeouts e compressão
- ✅ DATABASE_URL com suporte a PostgreSQL
- ✅ Configurações de SSL para Celery/Redis em produção

### 4. **Dockerfile** (Melhorado)
- ✅ Adicionados comentários sobre uso local vs Render
- ✅ Corrigido CMD para Gunicorn (era Celery)
- ✅ Exposto port 8000

### 5. **build.sh** (Atualizado)
- ✅ Melhor erro handling com `set -e`
- ✅ Adicionados emojis e mensagens informativas
- ✅ Compatível com build command do Render

### 6. **.gitignore** (Expandido)
- ✅ Adicionados padrões para Node, pytest, coverage
- ✅ Adicionados staticfiles/ e media/
- ✅ Melhor organização por categorias

### 7. **project/celery.py** (Otimizado)
- ✅ Removidas configurações hardcoded
- ✅ Agora usa settings.py como única fonte de verdade

### 8. **RENDER_DEPLOY.md** (Novo - Guia Completo)
- ✅ Instruções passo a passo para Render
- ✅ Configuração de Web Service, Worker, DB, Redis
- ✅ Variáveis de ambiente
- ✅ Troubleshooting detalhado
- ✅ Comandos úteis no Shell do Render

---

## 🚀 Como Fazer Deploy

### Pré-requisitos
1. Repositório Git com código atualizado
2. Conta no Render (gratuita)

### Passos Rápidos

1. **Commit e push das mudanças**
   ```bash
   git add .
   git commit -m "Preparar para deploy no Render"
   git push origin main
   ```

2. **Acesse o Render** → Dashboard
   - Clique em **New +**

3. **Crie um Web Service**
   - Repository: seu repositório
   - Root Directory: `apps/IA/backend`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn project.wsgi`

4. **Adicione Variáveis de Ambiente**
   ```
   DJANGO_DEBUG=false
   DJANGO_SECRET_KEY=<gere-uma-chave-segura>
   DJANGO_ALLOWED_HOSTS=seu-app.onrender.com
   CORS_ALLOWED_ORIGINS=https://seu-frontend.onrender.com
   ... (veja RENDER_DEPLOY.md para todas)
   ```

5. **Crie PostgreSQL** (para produção)
   - Clique em **New +** → PostgreSQL
   - Copie DATABASE_URL e adicione às variáveis

6. **Crie Redis** (para Celery)
   - Clique em **New +** → Redis
   - Copie REDIS_URL e adicione às variáveis

7. **Crie Worker** (Background Worker)
   - Start Command: `celery -A project worker -l info`
   - Mesmas variáveis de ambiente

8. **Deploy!**
   - Clique em **Create Web Service**
   - Render fará deploy automaticamente

---

## 📚 Recursos Importantes

| Arquivo | Propósito |
|---------|-----------|
| `Procfile` | Define como Render executa a app |
| `.env.example` | Template de variáveis (copie e configure) |
| `RENDER_DEPLOY.md` | Guia passo a passo para deploy |
| `requirements.txt` | Dependências Python |
| `build.sh` | Script de build automático |

---

## ⚠️ Checklist Antes do Deploy

- [ ] DJANGO_SECRET_KEY alterada (não use a padrão!)
- [ ] DJANGO_DEBUG=false em produção
- [ ] ALLOWED_HOSTS configurado com seu domínio
- [ ] PostgreSQL criado e DATABASE_URL configurado
- [ ] Redis criado e REDIS_URL configurado
- [ ] CORS_ALLOWED_ORIGINS com domínio correto
- [ ] Certificado SSL ativado (HTTPS)
- [ ] Admin Django criado: `python manage.py createsuperuser`

---

## 🔍 Verificação Pós-Deploy

Após o deploy, verifique:

```bash
# Admin Django
https://seu-app.onrender.com/admin

# API
https://seu-app.onrender.com/api/

# Health check
curl https://seu-app.onrender.com/
```

---

## 🐛 Troubleshooting Rápido

| Erro | Solução |
|------|---------|
| BUILD FAILED | Verifique `requirements.txt` e Python 3.12 compatibilidade |
| DJANGO_SECRET_KEY not found | Adicione variável no Render |
| 502 Bad Gateway | Aguarde build + migration terminar |
| No Redis connection | Crie Redis service e configure REDIS_URL |
| 404 Static files | Execute `python manage.py collectstatic` no Shell |

---

## 📞 Suporte

- 📖 [Render Docs](https://render.com/docs)
- 🐍 [Django Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- 📦 [Celery with Django](https://docs.celeryproject.org/en/stable/django/)

---

**Pronto para deploy!** 🎉
