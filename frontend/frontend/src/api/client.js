const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(
  /\/$/,
  ""
);
const API_KEY = import.meta.env.VITE_API_KEY || "";

/**
 * Monta URL absoluta para o backend (ex.: `/api/listas/previsao/`).
 */
export function apiUrl(path) {
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE}${p}`;
}

/**
 * fetch com headers padrão (JSON + API key opcional).
 */
export function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});

  if (
    options.body != null &&
    typeof options.body === "string" &&
    !headers.has("Content-Type")
  ) {
    headers.set("Content-Type", "application/json");
  }

  if (API_KEY) {
    headers.set("X-API-KEY", API_KEY);
  }

  return fetch(apiUrl(path), { ...options, headers });
}

/**
 * Converte um campo de erro da API em texto legível.
 * Evita o bug clássico: String([38]) === "38" e String(38) === "38" sem contexto.
 */
export function formatApiErrorValue(value) {
  if (value == null) return "";

  const mentions38 =
    value === 38 ||
    value === "38" ||
    (Array.isArray(value) && value.some((x) => x === 38 || x === "38"));

  const hint38 = mentions38
    ? " — Valor 38 costuma ser errno do sistema (ex.: ENOSYS no Linux ou I/O no Windows: Redis, Docker, joblib/modelo .pkl, pasta em rede). Confira o terminal do worker Celery e os logs do Django."
    : "";

  if (typeof value === "string") {
    return value + hint38;
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return `Resposta do servidor (${typeof value}): ${String(value)}${hint38}`;
  }
  if (Array.isArray(value)) {
    const parts = value
      .map((item) => {
        if (item == null) return "";
        if (typeof item === "string") return item;
        if (typeof item === "number" || typeof item === "boolean") return String(item);
        if (typeof item === "object" && item !== null && typeof item.string === "string") {
          return item.string;
        }
        try {
          return JSON.stringify(item);
        } catch {
          return String(item);
        }
      })
      .filter(Boolean);
    const body = parts.length ? parts.join("; ") : "Lista de detalhes vazia";
    return body + hint38;
  }
  if (typeof value === "object") {
    try {
      return JSON.stringify(value) + hint38;
    } catch {
      return String(value) + hint38;
    }
  }
  return String(value) + hint38;
}

/**
 * Lê corpo de erro (DRF costuma usar `detail`, throttling, etc.).
 */
export async function readApiError(response) {
  const text = await response.text();
  try {
    const data = JSON.parse(text);
    if (typeof data === "string") {
      return data;
    }
    if (data === null || typeof data !== "object") {
      return formatApiErrorValue(data) || `HTTP ${response.status}`;
    }

    if (data.detail !== undefined && data.detail !== null) {
      if (typeof data.detail === "string") {
        return data.detail;
      }
      return formatApiErrorValue(data.detail) || `HTTP ${response.status}`;
    }
    if (data.erro !== undefined && data.erro !== null) {
      return formatApiErrorValue(data.erro) || `HTTP ${response.status}`;
    }
    if (data.message !== undefined && data.message !== null) {
      return formatApiErrorValue(data.message) || `HTTP ${response.status}`;
    }
    if (data.non_field_errors !== undefined && data.non_field_errors !== null) {
      return formatApiErrorValue(data.non_field_errors) || `HTTP ${response.status}`;
    }
    return text?.slice(0, 400) || `HTTP ${response.status}`;
  } catch {
    return text?.slice(0, 400) || `HTTP ${response.status}`;
  }
}
