import { useEffect, useState } from "react";
import { apiFetch } from "../api/client.js";

/**
 * Lotofácil: universo 1–25; cada sorteio (lista) e a validação manual usam 15 dezenas;
 * a previsão também deve ter 15 números nesse intervalo.
 */
const DEZENA_MIN = 1;
const DEZENA_MAX = 25;
const QTD_PREVISAO = 15;
const QTD_RESULTADO_VALIDACAO = 15;

/** Quantas listas o endpoint retorna (usa-se só a mais recente para preencher o sorteio). */
const LISTAS_REFERENCIA = 6;

export default function ValidarPrevisao() {
    const [previsoes, setPrevisoes] = useState([]);
    const [input, setInput] = useState("");
    const [resultado, setResultado] = useState(null);
    const [selecionado, setSelecionado] = useState(null);
    const [validandoAuto, setValidandoAuto] = useState(false);

    // 🔹 carregar previsões
    useEffect(() => {
        apiFetch(`/api/listas/previsoes/?limit=50`)
            .then(res => res.json())
            .then(setPrevisoes);
    }, []);


    // 🔹 converter input → array
    function parseNumeros(texto) {
        return texto
            .split(/[\s,]+/)
            .map(Number)
            .filter(n => !isNaN(n));
    }

    function mensagemValidacaoLocal(numeros) {
        if (!numeros.length) {
            return "Nenhum número válido para validar.";
        }
        const fora = numeros.filter(
            n => !Number.isInteger(n) || n < DEZENA_MIN || n > DEZENA_MAX
        );
        if (fora.length) {
            return `Cada número deve ser inteiro entre ${DEZENA_MIN} e ${DEZENA_MAX}.`;
        }
        if (new Set(numeros).size !== numeros.length) {
            return "Não use números repetidos.";
        }
        if (numeros.length !== QTD_RESULTADO_VALIDACAO) {
            return `Informe exatamente ${QTD_RESULTADO_VALIDACAO} números (um sorteio).`;
        }
        return null;
    }

    async function validarComNumeros(numeros) {
        if (!selecionado) {
            alert("Selecione uma previsão");
            return;
        }
        const msg = mensagemValidacaoLocal(numeros);
        if (msg) {
            alert(msg);
            return;
        }

        const res = await apiFetch(`/api/listas/${selecionado}/validar/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ numeros }),
        });

        const data = await res.json();
        if (data.erro) {
            alert(data.erro);
            return;
        }
        setResultado(data);
    }

    // 🔹 validar previsão
    async function validar() {
        await validarComNumeros(parseNumeros(input));
    }

    /**
     * Busca as últimas N listas cadastradas, monta a referência como união dos
     * números sorteados nelas, preenche o campo e valida a previsão selecionada.
     */
    async function validarAutomatico() {
        if (!selecionado) {
            alert("Selecione uma previsão");
            return;
        }
        setValidandoAuto(true);
        try {
            const res = await apiFetch(
                `/api/listas/ultimas_listas/?limite=${LISTAS_REFERENCIA}`
            );
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                alert(
                    data.erro ||
                        "Não foi possível obter as listas de sorteio de referência"
                );
                return;
            }
            const ultima = Array.isArray(data.listas) ? data.listas[0] : null;
            const numeros = Array.isArray(ultima?.numeros) ? ultima.numeros : [];
            if (numeros.length !== QTD_RESULTADO_VALIDACAO) {
                alert(
                    numeros.length
                        ? `A lista mais recente tem ${numeros.length} números; são necessários ${QTD_RESULTADO_VALIDACAO} (Lotofácil).`
                        : "Não foi possível obter o último sorteio."
                );
                return;
            }
            setInput(numeros.join(", "));
            await validarComNumeros(numeros);
        } finally {
            setValidandoAuto(false);
        }
    }

    // 🔹 destacar acertos
    function renderComparacao(previstos, reais) {
        return previstos.map((n, i) => {
            const acertou = reais.includes(n);

            return (
                <span
                    key={i}
                    style={{
                        color: acertou ? "limegreen" : "red",
                        marginRight: "6px",
                        fontWeight: "bold"
                    }}
                >
                    {n}
                </span>
            );
        });
    }

    return (
        <div>
            <h1>Validar Previsão</h1>

            {/* 🔹 selecionar previsão */}
            <select onChange={(e) => {setSelecionado(Number(e.target.value));setResultado(null)}}>
                
                <option value="">Selecione</option>
                {previsoes.map(p => (
                    <option key={p.id} value={p.id}>
                        #{p.id} | {p.tipo} | {p.numeros.slice(0, 3).join(", ")}...
                    </option>
                ))}
            </select>

            <br /><br />

            {/* 🔹 input números reais */}
            <textarea
                placeholder={`Sorteio: ${QTD_RESULTADO_VALIDACAO} números inteiros entre ${DEZENA_MIN} e ${DEZENA_MAX} (ex: 1, 5, 7, 8, …)`}
                value={input}
                onChange={(e) => setInput(e.target.value)}
            />

            <br /><br />

            <button onClick={validar} disabled={validandoAuto}>
                Validar
            </button>
            {" "}
            <button type="button" onClick={validarAutomatico} disabled={validandoAuto}>
                {validandoAuto
                    ? "Validando…"
                    : `Validar automaticamente (últimas ${LISTAS_REFERENCIA} listas)`}
            </button>
            <p style={{ fontSize: "0.9rem", color: "#555", maxWidth: "36rem" }}>
                Validação automática: preenche com o sorteio mais recente (última lista
                cadastrada entre as {LISTAS_REFERENCIA} buscadas). Cada sorteio tem{" "}
                {QTD_RESULTADO_VALIDACAO} dezenas distintas de {DEZENA_MIN} a {DEZENA_MAX}.
                A previsão comparada também deve ter {QTD_PREVISAO} números nesse intervalo.
            </p>

            {/* 🔹 resultado */}
            {resultado && (
                <div>
                    <h2>Resultado</h2>

                    <p>Acertos: {resultado.acertos}</p>
                    <p>Total: {resultado.total}</p>
                    <p>
                        Acurácia: {(resultado.acuracia * 100).toFixed(1)}%
                    </p>

                    <p>Data da previsão: {resultado.data_previsao}</p>
                </div>
            )}

            {/* 🔹 comparação visual */}
            {resultado && selecionado && (
                <div>
                    <h3>Comparação</h3>

                    {renderComparacao(
                        previsoes.find(p => p.id == selecionado)
                            ?.numeros || [],
                        parseNumeros(input)
                    )}
                </div>
            )}
        </div>
    );
}


