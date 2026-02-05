"use client";

import Topbar from "./components/Topbar";
import LeftPanel from "./components/LeftPanel";
import CenterPanel from "./components/CenterPanel";
import RightPanel from "./components/RightPanel";
import BottomPanel from "./components/BottomPanel";
import { useWS } from "./hooks/useWS";

export default function DashboardPage() {
  const { connected, telemetry, alerts } = useWS("ws://localhost:8000/ws");

  const lastTelemetry =
    Array.isArray(telemetry) && telemetry.length > 0
      ? telemetry[telemetry.length - 1]
      : null;

  const summary = lastTelemetry?.payload?.summary;
  const heatmap = lastTelemetry?.payload?.heatmap;
  const topSSIDs = lastTelemetry?.payload?.top_ssids;

  return (
    <div className="flex flex-col h-screen bg-black text-white">
      <Topbar
        connected={connected}
        uptime={summary?.uptime_sec}
      />

      <div className="flex flex-1">
        <div className="w-[30%] border-r border-zinc-800 p-4">
          <LeftPanel summary={summary} />
        </div>

        <div className="w-[55%] border-r border-zinc-800 p-4">
          <CenterPanel heatmap={heatmap} />
        </div>

        <div className="w-[15%] p-4">
          <RightPanel ssids={topSSIDs} />
        </div>
      </div>

      <div className="p-4">
        <BottomPanel alerts={alerts} />
      </div>
    </div>
  );
}
