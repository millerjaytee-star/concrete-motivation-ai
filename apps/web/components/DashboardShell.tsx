import Link from "next/link";
import type { Route } from "next";
import type { DashboardView } from "@/lib/release-candidate";
import { dashboardViews } from "@/lib/release-candidate";

export function DashboardShell({ active, children }: { active?: DashboardView; children: React.ReactNode }) {
  return (
    <div className="command-layout">
      <aside className="command-nav">
        <Link className="brand" href="/" aria-label="Concrete Motivation home">
          <span className="brand-mark" aria-hidden="true">CM</span>
          <span>Command Center</span>
        </Link>
        <nav aria-label="Command center navigation">
          <Link href="/command-center">Overview</Link>
          {dashboardViews.map((view) => (
            <Link aria-current={active === view ? "page" : undefined} key={view} href={`/dashboard/${view}` as Route}>
              {view}
            </Link>
          ))}
        </nav>
        <div className="release-lock"><span /> Release candidate<br /><small>External actions locked</small></div>
      </aside>
      <div className="command-main">{children}</div>
    </div>
  );
}
