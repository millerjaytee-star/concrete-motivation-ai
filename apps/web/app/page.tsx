import Image from "next/image";
import Link from "next/link";
import { SiteShell } from "@/components/SiteShell";
import { imageFor } from "@/lib/photography";
import { siteConfig } from "@/lib/site-config";

const pillars = [
  ["Foundation", "Tell the truth about the pressure before you decide what to build."],
  ["Discipline", "Keep one measurable promise when motivation gets quiet."],
  ["Resilience", "Use every setback as information, then rebuild stronger."],
  ["Purpose", "Move responsibly before every answer arrives."],
  ["Leadership", "Lead at home first. Build something the people you love can feel."],
  ["Legacy", "Leave people, teams and communities stronger than you found them."]
] as const;

const memberships = [
  ["Foundation", "$9", "$90/year", ["Weekly Concrete Challenge", "Members-only message archive", "Early access to new Shorts", "Community updates"]],
  ["Builder", "$19", "$190/year", ["Everything in Foundation", "Monthly live group session", "Downloadable action worksheets", "10% merchandise discount"]],
  ["Legacy", "$49", "$490/year", ["Everything in Builder", "Quarterly small-group coaching", "Priority Q&A access", "20% merchandise discount"]]
] as const;

const merch = [
  ["Concrete Hoodie", "$55", "Heavyweight black fleece / CM chest mark"],
  ["Foundation Tee", "$28", "Premium black cotton / CM front print"],
  ["CM Crown Cap", "$25", "Structured black cap / embroidered mark"],
  ["Stay Concrete Bottle", "$24", "Insulated black bottle / vertical CM mark"],
  ["Built Different Band", "$8", "Black silicone / gold debossed message"]
] as const;

const programs = [
  ["Built Under Pressure", "The signature keynote: a practical path from hard seasons to disciplined purpose."],
  ["The Leadership Standard", "For managers and teams carrying responsibility while performance still matters."],
  ["Stay Concrete", "Youth and athlete development built around effort, response and coachability."],
  ["From Pressure to Purpose", "For schools, communities and faith-aware audiences ready to rebuild with intention."]
] as const;

