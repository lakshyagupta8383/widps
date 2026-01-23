export default function Topbar({ connected }) {
  return (
    <div className="h-14 flex items-center justify-between px-4 border-b border-zinc-800 bg-zinc-950">
      <div className="font-semibold tracking-wide">
        WIDPS
      </div>

      <div className="flex items-center gap-4 text-sm text-zinc-400">
        <span className={connected ? "text-green-400" : "text-red-400"}>
          {connected ? "● Connected" : "● Disconnected"}
        </span>
        <span>Live</span>
        <span>Filters</span>
        <span>User</span>
      </div>
    </div>
  );
}

