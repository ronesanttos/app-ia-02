import numpy as np #type:ignore
from sklearn.ensemble import RandomForestClassifier #type:ignore
import joblib #type:ignore

from .regras_jogo import DEZENA_MAX, DEZENA_MIN, MIN_SORTEIOS_PARA_DATASET_ML
from .services.reinforcement_service import gerar_memoria_reforco, normalizar_memoria, obter_bonus_por_numero

_DEZENAS_ORDEM = tuple(range(DEZENA_MIN, DEZENA_MAX + 1))
N_CLASSES = len(_DEZENAS_ORDEM)


def gerar_dataset(listas, janela=5):
    x = []
    y = []

    if len(listas) < MIN_SORTEIOS_PARA_DATASET_ML:
        return None, None

    for i in range(janela, len(listas)):
        historico = listas[i - janela : i]
        proxima_lista = listas[i]

        vetor = []

        for num in _DEZENAS_ORDEM:
            freq = 0
            atraso = 0
            encontrado = False

            for idx, lista in enumerate(reversed(historico)):
                if num in lista:
                    freq += 1
                    if not encontrado:
                        atraso = idx
                        encontrado = True

            if not encontrado:
                atraso = janela

            vetor.append(freq / janela)
            vetor.append(atraso / janela)

        label = [1 if num in proxima_lista else 0 for num in _DEZENAS_ORDEM]

        x.append(vetor)
        y.append(label)

    return np.array(x), np.array(y)


def treinar_modelo(X, y):
    modelos = []

    for i in range(y.shape[1]):
        y_coluna = y[:, i]
        
        if len(set(y_coluna)) < 2:
            modelos.append(None)
            continue
        
        modelo = RandomForestClassifier(
            n_estimators=50,
            max_depth=8,
            min_samples_split=5,
            random_state=42,
            n_jobs=1,
        )
        
        modelo.fit(X, y_coluna)
        modelos.append(modelo)
        
    return modelos

def prever_com_modelo(modelos, listas, janela=5, top_n=None):

    if top_n is None:
        top_n = N_CLASSES

    modelos_pad = list(modelos[:N_CLASSES])
    while len(modelos_pad) < N_CLASSES:
        modelos_pad.append(None)

    bonus = obter_bonus_por_numero()
    memoria = normalizar_memoria(gerar_memoria_reforco())

    peso_modelo = 0.5
    peso_reforco = 0.3
    peso_bonus = 0.2

    historico = listas[-janela:]

    vetor = []

    for num in _DEZENAS_ORDEM:
        freq = 0
        atraso = 0
        encontrado = False

        for idx, lista in enumerate(reversed(historico)):
            if num in lista:
                freq += 1
                if not encontrado:
                    atraso = idx
                    encontrado = True

        if not encontrado:
            atraso = janela

        vetor.append(freq / janela)
        vetor.append(atraso / janela)

    cap = min(top_n, N_CLASSES)
    probabilidades = []

    for idx, modelo in enumerate(modelos_pad):
        if idx >= N_CLASSES:
            break
        num = _DEZENAS_ORDEM[idx]
        if modelo is None:
            prob = 0

        else:
            probs = modelo.predict_proba([vetor])[0]
            prob = float(probs[1] if len(probs) > 1 else 0)

        prob_reforco = memoria.get(num, 0)
        bonus_numero = bonus.get(num, 0)

        if prob < 0.2:
            peso_reforco += 0.1
            peso_modelo -= 0.1

        prob_ajustada = float(
            (prob * peso_modelo)
            + (prob_reforco * peso_reforco)
            + (bonus_numero * peso_bonus)
        )

        probabilidades.append((num, prob_ajustada))

    probabilidades.sort(key=lambda x: x[1], reverse=True)

    previsao = [n for n, _ in probabilidades[:cap]]

    return {
        "previsao": previsao,
        "top_probabilidades": probabilidades[:cap],
    }
    
    

def avaliacao_modelo(modelos, listas, janela=5, top_n=15):
    acerto_total = 0
    total_previsto = 0
    
    for i in range(janela,len(listas) - 1):
        historico = listas[:i]
        
        resultados = prever_com_modelo(modelos,historico, janela=janela, top_n=top_n)
        
        previsao = resultados["previsao"]
        real = listas[i]
        acertos = len(set(previsao) & set(real))
        
        acerto_total += acertos
        total_previsto += top_n
        
    taxa_acertos = acerto_total / total_previsto if total_previsto else 0
    
    return {
        "taxa_acerto": taxa_acertos
        
    }

def salvar_modelo(modelos, path="modelo_lotofacil.pkl"):
    joblib.dump(modelos, path)


def carregar_modelo(path="modelo_lotofacil.pkl"):
    return joblib.load(path)