export default function RightPanel({ ssids }) {
  if (!ssids) return null;

  return (
    <div className="bg-zinc-900 rounded-xl p-4">
      <h3 className="text-sm text-zinc-400 mb-3">Top SSIDs</h3>
      <ul className="space-y-2">
        {ssids.map((s, i) => (
          <li
            key={i}
            className="flex justify-between text-sm text-zinc-200"
          >
            <span className="truncate">{s.ssid}</span>
            <span className="text-zinc-400">{s.ap_count} APs</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
