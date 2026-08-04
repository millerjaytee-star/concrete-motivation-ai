import Link from "next/link";
import { SiteShell } from "@/components/SiteShell";

export default function NotFound() {
  return (
    <SiteShell>
      <main id="main-content">
        <section className="page-hero">
          <div className="page-hero-inner">
            <p className="eyebrow">404 — Route not found</p>
            <h1>This path is not built yet.</h1>
            <p className="page-lead">Return to the movement and choose a clear next step.</p>
            <div className="button-row">
              <Link className="button button-primary" href="/">Return home</Link>
              <Link className="button button-secondary" href="/join">Join / Contact</Link>
            </div>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
