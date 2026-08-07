import { describe, expect, it } from "vitest";
import { botCatalog, dashboards, dashboardViews, findBot, integrations } from "./release-candidate";

describe("release candidate registry", () => {
  it("connects all fifteen uniquely identified bots", () => {
    expect(botCatalog).toHaveLength(15);
    expect(new Set(botCatalog.map((bot) => bot.id)).size).toBe(15);
    expect(new Set(botCatalog.map((bot) => bot.slug)).size).toBe(15);
    for (const bot of botCatalog) expect(findBot(bot.slug)).toEqual(bot);
  });

  it("provides all eight required dashboards", () => {
    expect(dashboardViews).toEqual(["owner", "analytics", "revenue", "crm", "email", "youtube", "community", "stripe"]);
    for (const view of dashboardViews) {
      expect(dashboards[view].cards.length).toBeGreaterThanOrEqual(4);
      expect(dashboards[view].queue.length).toBeGreaterThan(0);
    }
  });

  it("keeps every external integration explicit about approval", () => {
    for (const integration of integrations) expect(integration.approvalRequired.trim()).not.toBe("");
    expect(integrations.find((item) => item.key === "stripe")?.mode).toBe("test-only");
    expect(integrations.find((item) => item.key === "deployment")?.mode).toBe("not-deployed");
  });
});
