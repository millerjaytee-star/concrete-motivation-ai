import { describe, expect, it } from "vitest";
import { programPages, programSlugs } from "@/lib/program-pages";
import { publicPages, publicSlugs } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

const pages = { ...publicPages, ...programPages };
const slugs = new Set([...publicSlugs, ...programSlugs]);
const requiredJourneys = [
  "start-here",
  "concrete-nation",
  "daily-brick",
  "foundation-challenge",
  "concrete-conversations",
  "speaking",
  "programs",
  "memberships",
  "resources",
  "shop",
  "join"
];

describe("public route catalog", () => {
  it.each(requiredJourneys)("provides the %s experience", (slug) => {
    expect(slugs.has(slug)).toBe(true);
    expect(pages[slug].title).toBeTruthy();
    expect(pages[slug].description).toBeTruthy();
    expect(pages[slug].sections.length).toBeGreaterThan(0);
  });

  it("keeps every internal call to action on a real route", () => {
    for (const page of Object.values(pages)) {
      for (const cta of [page.primaryCta, page.secondaryCta].filter(Boolean)) {
        if (!cta || !cta.href.startsWith("/") || cta.href === "/") continue;
        expect(slugs.has(cta.href.slice(1)), `${page.slug} links to ${cta.href}`).toBe(true);
      }
    }
  });

  it("keeps page keys and canonical slugs aligned", () => {
    for (const [key, page] of Object.entries(pages)) expect(page.slug).toBe(key);
  });

  it("does not default production CTAs to preview hosts", () => {
    expect(siteConfig.links.website).toBe("https://concretemotivation.com");
    expect(siteConfig.links.app).toBe("https://app.concretemotivation.com");
  });
});
