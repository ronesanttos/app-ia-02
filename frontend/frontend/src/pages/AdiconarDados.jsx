import { useEffect, useMemo, useState } from "react";
import { apiFetch } from "../api/client.js";

/** Lotofácil: cada sorteio = 15 dezenas distintas entre 1 e 25. */
const TAMANHO_GRUPO = 15;
const DEZENA_MIN = 1;
const DEZENA_MAX = 25;

export default function AdicionarDados() {
    const [input, setInput] = useState("");
    const [formatado, setFormatado] = useState("");
    const [msg, setMsg] = useState("");

    // ♦ FORMATADOR
    function autoFormatar(texto) {
        const numeros = texto
            .split(/[\s,]+/)
            .map(Number)
            .filter(n => !isNaN(n));

        return numeros
            .map((n, i) => {
                const isLast = i === numeros.length - 1;
                const quebra = (i + 1) % TAMANHO_GRUPO === 0;

                if (quebra) return n + "\n";
                if (!isLast) return n + ", ";
                return n;
            })
            .join("")
            .trim();
    }

    // ♦ VALIDADOR + PARSER
    function processarEntrada(texto) {
        if (!texto.trim()) {
            return { erro: "Campo vazio", listas: [] };
        }

        const numeros = texto
            .split(/[\s,]+/)
            .map(Number)
            .filter(n => !isNaN(n));

        if (numeros.length === 0) {
            return { erro: "Nenhum número válido", listas: [] };
        }

        const fora = numeros.filter(
            n => !Number.isInteger(n) || n < DEZENA_MIN || n > DEZENA_MAX
        );
        if (fora.length) {
            return {
                erro: `Cada número deve ser inteiro entre ${DEZENA_MIN} e ${DEZENA_MAX}.`,
                listas: [],
            };
        }

        const listas = [];
        let aviso = "";

        for (let i = 0; i < numeros.length; i += TAMANHO_GRUPO) {
            const grupo = numeros.slice(i, i + TAMANHO_GRUPO);

            if (grupo.length !== TAMANHO_GRUPO) {
                return {
                    erro: `Último grupo incompleto (${grupo.length}/${TAMANHO_GRUPO})`,
                    listas,
                };
            }

            if (new Set(grupo).size !== grupo.length) {
                aviso = `⚠️ Duplicados detectados em ${grupo}`;
            }

            listas.push(grupo);
        }

        return { erro: aviso, listas };
    }


    // 🔹 AUTO FORMAT (DEBOUNCE)
    useEffect(() => {
        const timer = setTimeout(() => {
            setFormatado(autoFormatar(input));
        }, 400); // 500ms depois que parar de digitar

        return () => clearTimeout(timer);
    }, [input]);


    const { erro, listas: preview } = useMemo(
        () => processarEntrada(input),
        [input]
    );

    // 🔹 ENVIAR
    async function enviarDados() {
        try {
            let listas;

            if (input.trim().startsWith("[")) {
                try {
                    listas = JSON.parse(input);
                } catch {
                    setMsg("JSON inválido");
                    return;
                }
            } else {
                listas = preview;
            }

            console.log("LISTA ENVIADA", listas);

            const res = await apiFetch(`/api/listas/processar/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ listas })
            });

            const data = await res.json();

            console.log(data);

            setMsg("Dados enviados com sucesso!");
            setInput("");

        } catch {
            setMsg("Erro ao enviar dados");
        }
    }

    const totalNumeros = input
        .split(/[\s,]+/)
        .map(n => n.trim())
        .filter(n => n !== "")
        .length;

    const podeEnviar = preview.length > 0;

    return (
        <div>
            <h1>Adicionar Dados</h1>

            <textarea
                rows="6"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                style={{
                    border: erro ? "2px solid red" : "2px solid green"
                }}
            />

            <br /><br />

            <button
                onClick={enviarDados}
                disabled={!podeEnviar}
            >
                Enviar aqui
            </button>

            <h3>Formato automático:</h3>
            <pre>{formatado}</pre>

            {erro && (
                <p style={{
                    color: erro.includes("⚠️") ? "orange" : "red",
                    fontWeight: "bold"
                }}>
                    {erro}
                </p>
            )}

            {preview.length > 0 && (
                <div>
                    <h3>Preview:</h3>
                    {preview.map((lista, i) => (
                        <p key={i}>{lista.join(", ")}</p>
                    ))}
                </div>
            )}
            <p>Total de números: {totalNumeros}</p>
            <p>{msg}</p>
        </div>
    );
}
