export default function LeftPanel({ telemetry = [] }) {
  const latest = telemetry.at(-1)?.payload?.summary;

  return (
    <div className="h-full p-4 space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <Stat label="APs" value={latest?.ap_count ?? "-"} />
        <Stat label="Clients" value={latest?.client_count ?? "-"} />
        <Stat label="Uptime" value={latest ? `${Math.floor(latest.uptime_sec / 60)}m` : "-"} />
        <Stat label="Status" value={latest ? "Running" : "Waiting"} />
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="bg-zinc-900 rounded p-3">
      <div className="text-xs text-zinc-400">{label}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}