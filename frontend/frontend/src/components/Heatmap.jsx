export default function Heatmap({ items = [] }) {
  const map = new Map();
  for (const it of items) {
    if (it && typeof it.numero === "number") {
      map.set(it.numero, Number(it.frequencia) || 0);
    }
  }

  const freqs = [];
  for (let n = 1; n <= 25; n++) {
    freqs.push(map.get(n) ?? 0);
  }
  const max = Math.max(...freqs, 0);

  return (
    <div className="heatmap-wrap" aria-label="Mapa de calor de frequência por número">
      <div className="heatmap-grid">
        {freqs.map((freq, index) => {
          const num = index + 1;
          const t = freq / max;
          const hue = 265;
          const sat = 35 + t * 55;
          const light = 88 - t * 52;
          const bg = `hsl(${hue} ${sat}% ${light}%)`;
          const fg = light < 52 ? "#f9fafb" : "#111827";

          return (
            <div
              key={num}
              className="heatmap-cell"
              style={{ background: bg, color: fg }}
              title={`${num}: ${freq} ocorrências`}
            >
              {num}
            </div>
          );
        })}
      </div>
      <p className="heatmap-legend">
        Mais escuro = maior frequência nas listas recentes (1-25).
      </p>
    </div>
  );
}
