export default function LeftPanel({ telemetry }) {
  const latest = telemetry.at(-1)?.payload?.summary;
  if (!latest) return null;

  return (
    <div className="p-4 space-y-3 text-sm text-zinc-300">
      <div>APs: <b>{latest.ap_count}</b></div>
      <div>Clients: <b>{latest.client_count}</b></div>
      <div>Uptime: {Math.floor(latest.uptime_sec / 60)} min</div>
    </div>
  );
}
