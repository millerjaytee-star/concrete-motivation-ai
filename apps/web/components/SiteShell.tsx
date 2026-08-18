import Link from "next/link";
import { siteConfig } from "@/lib/site-config";

const primary = [
  ["Story", "/our-story"],
  ["Challenge", "/foundation-challenge"],
  ["30-Day Reset", "/concrete-30-day-reset"],
  ["Founding 100", "/founding-100"],
  ["Membership", "/memberships"],
  ["Shop", "/shop"],
  ["Catalog", "/catalog"]
] as const;

const footer = [
  ["Start Here", "/start-here"],
  ["About Jaytee", "/about-jaytee"],
  ["Concrete Story", "/our-story"],
  ["Concrete Nation", "/concrete-nation"],
  ["Daily Brick", "/daily-brick"],
  ["7-Day Challenge", "/foundation-challenge"],
  ["30-Day Reset", "/concrete-30-day-reset"],
  ["Founding 100", "/founding-100"],
  ["Founding Captains", "/founding-100-captains"],
  ["Founding Charter", "/concrete-nation-charter"],
  ["Concrete OS", "/concrete-os"],
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
