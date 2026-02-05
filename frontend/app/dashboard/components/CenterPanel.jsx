export default function CenterPanel({ heatmap }) {
  if (!heatmap) return null;

  return (
    <div className="bg-zinc-900 rounded-xl p-4">
      <h3 className="text-sm text-zinc-400 mb-4">
        Channel Activity Heatmap
      </h3>

      <div className="space-y-3">
        {Object.entries(heatmap.channels).map(([ch, count]) => (
          <div key={ch} className="flex items-center gap-3">
            <span className="w-12 text-sm text-zinc-400">Ch {ch}</span>
            <div className="flex-1 bg-zinc-800 h-3 rounded overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-teal-400 to-yellow-400"
                style={{ width: `${Math.min(count * 15, 100)}%` }}
              />
            </div>
            <span className="text-xs text-zinc-400">{count} APs</span>
          </div>
        ))}
      </div>
    </div>
  );
}
