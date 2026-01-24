export default function CenterPanel({ channels }) {
  const entries = Object.entries(channels)
    .map(([ch, count]) => ({ ch: Number(ch), count }))
    .sort((a, b) => a.ch - b.ch);

  return (
    <div className="h-full p-4">
      <div className="h-full rounded-xl border border-zinc-800 bg-zinc-950 p-4 flex flex-col">

        <div className="text-sm text-zinc-400 mb-3">
          Channel Activity Heatmap
        </div>

        {entries.length === 0 ? (
          <div className="flex-1 flex items-center justify-center text-zinc-500">
            Waiting for channel data…
          </div>
        ) : (
          <div className="grid grid-cols-13 gap-2">
            {entries.map(({ ch, count }) => (
              <div
                key={ch}
                className="h-16 rounded flex flex-col items-center justify-center text-xs border border-zinc-800"
                style={{
                  background: heatColor(count),
                }}
              >
                <div className="text-zinc-300">ch {ch}</div>
                <div className="text-zinc-400">{count} APs</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function heatColor(v) {
  if (v <= 1) return "rgba(37,99,235,0.25)";   // blue
  if (v <= 3) return "rgba(234,179,8,0.35)";  // yellow
  return "rgba(220,38,38,0.45)";              // red
}
