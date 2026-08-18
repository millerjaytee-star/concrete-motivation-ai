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
  hero: "founder-hero.webp",
  // The founder portrait intentionally serves both founder roles; they are used
  // on separate page contexts and represent the same approved founder identity.
  founder: "founder-hero.webp",
  founderFocus: "founder-hero.webp",
  marriageCommitment: "marriage-commitment.webp",
  legacyCeremony: "wedding-family.webp",
  familyLegacy: "family-generations.webp",
  fatherhood: "family-home.webp",
  brotherhood: "wedding-team.webp",
  community: "concrete-community.webp",
  familyUnity: "family-home.webp",
  nextGeneration: "next-generation.webp",
  weddingFamily: "wedding-family.webp",
  weddingTeam: "wedding-team.webp",
  familyGenerations: "family-generations.webp",
  weddingPortrait: "marriage-commitment.webp"
};

const positionFor: Partial<Record<WebsitePhotoRole, string>> = {
  hero: "58% center",
  founder: "58% center",
  founderFocus: "58% center",
  marriageCommitment: "58% center",
  legacyCeremony: "58% center",
  familyLegacy: "center center",
  fatherhood: "center 45%",
  brotherhood: "center 42%",
  community: "center 48%",
  familyUnity: "center 42%",
  nextGeneration: "center 48%",
  weddingFamily: "center 42%",
  weddingTeam: "center 45%",
  familyGenerations: "center 42%",
  weddingPortrait: "58% center"
};

export function imageFor(role: WebsitePhotoRole) {
  return `/brand/${fileFor[role]}`;
}

export function objectPositionFor(role: WebsitePhotoRole) {
  return positionFor[role] ?? "center";
}

export const photoFiles = fileFor;
