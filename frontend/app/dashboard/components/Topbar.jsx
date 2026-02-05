export default function Topbar({ connected, uptime }) {
  return (
    <div className="flex justify-between items-center px-6 py-4 bg-zinc-900 rounded-xl">
      <h1 className="text-xl font-semibold tracking-wide">WIDPS</h1>
      <span className="text-sm text-zinc-400">
        {connected ? "🟢 Connected" : "🔴 Disconnected"} · Uptime {uptime}s
      </span>
    </div>
  );
}
