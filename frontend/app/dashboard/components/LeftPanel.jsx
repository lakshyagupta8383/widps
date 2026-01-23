export default function LeftPanel() {
  return (
    <div className="h-full p-4 space-y-4 overflow-y-auto">
      <div className="h-24 bg-zinc-900 rounded p-3 text-sm text-zinc-400">
        Stats
      </div>

      <div className="h-48 bg-zinc-900 rounded p-3 text-sm text-zinc-400">
        Time-series
      </div>

      <div className="h-24 bg-zinc-900 rounded p-3 text-sm text-zinc-400">
        Saved Views
      </div>
    </div>
  );
}

