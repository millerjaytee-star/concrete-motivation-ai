import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NextRequest, NextResponse } from "next/server";
import {
  commandAuthConfigured, commandSessionCookie, requireCommandOwner, setCommandSession,
  signInCommandOwner, verifyCommandOrigin
} from "@/lib/command-auth";

const owner = "11111111-2222-4333-8444-555555555555";
const url = "https://staging.supabase.co";
const app = "https://preview.example.com";

beforeEach(() => {
  vi.stubEnv("COMMAND_OWNER_ID", owner);
  vi.stubEnv("COMMAND_SUPABASE_URL", url);
  vi.stubEnv("COMMAND_SUPABASE_PUBLISHABLE_KEY", "test-publishable");
  vi.stubEnv("COMMAND_ORIGIN", app);
});

afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("Command Center owner authorization", () => {
  it("fails closed without an exact UUID or HTTPS project", () => {
    expect(commandAuthConfigured()).toBe(true);
    vi.stubEnv("COMMAND_OWNER_ID", "owner@example.com");
    expect(commandAuthConfigured()).toBe(false);
    vi.stubEnv("COMMAND_OWNER_ID", owner);
    vi.stubEnv("COMMAND_SUPABASE_URL", "http://staging.supabase.co");
    expect(commandAuthConfigured()).toBe(false);
  });

  it("only issues a bounded session for the configured Supabase account", async () => {
    const fetch = vi.fn()
      .mockResolvedValueOnce(Response.json({ user: { id: owner }, access_token: "session", expires_in: 5400 }))
      .mockResolvedValueOnce(Response.json({ user: { id: "11111111-2222-4333-8444-555555555556" }, access_token: "member", expires_in: 3600 }));
    vi.stubGlobal("fetch", fetch);
    await expect(signInCommandOwner("owner@example.test", "fixture password")).resolves.toEqual({ token: "session", lifetime: 3600 });
    expect(fetch.mock.calls[0][0]).toBe(`${url}/auth/v1/token?grant_type=password`);
    await expect(signInCommandOwner("member@example.test", "fixture password")).rejects.toMatchObject({ status: 401 });
  });

  it("verifies each authenticated request with Supabase", async () => {
    const fetch = vi.fn().mockResolvedValue(Response.json({ id: owner }));
    vi.stubGlobal("fetch", fetch);
    await expect(requireCommandOwner(new NextRequest(`${app}/api/command-center`))).rejects.toMatchObject({ status: 401 });
    expect(fetch).not.toHaveBeenCalled();
    const request = new NextRequest(`${app}/api/command-center`, { headers: { cookie: `${commandSessionCookie}=session` } });
    await expect(requireCommandOwner(request)).resolves.toBe(owner);
    expect(fetch.mock.calls[0][1].headers.authorization).toBe("Bearer session");
    fetch.mockResolvedValueOnce(Response.json({ id: owner, is_anonymous: true }));
    await expect(requireCommandOwner(request)).rejects.toMatchObject({ status: 401 });
  });

  it("locks down the cookie and rejects cross-site mutations", () => {
    const response = NextResponse.json({});
    vi.stubEnv("NODE_ENV", "production");
    setCommandSession(response, "session", 60);
    const cookie = response.headers.get("set-cookie");
    expect(cookie).toContain("Path=/api/command-center");
    expect(cookie).toContain("HttpOnly");
    expect(cookie).toContain("Secure");
    expect(cookie).toContain("SameSite=strict");

    const request = (origin: string, site = "same-origin") => new NextRequest(`${app}/api/command-center`, {
      method: "POST", headers: { origin, "content-type": "application/json", "sec-fetch-site": site }
    });
    expect(() => verifyCommandOrigin(request(app))).not.toThrow();
    expect(() => verifyCommandOrigin(request("https://untrusted.example.com"))).toThrow();
    expect(() => verifyCommandOrigin(request(app, "cross-site"))).toThrow();
  });
});

it("allows the exact Netlify preview origin through an internal proxy URL", () => {
  const preview = "https://deploy-preview-56--example.netlify.app";
  vi.stubEnv("COMMAND_BUILD_ORIGIN", preview);
  const request = (origin: string) => new NextRequest("http://localhost:8888/api/command-center", {
    method: "POST", headers: { origin, "content-type": "application/json", "sec-fetch-site": "same-origin" }
  });
  expect(() => verifyCommandOrigin(request(preview))).not.toThrow();
  expect(() => verifyCommandOrigin(request("https://deploy-preview-57--example.netlify.app"))).toThrow();
});
