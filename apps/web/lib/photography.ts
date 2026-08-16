export type WebsitePhotoRole =
  | "hero"
  | "founder"
  | "marriageCommitment"
  | "familyLegacy"
  | "brotherhood"
  | "community"
  | "fatherhood"
  | "nextGeneration"
  | "weddingFamily"
  | "weddingTeam"
  | "familyGenerations"
  | "weddingPortrait";

const assetBase = (process.env.NEXT_PUBLIC_APP_ASSET_BASE ?? "https://concrete-nation.lovable.app").replace(/\/$/, "");

const fileFor: Record<WebsitePhotoRole, string> = {
  hero: "founder-hero.jpg",
  founder: "founder-hero.jpg",
  marriageCommitment: "marriage-commitment.jpg",
  familyLegacy: "family-legacy.jpg",
  brotherhood: "concrete-brotherhood.jpg",
  community: "concrete-brotherhood.jpg",
  fatherhood: "family-home.jpg",
  nextGeneration: "next-generation.jpg",
  weddingFamily: "family-legacy.jpg",
  weddingTeam: "wedding-team.jpg",
  familyGenerations: "family-generations.jpg",
  weddingPortrait: "wedding-family-portrait.jpg"
};

export function imageFor(role: WebsitePhotoRole) {
  return `${assetBase}/brand/${fileFor[role]}`;
}
