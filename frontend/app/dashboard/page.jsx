import Topbar from "./components/Topbar";
import LeftPanel from "./components/LeftPanel";
import CenterPanel from "./components/CenterPanel";
import RightPanel from "./components/RightPanel";
import BottomPanel from "./components/BottomPanel";

export default function DashboardPage() {
  return (
    <div className="flex flex-col h-full">
      
      {/* Topbar */}
      <Topbar />

      {/* Main */}
      <div className="flex flex-1 overflow-hidden">
        <div className="w-[30%] border-r border-zinc-800">
          <LeftPanel />
        </div>

        <div className="w-[55%] border-r border-zinc-800">
          <CenterPanel />
        </div>

        <div className="w-[15%]">
          <RightPanel />
        </div>
      </div>

      {/* Bottom */}
      <BottomPanel />
    </div>
  );
}
