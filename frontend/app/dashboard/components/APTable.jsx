export default function APTable({ aps }) {
  if (!aps || aps.length === 0) {
    return (
      <div className="bg-zinc-900 rounded-xl p-4 min-h-48 text-center text-zinc-500">
        No access points detected
      </div>
    );
  }

  return (
    <div className="bg-zinc-900 rounded-xl p-4 max-h-72 overflow-y-auto">
      <h3 className="text-sm text-zinc-400 mb-3">Live Access Points</h3>

      <table className="w-full text-sm">
        <thead className="text-zinc-500 text-xs uppercase">
          <tr>
            <th className="text-left">SSID</th>
            <th className="text-left">Channel</th>
            <th className="text-left">Signal</th>
          </tr>
        </thead>

        <tbody className="text-zinc-200">
          {aps.map((ap, i) => (
            <tr key={i} className="border-t border-zinc-800">
              <td>{ap.ssid || "Hidden"}</td>
              <td>{ap.channel}</td>
              <td>{ap.signal} dBm</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
