import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteShell } from "@/components/SiteShell";
import { publicPages, publicSlugs } from "@/lib/public-pages";

export function generateStaticParams() {
  return publicSlugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const page = publicPages[slug];
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

export default async function PublicPageRoute({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const page = publicPages[slug];
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
              <Link className="button button-primary" href={page.primaryCta.href}>{page.primaryCta.label}</Link>
              {page.secondaryCta ? <Link className="button button-secondary" href={page.secondaryCta.href}>{page.secondaryCta.label}</Link> : null}
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
          <Link className="button button-primary" href={page.primaryCta.href}>{page.primaryCta.label}</Link>
        </section>
      </main>
    </SiteShell>
  );
}
