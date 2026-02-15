export default function BottomPanel({ alerts }) {
  const baseClasses =
    "bg-zinc-900 rounded-xl p-4 min-h-48 flex flex-col";

  if (!alerts || alerts.length === 0) {
    return (
      <div className={`${baseClasses} justify-center items-center text-zinc-500 text-sm`}>
        No active alerts
      </div>
    );
  }

  return (
    <div className={baseClasses}>
      <h3 className="text-sm text-zinc-400 mb-3">Recent Alerts</h3>

      <ul className="space-y-2 max-h-44 overflow-y-auto flex-1">
        {alerts
          .slice()
          .reverse()
          .map((alert, idx) => {
            const {
              alert_type,
              severity,
              confidence,
              timestamp,
            } = alert.payload;

            const time = new Date(timestamp * 1000).toLocaleTimeString();

            const severityColor =
              severity === "HIGH"
                ? "text-red-400"
                : severity === "MED"
                ? "text-orange-400"
                : "text-yellow-400";

            return (
              <li
                key={idx}
                className="flex justify-between items-center text-sm"
              >
                <div className="flex items-center gap-3">
                  <span className={`font-semibold ${severityColor}`}>
                    {severity}
                  </span>

                  <span className="text-zinc-200">
                    {alert_type.replaceAll("_", " ")}
                  </span>

                  {confidence !== undefined && (
                    <span className="text-zinc-500 text-xs">
                      {(confidence * 100).toFixed(0)}%
                    </span>
                  )}
                </div>

                <span className="text-zinc-500 text-xs">{time}</span>
              </li>
            );
          })}
      </ul>
    </div>
  );
}
