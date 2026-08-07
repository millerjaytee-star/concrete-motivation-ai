import { describe, expect, it } from "vitest";
import { cleanText, validateBotRun, validateCheckout, validateLead } from "./api-contracts";

describe("internal API validation", () => {
  it("normalizes and bounds untrusted text", () => {
    expect(cleanText("  build\n\twell  ")).toBe("build well");
    expect(cleanText("abcdef", 3)).toBe("abc");
  });

  it("requires a known-shaped bot request", () => {
    expect(validateBotRun({ bot: "ceo", goal: "plan the week" }).ok).toBe(true);
    expect(validateBotRun({ bot: "", goal: "" }).ok).toBe(false);
  });

  it("requires consent and valid lead fields", () => {
    expect(validateLead({ name: "Jay", email: "jay@example.com", path: "speaking", goal: "Plan an event", consent: true }).ok).toBe(true);
    expect(validateLead({ name: "J", email: "bad", path: "", goal: "", consent: false }).ok).toBe(false);
  });

  it("only accepts Stripe price identifiers", () => {
    expect(validateCheckout({ priceId: "price_test_123", customerEmail: "owner@example.com" }).ok).toBe(true);
    expect(validateCheckout({ priceId: "prod_123" }).ok).toBe(false);
  });
});
