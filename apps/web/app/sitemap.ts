import type { MetadataRoute } from "next";
import { publicSlugs } from "@/lib/public-pages";
import { programSlugs } from "@/lib/program-pages";
import { siteConfig } from "@/lib/site-config";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = siteConfig.links.website.replace(/\/$/, "");
  const slugs = [...new Set([...publicSlugs, ...programSlugs])];
  const priorityRoutes = [
    "our-story",
    "start-here",
    "concrete-nation",
    "concrete-30-day-reset",
    "founding-100",
    "speaking",
    "videos",
    "shop",
    "memberships"
  ];

  return [
    { url: base, changeFrequency: "weekly", priority: 1 },
    ...slugs.map((slug) => ({
      url: `${base}/${slug}`,
      changeFrequency: "monthly" as const,
      priority: priorityRoutes.includes(slug) ? 0.8 : 0.6
    }))
  ];
}
