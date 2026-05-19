"""
Regras do jogo (Lotofácil): universo 1–25; cada sorteio tem 15 dezenas distintas.
Cada lista cadastrada e a previsão usam essa mesma quantidade; na validação manual
o usuário informa um sorteio (15 números).
"""

DEZENA_MIN = 1
DEZENA_MAX = 25
QTD_DEZENAS_SORTEIO = 15
QTD_DEZENAS_PREVISAO = QTD_DEZENAS_SORTEIO


def completar_dezenas_previsao(
    numeros,
    qtd=QTD_DEZENAS_PREVISAO,
    vmin=DEZENA_MIN,
    vmax=DEZENA_MAX,
):
    """Garante exatamente `qtd` dezenas únicas no intervalo do jogo (ordem preservada + completar)."""
    seen = set()
    out = []
    for x in numeros:
        n = int(x)
        if vmin <= n <= vmax and n not in seen:
            seen.add(n)
            out.append(n)
        if len(out) >= qtd:
            return out[:qtd]
    for n in range(vmin, vmax + 1):
        if len(out) >= qtd:
            break
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out[:qtd]


# Quantas listas recentes entram nos pipelines de previsão / ML
LIMITE_LISTAS_CONSULTA_PADRAO = 100

# Mínimo de sorteios no histórico para tentar montar o dataset do ML
MIN_SORTEIOS_PARA_DATASET_ML = 15
