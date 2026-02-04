export function heatColor(v) {
  if (v === 0) return "rgba(39,39,42,0.6)";
  if (v < 3) return "rgba(37,99,235,0.4)";
  if (v < 6) return "rgba(234,179,8,0.5)";
  return "rgba(220,38,38,0.6)";
}
