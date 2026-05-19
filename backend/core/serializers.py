from rest_framework import serializers #type:ignore
from .models import Lista,Resultado, Previsao
from .regras_jogo import DEZENA_MAX, DEZENA_MIN, QTD_DEZENAS_SORTEIO

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'
        
        
class ResultadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'

class PrevisaoSrializer(serializers.ModelSerializer):
    class Meta:
        model = Previsao
        fields = '__all__'
        
class ListaInputSerializer(serializers.Serializer):
    listas = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )

    def validate_listas(self, value):
        if not value:
            raise serializers.ValidationError("Envie ao menos uma lista.")

        for idx, lista in enumerate(value):
            if not isinstance(lista, list) or len(lista) == 0:
                raise serializers.ValidationError(f"Lista #{idx+1} vazia ou inválida.")

            if len(lista) != QTD_DEZENAS_SORTEIO:
                raise serializers.ValidationError(
                    f"Lista #{idx+1} deve ter exatamente {QTD_DEZENAS_SORTEIO} números."
                )

            if len(set(lista)) != len(lista):
                raise serializers.ValidationError(
                    f"Lista #{idx+1} não pode ter números repetidos."
                )

            for n in lista:
                if n < DEZENA_MIN or n > DEZENA_MAX:
                    raise serializers.ValidationError(
                        f"Número fora do intervalo {DEZENA_MIN}-{DEZENA_MAX} na lista #{idx+1}: {n}"
                    )

        return value


class ValidarPrevisaoSerializer(serializers.Serializer):
    numeros = serializers.ListField(
        child=serializers.IntegerField(min_value=DEZENA_MIN, max_value=DEZENA_MAX),
        allow_empty=False,
        min_length=QTD_DEZENAS_SORTEIO,
        max_length=QTD_DEZENAS_SORTEIO,
    )

    def validate_numeros(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Números não podem repetir.")
        return value