import { createHmac, timingSafeEqual } from "node:crypto";

export const SUPPORTED_STRIPE_EVENTS = new Set([
  "checkout.session.completed",
  "checkout.session.async_payment_succeeded",
  "checkout.session.async_payment_failed",
  "customer.subscription.created",
  "customer.subscription.updated",
  "customer.subscription.deleted",
  "invoice.paid",
  "invoice.payment_failed"
]);

const SIGNATURE_TOLERANCE_SECONDS = 300;

export class StripeWebhookError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message);
    this.name = "StripeWebhookError";
  }
}

export function verifyStripeSignature(payload: string, signatureHeader: string | null, secret: string, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (!signatureHeader) throw new StripeWebhookError(400, "Missing Stripe signature");
  if (!secret) throw new StripeWebhookError(503, "Stripe webhook configuration is incomplete");
  const values = new Map<string, string[]>();
  for (const part of signatureHeader.split(",")) {
    const [key, value] = part.split("=", 2);
    if (!key || !value) continue;
    values.set(key, [...(values.get(key) ?? []), value]);
  }
  const timestamp = Number(values.get("t")?.[0]);
  const signatures = values.get("v1") ?? [];
  if (!Number.isInteger(timestamp) || signatures.length === 0) throw new StripeWebhookError(400, "Malformed Stripe signature");
  if (Math.abs(nowSeconds - timestamp) > SIGNATURE_TOLERANCE_SECONDS) throw new StripeWebhookError(400, "Expired Stripe signature");
  const expected = createHmac("sha256", secret).update(`${timestamp}.${payload}`).digest("hex");
  const valid = signatures.some((candidate) => {
    const actual = Buffer.from(candidate, "utf8");
    const expectedBytes = Buffer.from(expected, "utf8");
    return actual.length === expectedBytes.length && timingSafeEqual(actual, expectedBytes);
  });
  if (!valid) throw new StripeWebhookError(400, "Invalid Stripe signature");
}

export function parseStripeEvent(payload: string): { id: string; type: string; livemode?: boolean } {
  let event: unknown;
  try { event = JSON.parse(payload); } catch { throw new StripeWebhookError(400, "Malformed Stripe event"); }
  if (!event || typeof event !== "object") throw new StripeWebhookError(400, "Malformed Stripe event");
  const candidate = event as { id?: unknown; type?: unknown; livemode?: unknown };
  if (typeof candidate.id !== "string" || !candidate.id || typeof candidate.type !== "string" || !candidate.type) {
    throw new StripeWebhookError(400, "Stripe event is missing id or type");
  }
  return { id: candidate.id, type: candidate.type, livemode: typeof candidate.livemode === "boolean" ? candidate.livemode : undefined };
}

export function isSupportedStripeEvent(type: string) {
  return SUPPORTED_STRIPE_EVENTS.has(type);
}
