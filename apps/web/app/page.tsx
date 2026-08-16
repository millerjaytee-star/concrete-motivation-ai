import Image from "next/image";
import Link from "next/link";
import { SiteShell } from "@/components/SiteShell";
import { imageFor } from "@/lib/photography";
import { siteConfig } from "@/lib/site-config";

const ecosystem = [
  { title: "Concrete Motivation", label: "The inspiration engine", copy: "Practical messages that turn pressure into disciplined action.", href: "/our-story" },
  { title: "Concrete Conversations", label: "The trust engine", copy: "Real people, real stories, real lessons, and transferable wisdom.", href: "/concrete-conversations" },
  { title: "Concrete Nation", label: "The action engine", copy: "Accountability, mentorship, resources, referrals, and opportunity.", href: "/concrete-nation" }
];

const flagship = [
  { eyebrow: "Free first step", title: "Daily Brick", copy: "Turn today's pressure into one specific, provable action.", href: "/daily-brick", cta: "Lay today's Brick" },
  { eyebrow: "Free 7-day experience", title: "Foundation Challenge", copy: "Seven days of kept promises, honest inspection, and recovery after misses.", href: "/foundation-challenge", cta: "Start the challenge" },
  { eyebrow: "Flagship program · $29", title: "30-Day Concrete Reset", copy: "Foundation, discipline, pressure and recovery, purpose and leadership — followed by a 90-day next Blueprint.", href: "/concrete-30-day-reset", cta: "Explore the Reset" },
  { eyebrow: "Inaugural cohort", title: "The Founding 100", copy: "100 Builders. One Foundation. One Brick Every Day. Founding status is earned through action, not bought.", href: "/founding-100", cta: "See the Founding 100" }
];

export default function HomePage() {
  return (
    <SiteShell>
      <main id="main-content">
        <section className="hero hero-with-photo" id="top">
          <div className="hero-copy">
            <p className="eyebrow">Mind. Body. Business. Legacy.</p>
            <h1><span>Concrete</span> Motivation</h1>
            <p className="hero-phrase">Built Under Pressure. Proven Through Purpose.</p>
            <p className="hero-description">Pressure does not have to destroy you. With the right foundation, it can reveal discipline, purpose, leadership, and the next thing you are called to build.</p>
            <div className="button-row">
              <Link className="button button-primary" href="/start-here">Start Building</Link>
              <Link className="button button-secondary" href="/our-story">Watch the Story</Link>
              <Link className="text-link" href="/speaking">Book Jaytee →</Link>
            </div>
            <ul className="pillar-row" aria-label="Concrete Motivation pillars">
              {siteConfig.pillars.map((pillar) => <li key={pillar}>{pillar}</li>)}
            </ul>
          </div>
          <aside className="hero-photo-card">
            <Image src={imageFor("hero")} alt="Jaytee Miller, founder of Concrete Motivation" width={900} height={900} priority />
            <div className="photo-caption">
              <p className="eyebrow">Founder message</p>
              <blockquote>“Pressure reveals the foundation. Purpose decides what gets built next.”</blockquote>
            </div>
          </aside>
        </section>

        <section className="section">
          <div className="section-heading">
            <p className="eyebrow">Do more than feel motivated</p>
            <h2>Choose the next Brick.</h2>
            <p className="lead">Explore the movement first. Create an account only when you want to save progress, enter private community spaces, track programs, or manage purchases.</p>
          </div>
          <div className="ecosystem-grid flagship-grid">
            {flagship.map((item, index) => (
              <Link className="feature-card" key={item.title} href={item.href}>
                <span className="card-number">0{index + 1}</span>
                <p className="eyebrow">{item.eyebrow}</p>
                <h3>{item.title}</h3>
                <p>{item.copy}</p>
                <span className="text-link">{item.cta} →</span>
              </Link>
            ))}
          </div>
        </section>

        <section className="section visual-story-grid">
          <article className="visual-story-card">
            <Image src={imageFor("brotherhood")} alt="Concrete brotherhood and community" width={900} height={700} />
            <div>
              <p className="eyebrow">Concrete Nation</p>
              <h2>You do not have to build alone.</h2>
              <p>Crews, accountability, mentorship, referrals, service, practical resources, and opportunities to lead.</p>
              <Link className="text-link" href="/founding-100">Meet the Founding 100 →</Link>
            </div>
          </article>
          <article className="visual-story-card">
            <Image src={imageFor("familyGenerations")} alt="Family and generations representing Concrete Motivation legacy" width={900} height={700} />
            <div>
              <p className="eyebrow">Family & legacy</p>
              <h2>Build something worth handing forward.</h2>
              <p>The work is bigger than individual achievement. Concrete is built to strengthen families, future generations, and the communities around them.</p>
              <Link className="text-link" href="/about-jaytee">Read the founder story →</Link>
            </div>
          </article>
        </section>

        <section className="section">
          <div className="section-heading">
            <p className="eyebrow">One movement. Three engines.</p>
            <h2>Attention becomes trust. Trust becomes action.</h2>
          </div>
          <div className="ecosystem-grid">
            {ecosystem.map((item, index) => (
              <Link className="feature-card" key={item.title} href={item.href}>
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
            <Link className="text-link" href="/concrete-conversations">Explore Concrete Conversations →</Link>
          </div>
          <div className="media-frame" aria-label="Featured content area">
            <span className="play-button" aria-hidden="true">▶</span>
            <p>Watch Concrete Motivation and Concrete Conversations</p>
            <a className="button button-secondary" href={siteConfig.links.youtube}>Open YouTube</a>
          </div>
        </section>

        <section className="section nation-section">
          <p className="eyebrow">Concrete Nation</p>
          <h2>{siteConfig.promise}</h2>
          <p className="lead">A community designed to connect people with accountability, mentors, practical resources, referrals, collaborations, service, and opportunities to become successful together.</p>
          <div className="nation-grid">
            {["Accountability circles", "Mentorship and skill exchange", "Career and business referrals", "Member challenges and progress", "Workshops and live conversations", "Opportunities to contribute and lead"].map((item) => <div className="nation-item" key={item}>{item}</div>)}
          </div>
          <div className="button-row">
            <Link className="button button-primary" href="/founding-100">Founding 100</Link>
            <Link className="button button-secondary" href="/concrete-nation-charter">Read the Charter</Link>
          </div>
        </section>

        <section className="section">
          <div className="section-heading">
            <p className="eyebrow">Membership & merch</p>
            <h2>Everything in one public catalog.</h2>
            <p className="lead">Foundation $9/mo · Builder $19/mo · Legacy $49/mo. T-shirt $28 · Hoodie $55 · Cap $25 · Bottle $24 · Wristband $8. Secure account and checkout actions stay in the app.</p>
          </div>
          <div className="button-row">
            <Link className="button button-primary" href="/catalog">Open the Catalog</Link>
            <Link className="button button-secondary" href="/shop">Shop</Link>
            <Link className="text-link" href="/memberships">Compare memberships →</Link>
          </div>
        </section>

        <section className="section join-section">
          <div>
            <p className="eyebrow">Join the movement</p>
            <h2>Build your next chapter with people who expect you to move.</h2>
          </div>
          <div className="button-row">
            <Link className="button button-primary" href="/start-here">Start here</Link>
            <a className="button button-secondary" href={siteConfig.links.app}>Open the app</a>
            <Link className="text-link" href="/speaking">Book Jaytee →</Link>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
