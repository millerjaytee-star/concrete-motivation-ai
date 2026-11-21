import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { commandStoreConfigured, getCommandState, mutateCommand, runScheduledCommandAutomations } from "@/lib/command-store";

const owner = "11111111-2222-4333-8444-555555555555";
const endpoint = "https://staging.supabase.co";

beforeEach(() => {
  vi.stubEnv("COMMAND_SUPABASE_URL", endpoint);
  vi.stubEnv("COMMAND_SUPABASE_SERVICE_KEY", "sb_secret_test-fixture");
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe("Command Center persistence transport", () => {
  it("sends modern secret keys only as apikey to the service-only RPC", async () => {
    const fetch = vi.fn().mockResolvedValue(Response.json({ records: [] }));
    vi.stubGlobal("fetch", fetch);
    await expect(getCommandState(owner)).resolves.toEqual({ records: [] });
    expect(fetch).toHaveBeenCalledWith(`${endpoint}/rest/v1/rpc/cm_command_state`, expect.objectContaining({
      method: "POST",
      headers: { apikey: "sb_secret_test-fixture", "Content-Type": "application/json" },
      body: JSON.stringify({ p_actor: owner }),
      cache: "no-store",
      redirect: "error"
    }));
  });

  it("supports legacy service role JWTs and omits workspace data from scheduled responses", async () => {
    vi.stubEnv("COMMAND_SUPABASE_SERVICE_KEY", "legacy.jwt.fixture");
    const fetch = vi.fn().mockResolvedValue(Response.json({ processed: 2 }));
    vi.stubGlobal("fetch", fetch);
    await expect(runScheduledCommandAutomations(owner)).resolves.toEqual({ processed: 2 });
    expect(fetch).toHaveBeenCalledWith(`${endpoint}/rest/v1/rpc/cm_command_tick`, expect.objectContaining({
      headers: { apikey: "legacy.jwt.fixture", Authorization: "Bearer legacy.jwt.fixture", "Content-Type": "application/json" },
      body: JSON.stringify({ p_actor: owner })
    }));
  });

  it("rejects insecure remote configuration before attaching a key", async () => {
    vi.stubEnv("COMMAND_SUPABASE_URL", "http://staging.supabase.co");
    const fetch = vi.fn();
    vi.stubGlobal("fetch", fetch);
    expect(commandStoreConfigured()).toBe(false);
    await expect(getCommandState(owner)).rejects.toMatchObject({ status: 503 });
    expect(fetch).not.toHaveBeenCalled();
  });

  it("maps known SQL errors and keeps untrusted diagnostics out of the browser", async () => {
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(Response.json({ code: "CM004", message: "internal diagnostic" }, { status: 400 }))
      .mockResolvedValueOnce(Response.json({ code: "toString", message: "internal diagnostic" }, { status: 500 })));
    await expect(mutateCommand(owner, { kind: "save_record", area: "nation", title: "iOS", stage: "Resolved" }))
      .rejects.toMatchObject({ status: 400, message: "Add source evidence before recording this status." });
    await expect(getCommandState(owner))
      .rejects.toMatchObject({ status: 502, message: "Workspace storage could not complete the request." });
  });
});
