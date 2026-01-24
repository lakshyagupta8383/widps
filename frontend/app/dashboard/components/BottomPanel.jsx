export default function BottomPanel({ telemetry = [], alerts = [] }) {
  // Merge telemetry + alerts into a single activity stream
  const activity = [
    ...telemetry.map(t => ({
      type: "telemetry",
      timestamp: t.payload?.timestamp,
      summary: t.payload?.summary
    })),
    ...alerts.map(a => ({
      type: "alert",
      timestamp: a.payload?.timestamp,
      alert: a.payload
    }))
  ]
    .filter(a => a.timestamp)
    .sort((a, b) => b.timestamp - a.timestamp)
    .slice(0, 20); // last 20 events

  return (
    <div className="h-48 border-t border-zinc-800 bg-zinc-950">
      <div className="h-full p-4 overflow-y-auto">
        <div className="text-sm font-semibold text-zinc-300 mb-2">
          Activity
        </div>

        <div className="space-y-2 text-xs">
          {activity.map((a, i) => (
            <ActivityRow key={i} event={a} />
          ))}
        </div>
      </div>
    </div>
  );
}

function ActivityRow({ event }) {
  if (event.type === "alert") {
    return (
      <div className="p-2 rounded bg-red-950 border border-red-800">
        <div className="font-medium text-red-300">
          ALERT · {event.alert.alert_type}
        </div>
        <div className="text-red-400">
          {event.alert.severity} · {Math.round(event.alert.confidence * 100)}%
        </div>
      </div>
    );
  }

  return (
    <div className="p-2 rounded bg-zinc-900 border border-zinc-800">
      <div className="text-zinc-300 font-medium">
        Telemetry update
      </div>
      <div className="text-zinc-400">
        APs: {event.summary?.ap_count ?? "-"} ·
        Clients: {event.summary?.client_count ?? "-"}
      </div>
    </div>
  );
}
