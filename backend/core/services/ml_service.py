from pathlib import Path
import joblib #type:ignore
import random

from ..ml import N_CLASSES, gerar_dataset, prever_com_modelo, treinar_modelo

from ..models import Previsao
from ..regras_jogo import (
    DEZENA_MAX,
    DEZENA_MIN,
    QTD_DEZENAS_PREVISAO,
    completar_dezenas_previsao,
)

# Arquivo novo: modelos antigos (100 classes, vetor 200) são ignorados.
MODEL_PATH = Path(__file__).resolve().parents[2] / "modelo_lotofacil.pkl"


def obter_modelo(listas, retrain=False):
    if MODEL_PATH.exists() and not retrain:
        try:
            loaded = joblib.load(MODEL_PATH)
            if (
                isinstance(loaded, list)
                and len(loaded) == N_CLASSES
            ):
                return loaded
        except Exception:
            pass
    
    X,y = gerar_dataset(listas)
    
    if X is None or len(X) < 5:
        return None
    
    modelos = treinar_modelo(X,y)
    joblib.dump(modelos, MODEL_PATH)
    
    return modelos


def _previsao_lotofacil_do_ranking(probabilidades):
    out = []
    for n, _ in probabilidades:
        if DEZENA_MIN <= n <= DEZENA_MAX and n not in out:
            out.append(n)
            if len(out) >= QTD_DEZENAS_PREVISAO:
                break
    for x in range(DEZENA_MIN, DEZENA_MAX + 1):
        if len(out) >= QTD_DEZENAS_PREVISAO:
            break
        if x not in out:
            out.append(x)
    return out[:QTD_DEZENAS_PREVISAO]


def previsao_machine_learning(listas,retrain=False):
    modelos = obter_modelo(listas, retrain)
    
    if not modelos:
        return {"erro": "Modelo indisponível"}
    
    raw = prever_com_modelo(modelos, listas, top_n=N_CLASSES)
    previsao = completar_dezenas_previsao(
        _previsao_lotofacil_do_ranking(raw["top_probabilidades"])
    )
    return {
        "previsao": previsao,
        "top_probabilidades": raw["top_probabilidades"][:QTD_DEZENAS_PREVISAO],
    }

def adicionar_ruido(previsao, intensidade=0.2):
    novos = list(previsao)
    for i in range(len(novos)):
        if random.random() < intensidade:
            novos[i] = random.randint(DEZENA_MIN, DEZENA_MAX)
    out = list(dict.fromkeys(novos))
    pool = [n for n in range(DEZENA_MIN, DEZENA_MAX + 1) if n not in out]
    random.shuffle(pool)
    while len(out) < QTD_DEZENAS_PREVISAO and pool:
        out.append(pool.pop())
    return out[:QTD_DEZENAS_PREVISAO]

def rodar_ml_em_background(listas):
    from .previsao_pipeline import gerar_previsao_ml_pipeline
    gerar_previsao_ml_pipeline(listas)
    