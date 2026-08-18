export type WebsitePhotoRole =
  | "hero"
  | "founder"
  | "founderFocus"
  | "marriageCommitment"
  | "legacyCeremony"
  | "familyLegacy"
  | "fatherhood"
  | "brotherhood"
  | "community"
  | "familyUnity"
  | "nextGeneration"
  | "weddingFamily"
  | "weddingTeam"
  | "familyGenerations"
  | "weddingPortrait";

const fileFor: Record<WebsitePhotoRole, string> = {
  hero: "founder-hero.jpg",
  founder: "wedding-family-portrait.jpg",
  founderFocus: "concrete-brotherhood.jpg",
  marriageCommitment: "marriage-commitment.jpg",
  legacyCeremony: "next-generation.jpg",
  familyLegacy: "wedding-family-portrait.jpg",
  fatherhood: "family-home.jpg",
  brotherhood: "wedding-team.jpg",
  community: "family-generations.jpg",
  familyUnity: "family-generations.jpg",
  nextGeneration: "next-generation.jpg",
  weddingFamily: "wedding-family-portrait.jpg",
  weddingTeam: "wedding-team.jpg",
  familyGenerations: "family-generations.jpg",
  weddingPortrait: "marriage-commitment.jpg"
};

export function imageFor(role: WebsitePhotoRole) {
  return `/brand/${fileFor[role]}`;
}
