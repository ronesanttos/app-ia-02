from collections import Counter
from .aprendizado_service import extrair_padroes_erro
from ..regras_jogo import DEZENA_MAX, DEZENA_MIN, QTD_DEZENAS_PREVISAO

def calcular_frequencia(listas):
    todos_numeros = [num for lista in listas for num in lista]
    frequencia = Counter(todos_numeros)

    # ordena do mais frequente para o menos frequente
    frequencia_ordenada = dict(sorted(frequencia.items(), key=lambda x: x[1], reverse=True))

    return frequencia_ordenada


def prever_inteligente_v2(listas, tamanho_lista=QTD_DEZENAS_PREVISAO):
    # Aceita duplicados na entrada, mas calcula em cima de listas deduplicadas
    from ..utils import deduplicar_listas
    listas = deduplicar_listas(listas)
    freq = calcular_frequencia(listas)
    candidatos = sorted(
        (k for k in freq if DEZENA_MIN <= k <= DEZENA_MAX),
        key=lambda k: freq[k],
        reverse=True,
    )
    previsao = candidatos[:tamanho_lista]
    
    return {
        "previsao": previsao,
        "score": freq
    }
    
    
def prever_com_aprendizado(listas, tamanho=QTD_DEZENAS_PREVISAO):
    from ..utils import calcular_score_final
    
    score = calcular_score_final(listas)
    
    apredizado = extrair_padroes_erro()
    
    erros = apredizado["erros"]
    acertos = apredizado["acertos"]
    
    score_ajustado = {}
    
    for num, valor in score.items():
        bonus = acertos.get(num,0) * 0.1
        penalidade = erros.get(num,0) * 0.1
        
        score_ajustado[num] = valor + bonus - penalidade
        
    ordenado = sorted(
        ((n, v) for n, v in score_ajustado.items() if DEZENA_MIN <= n <= DEZENA_MAX),
        key=lambda x: x[1],
        reverse=True,
    )

    previsao = [num for num, _ in ordenado[:tamanho]]
    
    return {
        "previsao": previsao,
        "score": dict(ordenado[:20])
    }