import type { MetadataRoute } from "next";
import { publicSlugs } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = siteConfig.links.website.replace(/\/$/, "");
  return [
    { url: base, changeFrequency: "weekly", priority: 1 },
    ...publicSlugs.map((slug) => ({
      url: `${base}/${slug}`,
      changeFrequency: "monthly" as const,
      priority: ["our-story", "concrete-nation", "speaking", "videos"].includes(slug) ? 0.8 : 0.6
    }))
  ];
}
