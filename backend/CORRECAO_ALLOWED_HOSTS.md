# 🔧 Erro: ALLOWED_HOSTS Inválido no Render

## Status: ✅ SOLUÇÃO RÁPIDA

Você recebeu o erro:
```
Cabeçalho HTTP_HOST inválido: 'app-ia-01-backend.onrender.com'. 
Talvez seja necessário adicionar 'app-ia-01-backend.onrender.com' à lista ALLOWED_HOSTS.
```

---

## 🎯 Solução: Adicionar DJANGO_ALLOWED_HOSTS no Render

### Passo 1: Acesse o Painel Render

1. Vá para https://dashboard.render.com
2. Clique no seu Web Service (app-ia-01-backend)
3. Acesse a aba **Settings**

### Passo 2: Editar Variáveis de Ambiente

1. Scroll até **Environment**
2. Procure por `DJANGO_ALLOWED_HOSTS`
3. Se não existir, clique em **Add Environment Variable**

### Passo 3: Configurar o Valor

Adicione ou edite a variável com:

```
DJANGO_ALLOWED_HOSTS=app-ia-01-backend.onrender.com,seu-dominio-customizado.com.br
```

**Explicação**:
- `app-ia-01-backend.onrender.com` = domínio automático Render (use o SEU específico!)
- `seu-dominio-customizado.com.br` = seu domínio próprio (se tiver)
- Separar múltiplos com vírgula

### Passo 4: Salvar e Redeploy

1. Clique em **Save** (ou **Update**)
2. Render fará re-deploy automático
3. Aguarde até aparecer "✓ Deploy succeeded"

---

## ✅ Verificação

Após o redeploy, acesse:

```
https://app-ia-01-backend.onrender.com
```

Deve funcionar sem o erro 502/SuspiciousOperation!

---

## 📝 Variável Completa (Recomendado)

Se quiser adicionar múltiplos domínios, use:

```
DJANGO_ALLOWED_HOSTS=app-ia-01-backend.onrender.com,localhost,127.0.0.1
```

---

## 🚨 Importante!

- Cada domínio que será acessado DEVE estar em ALLOWED_HOSTS
- Use o domínio EXATO fornecido pelo Render
- Não use `*` em produção (inseguro)

---

## 💡 Próximas Vezes

Para evitar esse erro no futuro:

**No `.env.example`**:
```env
# Adicione na primeira vez:
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,seu-app.onrender.com
```

**No Render**:
```
Configure DJANGO_ALLOWED_HOSTS assim que criar o serviço
```

---

## 📚 Referência Rápida

| Local | Variável | Valor |
|-------|----------|-------|
| Render | `DJANGO_ALLOWED_HOSTS` | `app-ia-01-backend.onrender.com` |
| Local (.env) | `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` |
| Production | `DJANGO_ALLOWED_HOSTS` | `seu-dominio.com.br,www.seu-dominio.com.br` |

---

Pronto! O erro deve desaparecer após o redeploy. ✨
