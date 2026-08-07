import { NextResponse } from "next/server";
import { supportedStripeEvents, verifyStripeSignature } from "@/lib/stripe-safety";

export async function POST(request: Request) {
  const payload = await request.text();
  const signature = request.headers.get("stripe-signature") ?? "";
  const secret = process.env.STRIPE_WEBHOOK_SECRET ?? "";
  if (!verifyStripeSignature(payload, signature, secret)) return NextResponse.json({ error: "Invalid Stripe signature" }, { status: 400 });
  let event: { id?: string; type?: string; livemode?: boolean };
  try {
    event = JSON.parse(payload) as { id?: string; type?: string; livemode?: boolean };
  } catch {
    return NextResponse.json({ error: "Invalid Stripe event payload" }, { status: 400 });
  }
  if (event.livemode) return NextResponse.json({ error: "Live Stripe events are disabled in this release candidate." }, { status: 403 });
  if (!event.type || !supportedStripeEvents.has(event.type)) return NextResponse.json({ received: true, handled: false, eventId: event.id ?? null });
  return NextResponse.json({ received: true, handled: "staged", persisted: false, eventId: event.id ?? null, type: event.type, nextStep: "Connect the approved membership/order data provider before production activation." });
}
