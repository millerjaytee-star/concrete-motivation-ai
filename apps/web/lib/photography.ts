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

const photos: Record<WebsitePhotoRole, string> = {
  hero: "/brand/founder-hero.jpg",
  founder: "/brand/founder-hero.jpg",
  marriageCommitment: "/brand/marriage-commitment.jpg",
  familyLegacy: "/brand/family-legacy.jpg",
  brotherhood: "/brand/concrete-brotherhood.jpg",
  community: "/brand/concrete-brotherhood.jpg",
  fatherhood: "/brand/family-home.jpg",
  nextGeneration: "/brand/next-generation.jpg",
  weddingFamily: "/brand/family-legacy.jpg",
  weddingTeam: "/brand/wedding-team.jpg",
  familyGenerations: "/brand/family-generations.jpg",
  weddingPortrait: "/brand/wedding-family-portrait.jpg"
};

export function imageFor(role: WebsitePhotoRole) {
  return photos[role];
}
