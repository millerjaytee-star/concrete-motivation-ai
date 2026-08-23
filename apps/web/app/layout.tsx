import type { Metadata } from "next";
import "./globals.css";
import "./public-pages.css";
import "./responsive-hardening.css";
import "./premium-polish.css";

export const metadata: Metadata = {
  title: {
    default: "Concrete Motivation",
    template: "%s | Concrete Motivation"
  },
  description:
    "Concrete Motivation helps people carrying real responsibility turn pressure into purpose, disciplined action, stronger relationships, and shared success.",
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "https://concretemotivation.com"),
  openGraph: {
    title: "Concrete Motivation",
    description: "Build from pressure. Lead with purpose. Move with discipline.",
    type: "website"
  },
  robots: { index: true, follow: true }
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">Skip to content</a>
        {children}
      </body>
    </html>
  );
}
