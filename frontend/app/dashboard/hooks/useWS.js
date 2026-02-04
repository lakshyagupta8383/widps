"use client";
import { useEffect, useState } from "react";

export function useWS(url) {
  const [connected, setConnected] = useState(false);
  const [telemetry, setTelemetry] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      if (msg.type === "telemetry") {
        setTelemetry((t) => [...t.slice(-100), msg]);
      }

      if (msg.type === "alert") {
        setAlerts((a) => [...a.slice(-20), msg]);
      }
    };

    return () => ws.close();
  }, [url]);

  return { connected, telemetry, alerts };
}
