import Link from "next/link";
import { siteConfig } from "@/lib/site-config";

const primary = [
  ["Our Story", "/our-story"],
  ["Who We Serve", "/who-we-serve"],
  ["Conversations", "/concrete-conversations"],
  ["Concrete Nation", "/concrete-nation"],
  ["Speaking", "/speaking"],
  ["Videos", "/videos"]
] as const;

const footer = [
  ["Memberships", "/memberships"],
  ["Shop", "/shop"],
  ["Join / Contact", "/join"],
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
          <Link className="nav-cta" href="/join">Join</Link>
        </nav>
      </header>
      {children}
      <footer>
        <div>
          <strong>Concrete Motivation</strong>
          <p>{siteConfig.phrase}</p>
          <p>{siteConfig.promise}</p>
        </div>
        <div className="footer-links" aria-label="Website links">
          {footer.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}
        </div>
        <div className="footer-links" aria-label="Social links">
          <a href={siteConfig.links.youtube}>YouTube</a>
          <a href={siteConfig.links.instagram}>Instagram</a>
          <a href={siteConfig.links.tiktok}>TikTok</a>
          <a href={siteConfig.links.facebook}>Facebook</a>
        </div>
        <p>© 2026 Concrete Motivation. Built for real change. No fake metrics, testimonials, partners, or promises.</p>
      </footer>
    </>
  );
}
