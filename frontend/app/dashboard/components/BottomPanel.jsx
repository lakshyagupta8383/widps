export default function BottomPanel({ telemetry }) {
  const latest = telemetry.at(-1)?.payload?.summary;
  if (!latest) return null;

  return (
    <div className="h-14 px-4 flex items-center border-t border-zinc-800 bg-zinc-950 text-sm text-zinc-400">
      RF environment stable · {latest.ap_count} APs · {latest.client_count} clients
    </div>
  );
}
