import type { Metadata } from "next";
import type { Route } from "next";
import Link from "next/link";
import { DashboardShell } from "@/components/DashboardShell";
import { BotConsole } from "@/components/BotConsole";
import { botCatalog, dashboards, dashboardViews, integrations } from "@/lib/release-candidate";

export const metadata: Metadata = {
  title: "Release Candidate Command Center",
  description: "Concrete Motivation owner command center for release readiness, bot orchestration, and approval-gated integrations.",
  robots: { index: false, follow: false },
};

export default function CommandCenterPage() {
  const ready = integrations.filter((item) => item.readiness === "ready").length;
  return (
    <DashboardShell>
      <main id="main-content" className="command-content">
        <header className="command-hero">
          <div><p className="eyebrow">Concrete Empire OS</p><h1>Build. Measure. Approve.</h1><p>The full release-candidate control plane. Every external action remains locked until the owner approves the exact target and payload.</p></div>
          <div className="readiness-ring" aria-label={`${ready} of ${integrations.length} integrations ready`}><strong>{ready}/{integrations.length}</strong><span>integrations ready</span></div>
        </header>

        <section className="dashboard-grid" aria-label="Dashboard directory">
          {dashboardViews.map((view) => (
            <Link className="dashboard-tile" href={`/dashboard/${view}` as Route} key={view}>
              <span>{String(dashboardViews.indexOf(view) + 1).padStart(2, "0")}</span>
              <h2>{dashboards[view].title}</h2>
              <p>{dashboards[view].description}</p>
            </Link>
          ))}
        </section>

        <BotConsole />

        <section className="command-section">
          <div className="section-heading"><p className="eyebrow">Bot orchestration</p><h2>15 specialists. One governed system.</h2></div>
          <div className="bot-grid">
            {botCatalog.map((bot) => <article className="bot-card" key={bot.slug}><span>{bot.group}</span><h3>{bot.name}</h3><p>{bot.purpose}</p><small>{bot.outputs.join(" · ")}</small></article>)}
          </div>
        </section>

        <section className="command-section">
          <div className="section-heading"><p className="eyebrow">Integration control</p><h2>Connected without losing control.</h2></div>
          <div className="integration-table" role="table" aria-label="Integration readiness">
            {integrations.map((item) => <div role="row" className="integration-row" key={item.key}><div role="cell"><span className={`status-dot ${item.readiness}`} />{item.name}</div><div role="cell">{item.mode}</div><div role="cell">{item.detail}</div><div role="cell">Approval: {item.approvalRequired}</div></div>)}
          </div>
        </section>
      </main>
    </DashboardShell>
  );
}
