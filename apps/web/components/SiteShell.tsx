import Link from "next/link";
import { siteConfig } from "@/lib/site-config";

const primary = [
  ["Start Here", "/start-here"],
  ["Story", "/our-story"],
  ["System", "/inside-the-app"],
  ["Programs", "/programs"],
  ["Gatherings", "/gatherings"],
  ["Membership", "/memberships"]
] as const;

const footer = [
  ["Start Here", "/start-here"],
  ["About Jaytee", "/about-jaytee"],
  ["Concrete Story", "/our-story"],
  ["Who We Serve", "/who-we-serve"],
  ["Concrete Nation", "/concrete-nation"],
  ["Concrete Nation Gatherings", "/gatherings"],
  ["Inside the App", "/inside-the-app"],
  ["Concrete OS", "/concrete-os"],
  ["Foundation Assessment", "/assessment"],
  ["Build + Blueprint", "/build-blueprint"],
  ["Daily Brick", "/daily-brick"],
  ["Proof of Build", "/proof-of-build"],
  ["Concrete Passport", "/concrete-passport"],
  ["Concrete Foreman", "/concrete-foreman"],
  ["444 Challenge", "/444-challenge"],
  ["Crews", "/crews"],
  ["Opportunities", "/opportunities"],
  ["Concrete Exchange", "/concrete-exchange"],
  ["Concrete Foundation", "/concrete-foundation"],
  ["Concrete Saturday", "/concrete-saturday"],
  ["7-Day Challenge", "/foundation-challenge"],
  ["30-Day Reset", "/concrete-30-day-reset"],
  ["Founding 100", "/founding-100"],
  ["Founding Captains", "/founding-100-captains"],
  ["Founding Charter", "/concrete-nation-charter"],
  ["Concrete Conversations", "/concrete-conversations"],
  ["Speaking", "/speaking"],
  ["Programs", "/programs"],
  ["Memberships", "/memberships"],
  ["Shop", "/shop"],
  ["Digital Catalog", "/catalog"],
  ["Community Impact", "/community-impact"],
  ["Resources", "/resources"],
  ["Contact", "/join"],
  ["Support", "/support"],
  ["Privacy", "/privacy"],
  ["Terms", "/terms"],
  ["Refunds", "/refunds"],
  ["Accessibility", "/accessibility"]
] as const;

export function SiteShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header className="site-header">
        <Link className="brand" href="/" aria-label="Concrete Motivation home">
          <span className="brand-mark" aria-hidden="true">CM</span>
          <span>Concrete Motivation</span>
        </Link>
        <nav aria-label="Primary navigation">
          {primary.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}
          <a className="nav-cta" href={siteConfig.links.app}>Open the app</a>
        </nav>
      </header>
      {children}
      <footer>
        <div>
          <strong>CM · Concrete Motivation</strong>
          <p>Build from pressure. Lead with purpose. Move with discipline.</p>
          <p>{siteConfig.promise}</p>
          <p>The website explains the complete system. The app is the private workspace where Builders do and document the work.</p>
        </div>
        <div className="footer-links" aria-label="Website links">
          {footer.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}
        </div>
        <div className="footer-links" aria-label="Social links">
          <a href={siteConfig.links.app}>App</a>
          <a href={siteConfig.links.youtube}>YouTube</a>
          <a href={siteConfig.links.instagram}>Instagram</a>
        </div>
        <p>© 2026 Jaytee Miller · Concrete Motivation. Built under pressure. Proven through purpose.</p>
      </footer>
    </>
  );
}
