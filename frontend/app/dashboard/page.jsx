"use client";

import Topbar from "./components/Topbar";
import LeftPanel from "./components/LeftPanel";
import CenterPanel from "./components/CenterPanel";
import RightPanel from "./components/RightPanel";
import BottomPanel from "./components/BottomPanel";
import { useWS } from "../hooks/useWS"; //to connect with the backend 

export default function DashboardPage() {
  const { connected, telemetry, alerts } = useWS("ws://localhost:8000/ws"); //getting the data from data-layer via useWs hook
  const latestTelemetry = telemetry
    .filter(m => m.type === "telemetry")
    .slice(-1)[0];

  return (
    <div className="flex flex-col h-full">

      <Topbar connected={connected} />

      <div className="flex flex-1 overflow-hidden">

        <div className="w-[30%] border-r border-zinc-800">
          <LeftPanel telemetry={telemetry} />
        </div>

        <CenterPanel
          channels={latestTelemetry?.payload?.heatmap?.channels ?? {}}
        />


        <div className="w-[15%]">
          <RightPanel alerts={alerts} />
        </div>

      </div>

      <BottomPanel />
    </div>
  );
}
