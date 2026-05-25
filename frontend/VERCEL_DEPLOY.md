# Guia de Deploy no Vercel - Frontend React + Vite

## Pré-requisitos
- Conta no [Vercel](https://vercel.com)
- Repositório GitHub com o código
- Backend deployado no Render (com URL disponível)

---

## Passo 1: Preparar o Repositório

Certifique-se de que os seguintes arquivos estão na raiz do `frontend/`:

### ✅ Criar `.env.production`
Adicione este arquivo com a URL do seu backend no Render:

```env
# URL do backend no Render (SEM barra no final)
VITE_API_BASE_URL=https://seu-app.onrender.com

# Se usar API Key no backend, adicione também:
# VITE_API_KEY=sua-chave-api
```

### ✅ Criar `vercel.json`
Arquivo de configuração para Vercel (routing, rewrites, headers):

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "cleanUrls": true,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/"
    }
  ],
  "headers": [
    {
      "source": "/index.html",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-cache, no-store, must-revalidate"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### ✅ Verificar `.gitignore`
Certifique-se que estes arquivos estão ignorados:

```gitignore
# Variáveis locais (não commit)
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build output
dist/
dist-ssr/
*.local

# Dependencies
node_modules/

# Editor
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### ✅ Verificar `package.json`
Certifique-se que tem os scripts corretos:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  }
}
```

---

## Passo 2: Conectar GitHub ao Vercel

1. Acesse [Vercel Dashboard](https://vercel.com/dashboard)
2. Clique em **Add New...** → **Project**
3. Clique em **Import Git Repository**
4. Selecione seu repositório GitHub
5. Clique em **Continue**

---

## Passo 3: Configurar o Projeto no Vercel

Na página de importação, configure:

### ✅ Project Settings
- **Framework Preset**: Vite
- **Root Directory**: `apps/IA/frontend/frontend` (ou o caminho relativo do seu frontend)
- **Build Command**: `npm run build` (padrão)
- **Output Directory**: `dist` (padrão)
- **Install Command**: `npm install` (padrão)

### ✅ Environment Variables
1. Clique em **Environment Variables**
2. Adicione:
   ```
   VITE_API_BASE_URL = https://seu-app.onrender.com
   ```

Se usar API Key:
   ```
   VITE_API_KEY = sua-chave-api-aqui
   ```

3. Selecione os ambientes: **Production**, **Preview**, **Development**

---

## Passo 4: Deploy

1. Clique em **Deploy**
2. Aguarde o build completar (normalmente 2-3 minutos)
3. Quando terminar, você receberá a URL: `https://seu-projeto.vercel.app`

---

## Passo 5: Configurar Domínio Customizado (Opcional)

Se quiser usar um domínio próprio:

1. No dashboard do projeto, vá em **Settings** → **Domains**
2. Clique em **Add**
3. Adicione seu domínio
4. Configure os DNS records conforme instruções

---

## Passo 6: Verificar CORS (Importante!)

Se o frontend não conseguir se comunicar com o backend, é provável que seja um erro de **CORS**.

### No Backend (Django - Render)

Certifique-se de que no `settings.py` você tem:

```python
CORS_ALLOWED_ORIGINS = [
    "https://seu-projeto.vercel.app",  # ← Seu frontend
    "http://localhost:3000",  # ← Desenvolvimento local
]

CSRF_TRUSTED_ORIGINS = [
    "https://seu-projeto.vercel.app",
]
```

### Redeploy do Backend
Depois de atualizar o `settings.py`, faça:
```bash
git push  # Push para GitHub
# O Render vai fazer redeploy automaticamente
```

---

## Troubleshooting

### ❌ Erro: "Build failed"
- Verifique se todos os arquivos `.jsx` estão importados corretamente
- Verifique se não há erros de linting
- Veja os logs completos no painel da Vercel

### ❌ Erro: "Cannot GET /"
- Verifique se o `vercel.json` está configurado com rewrites
- Pode ser também que a build não tenha criado o `dist/` corretamente

### ❌ Erro: "API calls retornam 403 Forbidden"
- Verifique se `VITE_API_BASE_URL` está correto
- Verifique se `CORS_ALLOWED_ORIGINS` no backend inclui o domínio do Vercel

### ❌ Erro: "CORS error - preflight request failed"
- Adicione o domínio Vercel em `CORS_ALLOWED_ORIGINS` no backend
- Faça redeploy do backend

### ❌ Erro: "API Key retorna 403"
- Verifique se `VITE_API_KEY` está configurado no Vercel
- Verifique se a chave está correta no backend

---

## Como Testar Localmente Antes de Deploy

```bash
# 1. Instalar dependências
npm install

# 2. Build local (como será em produção)
npm run build

# 3. Preview da build
npm run preview
```

Abra `http://localhost:4173` e teste todas as funcionalidades.

---

## Monitorar o Deploy

No dashboard do Vercel, você pode:

1. **Ver logs de build**: Clique em **Deployments** → selecione o deploy → **Build Logs**
2. **Ver logs de runtime**: Clique em **Logs** → **Runtime Logs**
3. **Rollback**: Se algo der errado, clique em **Promote** em um deploy anterior

---

## Atualizar o Frontend (Próximos Deploys)

Cada vez que você fizer `git push` para `main`, o Vercel vai fazer deploy automaticamente:

1. Edite seus arquivos localmente
2. Faça commit:
   ```bash
   git add .
   git commit -m "sua mensagem"
   git push origin main
   ```
3. Vercel detecta a mudança e inicia o build
4. Quando terminar, sua app está atualizada automaticamente

---

## Estrutura Recomendada no Git

```
apps/IA/
├── backend/                    # Django
│   ├── project/
│   ├── core/
│   ├── Procfile
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── VERCEL_DEPLOY.md       # ← Este arquivo
│   ├── vercel.json            # ← Criado
│   ├── .env.production        # ← Criado
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   └── public/
```

---

## Links Úteis

- 🔗 [Documentação Vercel](https://vercel.com/docs)
- 🔗 [Deploy Vite no Vercel](https://vercel.com/guides/deploying-vite-with-vercel)
- 🔗 [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)

---

**Pronto para deploy!** 🚀
