import os
import ssl
from celery import Celery  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

# Carregar configurações do Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-descobrir tasks nas apps
app.autodiscover_tasks()

# Configurações padrão otimizadas
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}

# ⚠️ OTIMIZADO: Sem result backend (fire-and-forget tasks)
# Evita auto-consumo de Redis mantendo só o broker ativo

