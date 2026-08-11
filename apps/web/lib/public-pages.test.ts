import { describe, expect, it } from "vitest";
import { publicPages, publicSlugs } from "./public-pages";

describe("public page catalog", () => {
  it("keeps the slug index and page records synchronized", () => {
    expect(publicSlugs).toEqual(Object.keys(publicPages));
    for (const slug of publicSlugs) {
      expect(publicPages[slug].slug).toBe(slug);
    }
  });

  it("gives every page complete copy, sections, and a CTA", () => {
    for (const page of Object.values(publicPages)) {
      expect(page.title.trim()).not.toBe("");
      expect(page.description.trim()).not.toBe("");
      expect(page.intro.trim()).not.toBe("");
      expect(page.sections.length).toBeGreaterThan(0);
      expect(page.primaryCta.label.trim()).not.toBe("");
      expect(page.primaryCta.href).toMatch(/^(\/|https?:|mailto:)/);
    }
  });

  it("does not expose live checkout routes while payments are staged", () => {
    const hrefs = Object.values(publicPages).flatMap((page) => [
      page.primaryCta.href,
      page.secondaryCta?.href,
    ]).filter(Boolean);

    expect(hrefs).not.toContain("/checkout");
    expect(publicPages.memberships.intro).toContain("Test mode");
  });
});
