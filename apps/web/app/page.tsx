import Link from "next/link";
import type { Route } from "next";
import { SiteShell } from "@/components/SiteShell";
import { siteConfig } from "@/lib/site-config";

const ecosystem = [
  { title: "Concrete Motivation", label: "The inspiration engine", copy: "Practical messages that turn pressure into disciplined action.", href: "/our-story" },
  { title: "Concrete Conversations", label: "The trust engine", copy: "Real people, real stories, real lessons, and transferable wisdom.", href: "/concrete-conversations" },
  { title: "Concrete Nation", label: "The action engine", copy: "Accountability, mentorship, resources, referrals, and opportunity.", href: "/concrete-nation" }
];

export default function HomePage() {
  return (
    <SiteShell>
      <main id="main-content">
        <section className="hero" id="top">
          <div className="hero-copy">
            <p className="eyebrow">Mind. Body. Business. Legacy.</p>
            <h1><span>Concrete</span> Motivation</h1>
            <p className="hero-phrase">{siteConfig.phrase}</p>
            <p className="hero-description">{siteConfig.description}</p>
            <div className="button-row">
              <Link className="button button-primary" href="/concrete-nation">Join Concrete Nation</Link>
              <Link className="button button-secondary" href="/our-story">Read the Story</Link>
            </div>
            <ul className="pillar-row" aria-label="Concrete Motivation pillars">
              {siteConfig.pillars.map((pillar) => <li key={pillar}>{pillar}</li>)}
            </ul>
          </div>
          <aside className="hero-card">
            <p className="eyebrow">Founder message</p>
            <blockquote>“Pressure reveals the foundation. Purpose decides what gets built next.”</blockquote>
            <p>Jaytee Miller built this movement for people carrying real responsibility who are ready to stop building alone.</p>
          </aside>
        </section>

        <section className="section">
          <div className="section-heading">
            <p className="eyebrow">One movement. Three engines.</p>
            <h2>Attention becomes trust. Trust becomes action.</h2>
          </div>
          <div className="ecosystem-grid">
            {ecosystem.map((item, index) => (
              <Link className="feature-card" key={item.title} href={item.href as Route}>
                <span className="card-number">0{index + 1}</span>
                <p className="eyebrow">{item.label}</p>
                <h3>{item.title}</h3>
                <p>{item.copy}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="section method-section">
          <div className="section-heading">
            <p className="eyebrow">The Concrete Method</p>
            <h2>Eight moves from pressure to legacy.</h2>
          </div>
          <div className="method-grid">
            {siteConfig.method.map(([title, copy], index) => (
              <article className="method-card" key={title}>
                <span>{index + 1}</span>
                <h3>{title}</h3>
                <p>{copy}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section split-section">
          <div>
            <p className="eyebrow">Concrete Conversations</p>
            <h2>Real stories. Real lessons. Real impact.</h2>
            <p>Honest conversations about leadership, family, business, sports, faith, rebuilding, and what success actually costs.</p>
            <Link className="text-link" href="/concrete-conversations">Explore the media platform →</Link>
          </div>
          <div className="media-frame" aria-label="Featured content area">
            <span className="play-button" aria-hidden="true">▶</span>
            <p>Channel trailer and latest episode</p>
          </div>
        </section>

        <section className="section nation-section">
          <p className="eyebrow">Concrete Nation</p>
          <h2>{siteConfig.promise}</h2>
          <p className="lead">A community designed to connect people with accountability, mentors, practical resources, referrals, collaborations, and opportunities to become successful together.</p>
          <div className="nation-grid">
            {["Accountability circles", "Mentorship and skill exchange", "Career and business referrals", "Member challenges and progress", "Workshops and live conversations", "Opportunities to contribute and lead"].map((item) => <div className="nation-item" key={item}>{item}</div>)}
          </div>
        </section>

        <section className="section join-section">
          <div>
            <p className="eyebrow">Join the movement</p>
            <h2>Build your next chapter with people who expect you to move.</h2>
          </div>
          <div className="button-row">
            <Link className="button button-primary" href="/join">Start here</Link>
            <Link className="button button-secondary" href="/speaking">Book Jaytee</Link>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
