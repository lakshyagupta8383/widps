export default function RightPanel({ messages = [] }) {
  const alerts = messages.filter(m => m.type === "alert");

  return (
    <div className="h-full p-4 space-y-4 overflow-y-auto">
      <div className="text-sm font-semibold text-zinc-300">
        Alerts
      </div>

      <div className="space-y-2">
        {alerts.slice(-10).reverse().map((a, i) => (
          <div
            key={i}
            className="p-2 rounded bg-zinc-900 border border-zinc-800"
          >
            <div className="text-sm font-medium">
              {a.payload.alert_type}
            </div>
            <div className="text-xs text-zinc-400">
              {a.payload.severity} · {Math.round(a.payload.confidence * 100)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
