import { siteConfig } from "@/lib/site-config";

const ecosystem = [
  {
    title: "Concrete Motivation",
    label: "The inspiration engine",
    copy: "Practical messages that turn pressure into disciplined action."
  },
  {
    title: "Concrete Conversations",
    label: "The trust engine",
    copy: "Real people, real stories, real lessons, and transferable wisdom."
  },
  {
    title: "Concrete Nation",
    label: "The action engine",
    copy: "Accountability, mentorship, resources, referrals, and opportunity."
  }
];

export default function HomePage() {
  return (
    <main id="main-content">
      <header className="site-header">
        <a className="brand" href="#top" aria-label="Concrete Motivation home">
          <span className="brand-mark">CM</span>
          <span>Concrete Motivation</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#story">Story</a>
          <a href="#method">Method</a>
          <a href="#conversations">Conversations</a>
          <a href="#nation">Concrete Nation</a>
          <a className="nav-cta" href="#join">Join</a>
        </nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-noise" aria-hidden="true" />
        <div className="hero-copy">
          <p className="eyebrow">Mind. Body. Business. Legacy.</p>
          <h1><span>Concrete</span> Motivation</h1>
          <p className="hero-phrase">{siteConfig.phrase}</p>
          <p className="hero-description">{siteConfig.description}</p>
          <div className="button-row">
            <a className="button button-primary" href="#nation">Join Concrete Nation</a>
            <a className="button button-secondary" href="#story">Watch the Story</a>
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

      <section className="section" id="story">
        <div className="section-heading">
          <p className="eyebrow">One movement. Three engines.</p>
          <h2>Attention becomes trust. Trust becomes action.</h2>
        </div>
        <div className="ecosystem-grid">
          {ecosystem.map((item, index) => (
            <article className="feature-card" key={item.title}>
              <span className="card-number">0{index + 1}</span>
              <p className="eyebrow">{item.label}</p>
              <h3>{item.title}</h3>
              <p>{item.copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section method-section" id="method">
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

      <section className="section split-section" id="conversations">
        <div>
          <p className="eyebrow">Concrete Conversations</p>
          <h2>Real stories. Real lessons. Real impact.</h2>
          <p>Honest conversations about leadership, family, business, sports, faith, rebuilding, and what success actually costs.</p>
          <a className="text-link" href={siteConfig.links.youtube}>Explore the video and podcast hub →</a>
        </div>
        <div className="media-frame" aria-label="Featured content placeholder">
          <span className="play-button" aria-hidden="true">▶</span>
          <p>Channel trailer and latest episode</p>
        </div>
      </section>

      <section className="section nation-section" id="nation">
        <p className="eyebrow">Concrete Nation</p>
        <h2>{siteConfig.promise}</h2>
        <p className="lead">A community designed to connect people with accountability, mentors, practical resources, referrals, collaborations, and opportunities to become successful together.</p>
        <div className="nation-grid">
          {[
            "Accountability circles",
            "Mentorship and skill exchange",
            "Career and business referrals",
            "Member challenges and progress",
            "Workshops and live conversations",
            "Opportunities to contribute and lead"
          ].map((item) => <div className="nation-item" key={item}>{item}</div>)}
        </div>
      </section>

      <section className="section join-section" id="join">
        <div>
          <p className="eyebrow">Join the movement</p>
          <h2>Build your next chapter with people who expect you to move.</h2>
        </div>
        <div className="button-row">
          <a className="button button-primary" href={siteConfig.links.app}>Join the app waitlist</a>
          <a className="button button-secondary" href={siteConfig.links.booking}>Book Jaytee</a>
        </div>
      </section>

      <footer>
        <div><strong>Concrete Motivation</strong><p>{siteConfig.phrase}</p></div>
        <div className="footer-links">
          <a href={siteConfig.links.youtube}>YouTube</a>
          <a href={siteConfig.links.instagram}>Instagram</a>
          <a href={siteConfig.links.tiktok}>TikTok</a>
          <a href={siteConfig.links.facebook}>Facebook</a>
        </div>
        <p>© 2026 Concrete Motivation. Built for real change.</p>
      </footer>
    </main>
  );
}