export default function HomePage() {
  return (
    <SiteShell>
      <main id="main-content">
        <section className="legacy-hero" id="top">
          <div className="legacy-hero-copy">
            <p className="eyebrow">Family • Faith • Leadership</p>
            <h1>Built under pressure.<br /><span>Proven through purpose.</span></h1>
            <p className="legacy-lead">A family-built movement helping people lead with faith, stand through pressure, and turn hard seasons into lasting purpose.</p>
            <div className="button-row">
              <Link className="button button-primary" href="/foundation-challenge">Start the free 7-day challenge</Link>
              <a className="button button-secondary" href="#family">Meet the Miller family</a>
            </div>
            <div className="proof-strip">
              <span><b>Real stories</b> Honest lessons from lived experience.</span>
              <span><b>Practical growth</b> One truth and one next action.</span>
              <span><b>Family-rooted</b> Leadership begins at home.</span>
              <span><b>Purpose-driven</b> Build a legacy that serves others.</span>
            </div>
          </div>
          <div className="hero-photo-stack" aria-label="Concrete Motivation family photography">
            <Image className="hero-photo hero-photo-main" src={imageFor("hero")} alt="Jaytee Miller, founder of Concrete Motivation" width={1000} height={1200} priority />
            <Image className="hero-photo hero-photo-small one" src={imageFor("familyLegacy")} alt="The Miller family together" width={700} height={700} />
            <Image className="hero-photo hero-photo-small two" src={imageFor("marriageCommitment")} alt="Jaytee and his wife on their wedding day" width={700} height={700} />
          </div>
        </section>

        <section className="numbered-section" id="story">
          <div className="section-number">01 / THE FOUNDATION</div>
          <div className="editorial-grid">
            <div>
              <h2>This was not<br />built in comfort.</h2>
            </div>
            <div className="story-copy">
              <p>Concrete Motivation came from carrying responsibility while still becoming.</p>
              <p>Jaytee Miller is a husband, father, operations leader and builder who learned leadership in real rooms—opening doors, developing people, owning results, providing for family and rebuilding after setbacks. Through grief, pressure, career changes and the daily responsibility of showing up for the people who depend on him, one truth kept returning: motivation may start the movement, but discipline, faith and structure make it last.</p>
              <p>Concrete Motivation became the message. Concrete Nation became the family around it—a place for people who have been overlooked, underestimated or tested by life to place one honest brick at a time. The standard is simple: tell the truth, make the plan, protect the people and execute the next right step.</p>
              <blockquote>“You rebuild your life one kept promise at a time.”</blockquote>
              <Link className="text-link" href="/our-story">Read the complete Concrete Story →</Link>
            </div>
          </div>
        </section>

        <section className="numbered-section family-section" id="family">
          <div className="section-number">02 / THE MILLER FAMILY</div>
          <div className="section-heading wide-heading">
            <p className="eyebrow">The family is the foundation</p>
            <h2>Concrete Nation<br />started at home.</h2>
            <p className="lead">Before it was a website, membership or stage, it was a family choosing to keep building together. Marriage taught partnership. Fatherhood made leadership personal. The children made legacy visible. Concrete Nation carries those values forward: love with standards, faith with action, resilience with honesty, and success that strengthens the people around you.</p>
          </div>
          <div className="family-gallery">
            <figure className="family-card family-wide"><Image src={imageFor("weddingFamily")} alt="The Miller family together" width={1200} height={900} /><figcaption>Family • The first team</figcaption></figure>
            <figure className="family-card"><Image src={imageFor("familyLegacy")} alt="A Miller family moment" width={900} height={900} /><figcaption>Joy • The reason</figcaption></figure>
            <figure className="family-card"><Image src={imageFor("marriageCommitment")} alt="Jaytee and his wife" width={900} height={900} /><figcaption>Partnership • The promise</figcaption></figure>
            <figure className="family-card"><Image src={imageFor("familyGenerations")} alt="Miller family across generations" width={900} height={1100} /><figcaption>Roots • The legacy</figcaption></figure>
            <figure className="family-card"><Image src={imageFor("nextGeneration")} alt="The next generation of the Miller family" width={900} height={900} /><figcaption>Future • The work</figcaption></figure>
            <figure className="family-card family-wide"><Image src={imageFor("fatherhood")} alt="Family and fatherhood" width={1200} height={900} /><figcaption>Home • The standard</figcaption></figure>
          </div>
        </section>

        <section className="numbered-section" id="framework">
          <div className="section-number">03 / THE FRAMEWORK</div>
          <div className="section-heading wide-heading"><h2>Six pillars.<br />One foundation.</h2><p className="lead">Motivation can start the movement. A system is what keeps it alive.</p></div>
          <div className="pillar-grid-old">
            {pillars.map(([title, copy], index) => <article key={title}><span>{String(index + 1).padStart(2, "0")}</span><h3>{title}</h3><p>{copy}</p></article>)}
          </div>
        </section>

        <section className="numbered-section nation-home" id="nation">
          <div className="section-number">04 / CONCRETE NATION</div>
          <div className="editorial-grid nation-editorial">
            <div><h2>One truth.<br />One action.<br />One reason to return.</h2></div>
            <div className="story-copy">
              <p>Concrete Nation is not an audience waiting for motivation. It is a community placing one brick every day. Start publicly without signing up; create a private app account when you want saved reflections, deeper tools and member access.</p>
              <div className="button-row"><Link className="button button-primary" href="/daily-brick">Lay today’s Brick</Link><a className="button button-secondary" href={siteConfig.links.app}>Open the app</a></div>
            </div>
          </div>
          <div className="brick-panel">
            <div><p className="eyebrow">Today’s Brick / Foundation</p><h3>Rest is not quitting. It is maintenance for the work that still matters.</h3><p>Review the week, celebrate one kept promise, and choose next week’s first brick.</p></div>
            <div className="brick-meter"><span>0 of 7 bricks placed</span><strong>0%</strong><div className="meter"><i /></div></div>
          </div>
        </section>

        <section className="numbered-section flagship-section" id="build">
          <div className="section-number">05 / START BUILDING</div>
          <div className="section-heading wide-heading"><h2>From first Brick<br />to Founding Builder.</h2><p className="lead">The website explains the movement. The app delivers the private work. Choose the entry point that matches your season.</p></div>
          <div className="flagship-grid-home">
            <Link href="/foundation-challenge" className="launch-card"><span>FREE</span><h3>7-Day Foundation Challenge</h3><p>Seven days. Seven kept promises. No payment required to start.</p><b>Start free →</b></Link>
            <Link href="/concrete-30-day-reset" className="launch-card featured"><span>$29 ONE TIME</span><h3>30-Day Concrete Reset</h3><p>Foundation, discipline, recovery, purpose and leadership—then your next 90-day Blueprint.</p><b>Explore the Reset →</b></Link>
            <Link href="/founding-100" className="launch-card"><span>INAUGURAL COHORT</span><h3>The Founding 100</h3><p>100 Builders. One Foundation. One Brick Every Day. Founding status is earned through action.</p><b>See the Founding 100 →</b></Link>
            <Link href="/concrete-os" className="launch-card"><span>THE SYSTEM</span><h3>Concrete OS</h3><p>Pressure → Foundation → Blueprint → Bricks → Inspection → Structure → Legacy.</p><b>See the system →</b></Link>
          </div>
          <div className="mini-link-row"><Link href="/founding-100-captains">Captain pathway →</Link><Link href="/concrete-nation-charter">Read the Charter →</Link><Link href="/programs">View all programs →</Link></div>
        </section>

        <section className="numbered-section" id="membership">
          <div className="section-number">06 / MEMBERSHIP</div>
          <div className="section-heading wide-heading"><h2>Don’t just watch.<br />Build with us.</h2><p className="lead">Founding-member pricing with monthly or annual access. Secure account and checkout actions live inside the member app.</p></div>
          <div className="membership-grid-old">
            {memberships.map(([name, monthly, annual, benefits], index) => <article key={name} className={index === 1 ? "membership-card popular" : "membership-card"}>{index === 1 ? <span className="popular-tag">Most popular</span> : null}<h3>{name}</h3><p className="membership-price"><strong>{monthly}</strong> per month <small>• {annual}</small></p><ul>{benefits.map(b => <li key={b}>{b}</li>)}</ul><a className="text-link" href={siteConfig.links.app}>Explore {name} →</a></article>)}
          </div>
        </section>

        <section className="numbered-section" id="shop">
          <div className="section-number">07 / SHOP THE STANDARD</div>
          <div className="section-heading wide-heading"><h2>Wear what<br />you stand for.</h2><p className="lead">The Concrete collection carries the same standard as the movement: simple, durable and built around what you represent.</p></div>
          <div className="merch-grid-home">
            {merch.map(([name, price, copy]) => <Link key={name} href="/shop" className="merch-card"><div className="merch-mark">CM</div><h3>{name}</h3><p>{copy}</p><strong>{price}</strong><span>View product →</span></Link>)}
          </div>
          <div className="catalog-banner"><div><p className="eyebrow">Official 2026 catalog</p><h3>The complete brand, membership & merch guide.</h3></div><Link className="button button-primary" href="/catalog">View the catalog</Link></div>
        </section>

        <section className="numbered-section media-section" id="watch">
          <div className="section-number">08 / WATCH & CONVERSATIONS</div>
          <div className="split-section-old">
            <div><p className="eyebrow">Concrete Motivation</p><h2>Messages for<br />the real season.</h2><p>Original short-form messages built to move people from inspiration to one responsible action.</p><a className="text-link" href={siteConfig.links.youtube}>Visit Concrete Motivation on YouTube →</a></div>
            <div className="conversation-card"><p className="eyebrow">Concrete Conversations</p><h2>Real stories.<br />Real lessons.<br />Real impact.</h2><p>A founder-led show about responsibility, leadership, fatherhood, faith, recovery, discipline and what people build after life tests the plan.</p><Link className="button button-secondary" href="/concrete-conversations">Explore Conversations</Link></div>
          </div>
        </section>

        <section className="numbered-section" id="speaking">
          <div className="section-number">09 / SPEAKING & PROGRAMS</div>
          <div className="section-heading wide-heading"><h2>Move the room<br />toward action.</h2></div>
          <div className="program-grid-home">{programs.map(([title, copy], index) => <article key={title}><span>{String(index + 1).padStart(2, "0")}</span><h3>{title}</h3><p>{copy}</p></article>)}</div>
          <div className="speaking-photo"><Image src={imageFor("weddingPortrait")} alt="Jaytee Miller and family representing commitment and legacy" width={1400} height={900} /><div><p className="eyebrow">Build with us</p><h2>What are you building under pressure?</h2><p>Bring Concrete Motivation to your school, team, church, organization, podcast or leadership event.</p><div className="button-row"><Link className="button button-primary" href="/speaking">Start a booking conversation</Link><Link className="button button-secondary" href="/catalog">View the official catalog</Link></div></div></div>
        </section>
      </main>
    </SiteShell>
  );
}
