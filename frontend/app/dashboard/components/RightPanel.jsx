export default function RightPanel({ alerts = [] }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="p-4 text-zinc-500">
        No active alerts
      </div>
    );
  }

  return (
    <div className="p-4 space-y-2">
      {alerts.slice(-5).map((a, i) => (
        <div key={i} className="text-sm text-red-400">
          {a.payload?.alert_type ?? "Unknown alert"}
        </div>
      ))}
    </div>
  );
}

