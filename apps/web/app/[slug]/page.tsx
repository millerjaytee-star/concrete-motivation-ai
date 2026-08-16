import type { Metadata, Route } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteShell } from "@/components/SiteShell";
import { publicPages, publicSlugs } from "@/lib/public-pages";
import { programPages, programSlugs } from "@/lib/program-pages";

const allPages = { ...publicPages, ...programPages };
const allSlugs = [...new Set([...publicSlugs, ...programSlugs])];

export function generateStaticParams() {
  return allSlugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const page = allPages[slug];
  if (!page) return {};
  return {
    title: page.title,
    description: page.description,
    alternates: { canonical: `/${page.slug}` },
    openGraph: {
      title: `${page.title} | Concrete Motivation`,
      description: page.description,
      url: `/${page.slug}`,
      type: "website"
    }
  };
}

function CtaLink({ href, label, secondary = false }: { href: string; label: string; secondary?: boolean }) {
  const className = secondary ? "button button-secondary" : "button button-primary";
  if (/^(https?:|mailto:|tel:)/.test(href)) {
    return <a className={className} href={href}>{label}</a>;
  }
  return <Link className={className} href={href as Route}>{label}</Link>;
}

export default async function PublicPageRoute({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const page = allPages[slug];
  if (!page) notFound();

  return (
    <SiteShell>
      <main id="main-content">
        <section className="page-hero">
          <div className="page-hero-inner">
            <p className="eyebrow">{page.eyebrow}</p>
            <h1>{page.title}</h1>
            <p className="page-lead">{page.description}</p>
            <div className="button-row">
              <CtaLink href={page.primaryCta.href} label={page.primaryCta.label} />
              {page.secondaryCta ? <CtaLink href={page.secondaryCta.href} label={page.secondaryCta.label} secondary /> : null}
            </div>
          </div>
        </section>

        <section className="section page-intro">
          <p>{page.intro}</p>
        </section>

        <section className="section content-grid" aria-label={`${page.title} details`}>
          {page.sections.map((section, index) => (
            <article className="content-card" key={section.title}>
              <span className="card-number">{String(index + 1).padStart(2, "0")}</span>
              <h2>{section.title}</h2>
              <p>{section.body}</p>
              {section.items ? (
                <ul>
                  {section.items.map((item) => <li key={item}>{item}</li>)}
                </ul>
              ) : null}
            </article>
          ))}
        </section>

        <section className="section closing-cta">
          <div>
            <p className="eyebrow">Your next move</p>
            <h2>{page.primaryCta.label}</h2>
          </div>
          <CtaLink href={page.primaryCta.href} label={page.primaryCta.label} />
        </section>
      </main>
    </SiteShell>
  );
}
