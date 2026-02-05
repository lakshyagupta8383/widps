export default function LeftPanel({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-1 gap-4">
      <div className="bg-zinc-900 rounded-xl p-4">
        <h3 className="text-sm text-zinc-400">Access Points</h3>
        <p className="text-3xl font-semibold">{summary.ap_count}</p>
      </div>

      <div className="bg-zinc-900 rounded-xl p-4">
        <h3 className="text-sm text-zinc-400">Active Clients</h3>
        <p className="text-3xl font-semibold">{summary.client_count}</p>
      </div>

      <div className="bg-zinc-900 rounded-xl p-4">
        <h3 className="text-sm text-zinc-400 mb-2">AP Stability</h3>
        <p className="text-lg">
          <span className="text-green-400">{summary.stable_aps}</span>{" "}
          <span className="text-zinc-500">|</span>{" "}
          <span className="text-orange-400">
            {summary.transient_aps}
          </span>
        </p>
        <p className="text-xs text-zinc-500">Stable | Transient</p>
      </div>
    </div>
  );
}
