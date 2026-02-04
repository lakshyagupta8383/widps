import { heatColor } from "../utils/colors";

export default function CenterPanel({ channels }) {
  return (
    <div className="p-4 h-full">
      <div className="grid grid-cols-13 gap-2 h-full">
        {Array.from({ length: 13 }, (_, i) => {
          const ch = i + 1;
          const v = channels[ch] || 0;

          return (
            <div
              key={ch}
              className="rounded flex items-end justify-center text-xs text-zinc-200"
              style={{ background: heatColor(v) }}
            >
              ch {ch}
            </div>
          );
        })}
      </div>
    </div>
  );
}
