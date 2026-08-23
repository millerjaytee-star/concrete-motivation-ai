import type { Metadata } from "next";
import Link from "next/link";
import { SiteShell } from "@/components/SiteShell";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Concrete Nation Gatherings | Concrete Motivation",
  description:
    "Members-only Concrete Nation Gatherings turn online community into real participation through accountability circles, service, learning, networking, wellness, and live conversations.",
  alternates: { canonical: "/gatherings" },
  openGraph: {
    title: "Concrete Nation Gatherings | Concrete Motivation",
    description:
      "Paid Concrete Nation members meet, serve, learn, and build together — with RSVP accountability, verified attendance, and Concrete Passport proof.",
    url: "/gatherings",
    type: "website"
  }
};

const appGatheringsUrl = `${siteConfig.links.app.replace(/\/$/, "")}/app/gatherings`;

export default function GatheringsPage() {
  return (
    <SiteShell>
      <main id="main-content">
        <section className="page-hero">
          <div className="page-hero-inner">
            <p className="eyebrow">Concrete Nation · Members Only</p>
            <h1>Do more than join. Show up.</h1>
            <p className="page-lead">
              Concrete Nation Gatherings are private, action-based experiences for active paid members — built to turn connection into participation, proof, service, and stronger relationships.
            </p>
            <div className="button-row">
              <a className="button button-primary" href={appGatheringsUrl}>Open Gatherings in the app</a>
              <Link className="button button-secondary" href="/memberships">See memberships</Link>
            </div>
          </div>
        </section>

        <section className="section page-intro">
          <p>
            This is not a popularity feed and it is not another free event board. Members reserve a spot, receive the private details after they commit, check in when they arrive, and build a participation record inside their Concrete Passport.
          </p>
        </section>

        <section className="section content-grid" aria-label="Concrete Nation Gathering details">
          <article className="content-card">
            <span className="card-number">01</span>
            <h2>Built for people who participate</h2>
            <p>Gatherings are a paid-member benefit. Public pages can explain what is happening, but RSVP access, private locations, virtual links, and participation history stay inside the authenticated member experience.</p>
          </article>

          <article className="content-card">
            <span className="card-number">02</span>
            <h2>Meet online or in person</h2>
            <p>Gatherings can be virtual, in person, or hybrid: accountability circles, service projects, financial-literacy discussions, networking happy hours, youth mentorship, walking or workout groups, book discussions, business-owner meetups, volunteer opportunities, and Concrete Conversations watch sessions.</p>
          </article>

          <article className="content-card">
            <span className="card-number">03</span>
            <h2>RSVP means commitment</h2>
            <p>Members reserve their spot, can cancel when plans change, and check in when they attend. Attendance becomes durable proof in the Concrete Passport so reliability is based on action, not likes or followers.</p>
          </article>

          <article className="content-card">
            <span className="card-number">04</span>
            <h2>Private details stay private</h2>
            <p>Exact locations, private access instructions, and virtual meeting links are protected behind membership and RSVP status. The public site never exposes sensitive event details.</p>
          </article>

          <article className="content-card">
            <span className="card-number">05</span>
            <h2>Leadership is earned</h2>
            <p>Members can move toward hosting through an approval path. Host permissions, check-in authority, reporting, moderation, and safety controls keep Gatherings useful without turning the Nation into an unmoderated event marketplace.</p>
          </article>

          <article className="content-card">
            <span className="card-number">06</span>
            <h2>The first pours</h2>
            <p>Seed experiences include Concrete Orientation, Foundation Circle, Money & Concrete, DMV Concrete Walk, Service Pour, Concrete Conversations Live, and Founding Pour. Real dates and venues are published only when confirmed.</p>
          </article>
        </section>

        <section className="section closing-cta">
          <div>
            <p className="eyebrow">Your next move</p>
            <h2>Get in the room. Lay the Brick. Build the Nation.</h2>
          </div>
          <a className="button button-primary" href={appGatheringsUrl}>Open Gatherings</a>
        </section>
      </main>
    </SiteShell>
  );
}
