import { createHmac } from "node:crypto";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "@/app/api/stripe/webhook/route";

const secret = "whsec_test_secret";
const originalEnv = { ...process.env };

function signedBody(body: string) {
  const timestamp = Math.floor(Date.now() / 1000);
  const digest = createHmac("sha256", secret).update(`${timestamp}.${body}`).digest("hex");
  return { body, signature: `t=${timestamp},v1=${digest}` };
}

function request(body: string, signature?: string) {
  return new Request("http://localhost/api/stripe/webhook", {
    method: "POST",
    body,
    headers: signature ? { "stripe-signature": signature } : undefined
  });
}

function event(type = "checkout.session.completed") {
  return JSON.stringify({ id: "evt_test_123", type, livemode: false, data: { object: {} } });
}

afterEach(() => {
  process.env = { ...originalEnv };
  vi.restoreAllMocks();
});

describe("Stripe webhook endpoint", () => {
  it("rejects a missing signature", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    expect((await POST(request(event()))).status).toBe(400);
  });

  it("rejects an invalid signature", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    expect((await POST(request(event(), "t=1,v1=bad"))).status).toBe(400);
  });

  it("rejects malformed signed events", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    const signed = signedBody("not-json");
    expect((await POST(request(signed.body, signed.signature))).status).toBe(400);
  });

  it("returns configuration failure without acknowledging a supported event", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    const signed = signedBody(event());
    expect((await POST(request(signed.body, signed.signature))).status).toBe(503);
  });

  it("records a valid supported event and returns 200", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    process.env.SUPABASE_URL = "https://example.supabase.co";
    process.env.SUPABASE_SERVICE_ROLE_KEY = "server-only-test-key";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(null, { status: 201 })));
    const signed = signedBody(event());
    const response = await POST(request(signed.body, signed.signature));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ received: true });
  });

  it("handles duplicate event delivery idempotently", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    process.env.SUPABASE_URL = "https://example.supabase.co";
    process.env.SUPABASE_SERVICE_ROLE_KEY = "server-only-test-key";
    const fetchMock = vi.fn().mockResolvedValue(new Response(null, { status: 201 }));
    vi.stubGlobal("fetch", fetchMock);
    const signed = signedBody(event());
    expect((await POST(request(signed.body, signed.signature))).status).toBe(200);
    expect((await POST(request(signed.body, signed.signature))).status).toBe(200);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[0][1].headers.Prefer).toContain("ignore-duplicates");
  });

  it("acknowledges unsupported legitimate events without persistence", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const signed = signedBody(event("charge.refunded"));
    const response = await POST(request(signed.body, signed.signature));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ received: true, ignored: true });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("returns 502 when durable persistence fails", async () => {
    process.env.STRIPE_WEBHOOK_SECRET = secret;
    process.env.SUPABASE_URL = "https://example.supabase.co";
    process.env.SUPABASE_SERVICE_ROLE_KEY = "server-only-test-key";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(null, { status: 500 })));
    const signed = signedBody(event());
    expect((await POST(request(signed.body, signed.signature))).status).toBe(502);
  });
});
