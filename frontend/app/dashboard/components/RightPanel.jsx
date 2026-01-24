export default function RightPanel({ alerts = [] }) {
  return (
    <div className="h-full p-4 space-y-3 overflow-y-auto">
      <div className="text-sm font-semibold">Alerts</div>

      {alerts.slice().reverse().map((a, i) => (
        <div
          key={i}
          className={`p-2 rounded border text-sm ${
            a.payload.severity === "high"
              ? "bg-red-950 border-red-700"
              : "bg-zinc-900 border-zinc-800"
          }`}
        >
          <div className="font-medium">{a.payload.alert_type}</div>
          <div className="text-xs text-zinc-400">
            {Math.round(a.payload.confidence * 100)}% confidence
          </div>
        </div>
      ))}
    </div>
  );
}