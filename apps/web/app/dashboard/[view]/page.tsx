import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { DashboardShell } from "@/components/DashboardShell";
import { dashboards, dashboardViews, isDashboardView } from "@/lib/release-candidate";

export const metadata: Metadata = { title: "Operations Dashboard", robots: { index: false, follow: false } };

export function generateStaticParams() {
  return dashboardViews.map((view) => ({ view }));
}

export default async function DashboardPage({ params }: { params: Promise<{ view: string }> }) {
  const { view } = await params;
  if (!isDashboardView(view)) notFound();
  const dashboard = dashboards[view];
  return (
    <DashboardShell active={view}>
      <main id="main-content" className="command-content">
        <header className="dashboard-hero"><p className="eyebrow">{dashboard.eyebrow}</p><h1>{dashboard.title}</h1><p>{dashboard.description}</p></header>
        <section className="metric-grid" aria-label={`${dashboard.title} metrics`}>
          {dashboard.cards.map((card) => <article className="metric-card" key={card.label}><span className={`status-label ${card.tone ?? "staged"}`}>{card.label}</span><strong>{card.value}</strong><p>{card.note}</p></article>)}
        </section>
        <section className="approval-panel"><div><p className="eyebrow">Next responsible moves</p><h2>Approval queue</h2></div><ol>{dashboard.queue.map((item) => <li key={item}>{item}</li>)}</ol></section>
        <p className="data-note">Release-candidate data only. This dashboard does not claim production activity, revenue, audience, or sends that have not occurred.</p>
      </main>
    </DashboardShell>
  );
}
