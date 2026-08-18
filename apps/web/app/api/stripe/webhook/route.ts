import { NextResponse } from "next/server";
import { isSupportedStripeEvent, parseStripeEvent, StripeWebhookError, verifyStripeSignature } from "@/lib/stripe-webhook";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function jsonError(error: unknown) {
  if (error instanceof StripeWebhookError) return NextResponse.json({ error: error.message }, { status: error.status });
  return NextResponse.json({ error: "Webhook processing failed" }, { status: 500 });
}

export async function POST(request: Request) {
  try {
    const rawBody = await request.text();
    verifyStripeSignature(rawBody, request.headers.get("stripe-signature"), process.env.STRIPE_WEBHOOK_SECRET ?? "");
    const event = parseStripeEvent(rawBody);
    if (!isSupportedStripeEvent(event.type)) return NextResponse.json({ received: true, ignored: true });

    const supabaseUrl = process.env.SUPABASE_URL?.replace(/\/$/, "");
    const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
    const eventsTable = process.env.STRIPE_WEBHOOK_EVENTS_TABLE ?? "stripe_webhook_events";
    if (!supabaseUrl || !serviceRoleKey) return NextResponse.json({ error: "Webhook persistence is not configured" }, { status: 503 });

    const response = await fetch(`${supabaseUrl}/rest/v1/${encodeURIComponent(eventsTable)}`, {
      method: "POST",
      headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}`, "Content-Type": "application/json", Prefer: "resolution=ignore-duplicates,return=minimal" },
      body: JSON.stringify({ stripe_event_id: event.id, event_type: event.type, livemode: event.livemode ?? false, payload: JSON.parse(rawBody) })
    });
    if (!response.ok) return NextResponse.json({ error: "Webhook persistence failed" }, { status: 502 });
    return NextResponse.json({ received: true });
  } catch (error) {
    return jsonError(error);
  }
}

export function GET() {
  return NextResponse.json({ error: "Method not allowed" }, { status: 405, headers: { Allow: "POST" } });
}
