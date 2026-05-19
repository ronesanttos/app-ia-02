from ..models import Previsao
from ..regras_jogo import DEZENA_MAX, DEZENA_MIN
from ..utils import calcular_peso_previsao


def obter_bonus_por_numero():
    bonus = {i: 0 for i in range(DEZENA_MIN, DEZENA_MAX + 1)}
    
    previsoes = Previsao.objects.exclude(acuracia=None).order_by('-id')[:100]
    
    for p in previsoes:
        peso = calcular_peso_previsao(p)
        reais = set()
        for x in p.numeros_reais or []:
            try:
                r = int(x)
            except (TypeError, ValueError):
                continue
            if DEZENA_MIN <= r <= DEZENA_MAX:
                reais.add(r)

        for raw in p.numeros_previstos or []:
            try:
                n = int(raw)
            except (TypeError, ValueError):
                continue
            if not (DEZENA_MIN <= n <= DEZENA_MAX):
                continue
            if n in reais:
                bonus[n] += 0.2 * peso
            else:
                bonus[n] -= 0.1 * peso
                
    max_val = max(abs(v) for v in bonus.values()) or 1
    
    for k in bonus:
        bonus[k] /= max_val
        
    return bonus

def gerar_memoria_reforco():
    memoria = {i: 0 for i in range(DEZENA_MIN, DEZENA_MAX + 1)}
    
    previsoes = Previsao.objects.exclude(numeros_reais=None).order_by('-id')[:200]
    
    for p in previsoes:
        previstos = set()
        for x in p.numeros_previstos or []:
            try:
                n = int(x)
            except (TypeError, ValueError):
                continue
            if DEZENA_MIN <= n <= DEZENA_MAX:
                previstos.add(n)
        reais = set()
        for x in p.numeros_reais or []:
            try:
                n = int(x)
            except (TypeError, ValueError):
                continue
            if DEZENA_MIN <= n <= DEZENA_MAX:
                reais.add(n)

        acertos = previstos & reais
        erros = previstos - reais

        for n in acertos:
            memoria[n] += 1

        for n in erros:
            memoria[n] -= 0.5
            
    return memoria

def normalizar_memoria(memoria):
    max_val = max(abs(v) for v in memoria.values()) or 1
    
    return {k:v / max_val for k, v in memoria.items()}