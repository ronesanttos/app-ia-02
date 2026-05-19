from collections import Counter

from ..regras_jogo import DEZENA_MAX, DEZENA_MIN

def processar_listas(listas):
    todos_numeros = [num for lista in listas for num in lista]
    
    contagem = Counter(todos_numeros)
    
    nao_repete = [n for n, q in contagem.items() if q == 1]
    repete = [n for n, q in contagem.items() if q > 1]
    
    universo = set(range(DEZENA_MIN, DEZENA_MAX + 1))
    falta = list(universo - set(todos_numeros))
    
    return {
        "nao_repete": sorted(nao_repete),
        "repete": sorted(repete),
        "falta": sorted(falta),
    }
    
