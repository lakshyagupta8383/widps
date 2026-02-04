import { useEffect, useRef } from "react";

const WINDOW = 30;

export function useBaseline(channels) {
  const history = useRef([]);
  const baseline = useRef({});

  useEffect(() => {
    if (!channels || Object.keys(channels).length === 0) return;

    history.current.push(channels);
    if (history.current.length > WINDOW) history.current.shift();

    const sum = {};
    history.current.forEach((frame) => {
      Object.entries(frame).forEach(([ch, v]) => {
        sum[ch] = (sum[ch] || 0) + v;
      });
    });

    const avg = {};
    Object.entries(sum).forEach(([ch, v]) => {
      avg[ch] = v / history.current.length;
    });

    baseline.current = avg;
  }, [channels]);

  return baseline.current;
}
