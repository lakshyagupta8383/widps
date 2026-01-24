"use client";
import { useEffect, useRef, useState } from "react";

export function useWS(url) {
  const wsRef = useRef(null);//holds the webSocket instance 
  const [connected, setConnected] = useState(false); //maintains the connected state
  const [telemetry, setTelemetry] = useState([]); //holds telemetry data(high-frequency,live data)
  const [alerts, setAlerts] = useState([]);//holds alert(low-frequency)

  useEffect(() => {
    wsRef.current = new WebSocket(url);  //mounts the mutable url link

    wsRef.current.onopen = () => setConnected(true); //WebSocket handshake successful
    wsRef.current.onclose = () => setConnected(false); //WebSocket disconnected

    wsRef.current.onmessage = (event) => { // triggered when backend/data-layer sends data
      try { 
        const msg = JSON.parse(event.data); //parsing json

        // now it checks the type of data 
        if (msg.type === "telemetry") {
          setTelemetry(prev => [...prev.slice(-100), msg]); //keeps only last 100 entries
        }

        if (msg.type === "alert") {
          setAlerts(prev => [...prev.slice(-50), msg]);//keeps only last 50 entries
        }
      } catch (e) {
        console.error("WS parse error", e);
      }
    };

    return () => wsRef.current?.close();
  }, [url]);

  return { connected, telemetry, alerts };
}