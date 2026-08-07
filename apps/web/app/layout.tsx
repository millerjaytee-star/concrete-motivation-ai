import type { Metadata } from "next";
import "./globals.css";
import "./public-pages.css";
import "./command-center.css";
import { AnalyticsConsent } from "@/components/AnalyticsConsent";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: {
    default: "Concrete Motivation",
    template: "%s | Concrete Motivation"
  },
  description:
    "Concrete Motivation helps people carrying real responsibility turn pressure into purpose, disciplined action, stronger relationships, and shared success.",
  applicationName: "Concrete Motivation",
  category: "leadership development",
  keywords: ["motivational speaker", "leadership development", "discipline", "athlete mindset", "fatherhood", "Concrete Conversations", "Concrete Nation", "Jaytee Miller"],
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "https://concretemotivation.com"),
  alternates: { canonical: "/" },
  openGraph: {
    title: "Concrete Motivation",
    description: "Build from pressure. Lead with purpose. Move with discipline.",
    type: "website",
    siteName: "Concrete Motivation",
    locale: "en_US",
  },
  twitter: { card: "summary_large_image", title: "Concrete Motivation", description: "Build from pressure. Lead with purpose. Move with discipline." },
  robots: { index: true, follow: true }
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">Skip to content</a>
        {children}
        <AnalyticsConsent measurementId={process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          name: siteConfig.name,
          url: siteConfig.links.website,
          founder: { "@type": "Person", name: "Jaytee Miller" },
          slogan: siteConfig.phrase,
          sameAs: [siteConfig.links.youtube, siteConfig.links.instagram, siteConfig.links.tiktok, siteConfig.links.facebook].filter((url) => !url.startsWith("#")),
        }) }} />
      </body>
    </html>
  );
}
