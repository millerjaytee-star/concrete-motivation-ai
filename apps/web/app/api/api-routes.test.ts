import { describe, expect, it } from "vitest";
import { GET as getHealth } from "./health/route";
import { GET as getOrchestration, POST as postOrchestration } from "./orchestration/route";
import { POST as postLead } from "./crm/leads/route";
import { POST as postEmailDraft } from "./email/drafts/route";
import { POST as postCheckout } from "./stripe/checkout/route";

describe("release-candidate API routes", () => {
  it("reports a locked healthy release candidate", async () => {
    const body = await getHealth().json();
    expect(body).toMatchObject({ status: "ok", release: "candidate", externalActions: "locked", bots: 15 });
  });

  it("exposes and stages all bot contracts without executing", async () => {
    const catalog = await getOrchestration().json();
    expect(catalog.bots).toHaveLength(15);
    const response = await postOrchestration(new Request("http://local/api/orchestration", { method: "POST", body: JSON.stringify({ bot: "ceo", goal: "Plan the next safe phase" }) }));
    expect(response.status).toBe(202);
    expect(await response.json()).toMatchObject({ status: "staged", dryRun: true });
  });

  it("validates CRM consent and stages valid leads without persistence", async () => {
    const invalid = await postLead(new Request("http://local/api/crm/leads", { method: "POST", body: JSON.stringify({ email: "bad" }) }));
    expect(invalid.status).toBe(400);
    const valid = await postLead(new Request("http://local/api/crm/leads", { method: "POST", body: JSON.stringify({ name: "Test User", email: "test@example.com", path: "speaking", goal: "Book a workshop", consent: true }) }));
    expect(await valid.json()).toMatchObject({ status: "staged", persisted: false });
  });

  it("creates email drafts without sending", async () => {
    const response = await postEmailDraft(new Request("http://local/api/email/drafts", { method: "POST", body: JSON.stringify({ subject: "Owner review", body: "This remains a draft." }) }));
    expect(await response.json()).toMatchObject({ status: "drafted", sent: false });
  });

  it("keeps Stripe checkout in dry-run without explicit test configuration", async () => {
    const response = await postCheckout(new Request("http://local/api/stripe/checkout", { method: "POST", body: JSON.stringify({ priceId: "price_test_123" }) }));
    expect(await response.json()).toMatchObject({ status: "dry-run", checkoutCreated: false });
  });
});
