export default function Topbar({ connected }) {
  return (
    <div className="h-12 px-4 flex items-center justify-between border-b border-zinc-800 bg-zinc-950">
      <span className="font-semibold text-zinc-200">WIDPS</span>
      <span className={connected ? "text-emerald-400" : "text-red-400"}>
        {connected ? "Connected" : "Disconnected"}
      </span>
    </div>
  );
}
