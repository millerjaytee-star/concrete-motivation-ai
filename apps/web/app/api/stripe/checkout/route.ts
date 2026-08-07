import { NextResponse } from "next/server";
import { validateCheckout } from "@/lib/api-contracts";

export async function POST(request: Request) {
  const validation = validateCheckout(await request.json().catch(() => null));
  if (!validation.ok) return NextResponse.json({ error: "Validation failed", details: validation.errors }, { status: 400 });

  const secret = process.env.STRIPE_SECRET_KEY ?? "";
  const enabled = process.env.STRIPE_ENABLE_TEST_SESSION_CREATION === "true";
  const allowed = (process.env.STRIPE_ALLOWED_TEST_PRICE_IDS ?? "").split(",").map((value) => value.trim()).filter(Boolean);
  if (!secret.startsWith("sk_test_") || !enabled) {
    return NextResponse.json({ status: "dry-run", checkoutCreated: false, reason: "Stripe test-session creation is not explicitly enabled.", request: validation.value }, { status: 202 });
  }
  if (!allowed.includes(validation.value.priceId)) return NextResponse.json({ error: "Price ID is not in the approved test allowlist." }, { status: 403 });

  const origin = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  const form = new URLSearchParams({ mode: "subscription", "line_items[0][price]": validation.value.priceId, "line_items[0][quantity]": "1", success_url: `${origin}/memberships?checkout=success`, cancel_url: `${origin}/memberships?checkout=cancelled` });
  if (validation.value.customerEmail) form.set("customer_email", validation.value.customerEmail);
  const response = await fetch("https://api.stripe.com/v1/checkout/sessions", { method: "POST", headers: { Authorization: `Bearer ${secret}`, "Content-Type": "application/x-www-form-urlencoded" }, body: form, cache: "no-store" });
  const result = await response.json();
  if (!response.ok) return NextResponse.json({ error: "Stripe test session failed", detail: result?.error?.message ?? "Unknown Stripe error" }, { status: 502 });
  return NextResponse.json({ status: "test-session-created", liveMode: false, id: result.id, url: result.url }, { status: 201 });
}
