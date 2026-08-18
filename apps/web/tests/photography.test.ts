import { existsSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { imageFor, type WebsitePhotoRole } from "@/lib/photography";

const brandRoot = resolve(process.cwd(), "public");
const roles: WebsitePhotoRole[] = [
  "hero",
  "founder",
  "founderFocus",
  "marriageCommitment",
  "legacyCeremony",
  "familyLegacy",
  "fatherhood",
  "brotherhood",
  "community",
  "familyUnity",
  "nextGeneration",
  "weddingFamily",
  "weddingTeam",
  "familyGenerations",
  "weddingPortrait"
];

function assetPath(role: WebsitePhotoRole) {
  return resolve(brandRoot, imageFor(role).replace(/^\//, ""));
}

describe("semantic photography system", () => {
  it("resolves every role to an existing brand asset", () => {
    for (const role of roles) expect(existsSync(assetPath(role)), role).toBe(true);
  });

  it("keeps the critical storytelling roles distinct", () => {
    expect(imageFor("hero")).not.toBe(imageFor("founderFocus"));
    expect(imageFor("familyLegacy")).not.toBe(imageFor("fatherhood"));
    expect(imageFor("familyUnity")).not.toBe(imageFor("nextGeneration"));
  });

  it("returns only local /brand references", () => {
    for (const role of roles) {
      expect(imageFor(role)).toMatch(/^\/brand\/[\w.-]+\.(?:jpg|jpeg|png)$/);
      expect(imageFor(role)).not.toMatch(/^https?:/);
    }
  });

  it("keeps all approved central references resolvable", () => {
    const imageFiles = readdirSync(resolve(brandRoot, "brand")).filter((file) => /\.(?:jpg|jpeg|png)$/.test(file));
    expect(imageFiles.length).toBeGreaterThanOrEqual(9);
    for (const file of imageFiles) expect(existsSync(resolve(brandRoot, "brand", file))).toBe(true);
  });
});
