"use client";

import Topbar from "./components/Topbar";
import LeftPanel from "./components/LeftPanel";
import CenterPanel from "./components/CenterPanel";
import RightPanel from "./components/RightPanel";
import BottomPanel from "./components/BottomPanel";
import { useWS } from "./hooks/useWS";

export default function DashboardPage() {
  const { connected, telemetry, alerts } = useWS("ws://localhost:8000/ws");

  const channels =
    telemetry.at(-1)?.payload?.heatmap?.channels ?? {};

  return (
    <div className="flex flex-col h-screen bg-black">
      <Topbar connected={connected} />

      <div className="flex flex-1">
        <div className="w-[30%] border-r border-zinc-800">
          <LeftPanel telemetry={telemetry} />
        </div>

        <div className="w-[55%] border-r border-zinc-800">
          <CenterPanel channels={channels} />
        </div>

        <div className="w-[15%]">
          <RightPanel alerts={alerts} />
        </div>
      </div>

      <BottomPanel telemetry={telemetry} />
    </div>
  );
}
