import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase

from .models import Lista
from .regras_jogo import QTD_DEZENAS_PREVISAO
from .services.previsao_pipeline import gerar_previsao_ml_pipeline


def _sorteio_lotofacil(offset):
    """15 dezenas distintas entre 1 e 25 (determinístico)."""
    seq = list(range(1, 26)) * 2
    return seq[offset : offset + 15]


class PrevisaoMlPipelineTests(TestCase):
    """Integração leve do pipeline ML (treina RF em disco temporário)."""

    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False)
        self._tmp.close()
        self._model_path = Path(self._tmp.name)
        self._patch = patch("core.services.ml_service.MODEL_PATH", self._model_path)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        try:
            os.unlink(self._tmp.name)
        except OSError:
            pass

    def test_previsao_ml_retorna_15_dezenas_validas(self):
        for i in range(12):
            Lista.objects.create(numeros=_sorteio_lotofacil(i))

        listas = list(
            Lista.objects.order_by("-id").values_list("numeros", flat=True)[:100]
        )

        resultado = gerar_previsao_ml_pipeline(listas, salvar=False)

        self.assertTrue(resultado.get("success"), msg=resultado)
        data = resultado.get("data") or {}
        prev = data.get("previsao")
        self.assertIsInstance(prev, list)
        self.assertEqual(len(prev), QTD_DEZENAS_PREVISAO)
        self.assertEqual(len(prev), len(set(prev)))
        for n in prev:
            self.assertTrue(1 <= n <= 25, msg=n)

        probs = data.get("probabilidades") or []
        self.assertIsInstance(probs, list)
        for item in probs:
            self.assertIsInstance(item, list)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], int)
            self.assertIsInstance(item[1], float)
