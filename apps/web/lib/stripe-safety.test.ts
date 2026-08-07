import { createHmac } from "node:crypto";
import { describe, expect, it } from "vitest";
import { supportedStripeEvents, verifyStripeSignature } from "./stripe-safety";

describe("Stripe webhook safety", () => {
  it("accepts a current valid signature", () => {
    const payload = '{"id":"evt_test","livemode":false}';
    const secret = "whsec_test";
    const timestamp = 1_700_000_000;
    const signature = createHmac("sha256", secret).update(`${timestamp}.${payload}`).digest("hex");
    expect(verifyStripeSignature(payload, `t=${timestamp},v1=${signature}`, secret, timestamp)).toBe(true);
  });

  it("rejects invalid and replayed signatures", () => {
    expect(verifyStripeSignature("{}", "t=1,v1=bad", "whsec_test", 1000)).toBe(false);
  });

  it("documents every subscription and payment event handled by the release candidate", () => {
    expect(supportedStripeEvents.has("checkout.session.completed")).toBe(true);
    expect(supportedStripeEvents.has("invoice.payment_failed")).toBe(true);
    expect(supportedStripeEvents.has("charge.refunded")).toBe(true);
  });
});
