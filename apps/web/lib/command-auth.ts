import type { NextRequest, NextResponse } from "next/server";

export const commandSessionCookie = "concrete_command_session";
const uuid = /^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i;

export class CommandAuthError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
  }
}

function authConfig() {
  const url = process.env.COMMAND_SUPABASE_URL?.trim().replace(/\/$/, "");
  const key = process.env.COMMAND_SUPABASE_PUBLISHABLE_KEY?.trim();
  const ownerId = process.env.COMMAND_OWNER_ID?.trim().toLowerCase();
  if (!url || !key || !ownerId || !uuid.test(ownerId)) return null;
  try {
    const parsed = new URL(url);
    const local = ["localhost", "127.0.0.1"].includes(parsed.hostname);
    if (parsed.protocol !== "https:" && !(parsed.protocol === "http:" && local)) return null;
    if (parsed.username || parsed.password || parsed.search || parsed.hash || parsed.pathname !== "/") return null;
    return { url, key, ownerId };
  } catch {
    return null;
  }
}

export function commandAuthConfigured() {
  return authConfig() !== null;
}

function requireConfig() {
  const config = authConfig();
  if (!config) throw new CommandAuthError("Owner authentication is awaiting staging configuration.", 503);
  return config;
}

async function authRequest(url: string, init: RequestInit) {
  try {
    return await fetch(url, { ...init, cache: "no-store", redirect: "error", signal: AbortSignal.timeout(6000) });
  } catch {
    throw new CommandAuthError("The authentication service is temporarily unavailable.", 503);
  }
}

export async function signInCommandOwner(email: unknown, password: unknown) {
  const { url, key, ownerId } = requireConfig();
  if (typeof email !== "string" || typeof password !== "string" ||
      !email.trim() || email.length > 254 || !password || password.length > 1024) {
    throw new CommandAuthError("Enter your owner account email and password.", 400);
  }
  const response = await authRequest(`${url}/auth/v1/token?grant_type=password`, {
    method: "POST",
    headers: { apikey: key, "content-type": "application/json" },
    body: JSON.stringify({ email: email.trim(), password })
  });
  if (response.status === 429) throw new CommandAuthError("Too many sign-in attempts. Try again shortly.", 429);
  if (response.status >= 500) throw new CommandAuthError("The authentication service is temporarily unavailable.", 503);
  const session = response.ok ? await response.json() : null;
  if (!session || session.user?.id?.toLowerCase() !== ownerId || session.user?.is_anonymous === true ||
      typeof session.access_token !== "string" || !Number.isFinite(session.expires_in) || session.expires_in < 1) {
    throw new CommandAuthError("Sign-in failed for the configured owner account.", 401);
  }
  return { token: session.access_token as string, lifetime: Math.min(3600, Math.floor(session.expires_in)) };
}

export async function requireCommandOwner(request: NextRequest) {
  const { url, key, ownerId } = requireConfig();
  const token = request.cookies.get(commandSessionCookie)?.value;
  if (!token || token.length > 8192) throw new CommandAuthError("Sign in to the Command Center.", 401);
  const response = await authRequest(`${url}/auth/v1/user`, {
    headers: { apikey: key, authorization: `Bearer ${token}` }
  });
  if (response.status >= 500) throw new CommandAuthError("The authentication service is temporarily unavailable.", 503);
  const user = response.ok ? await response.json() : null;
  if (!user || user.id?.toLowerCase() !== ownerId || user.is_anonymous === true) {
    throw new CommandAuthError("Sign in to the Command Center as the configured owner.", 401);
  }
  return ownerId;
}

export function setCommandSession(response: NextResponse, token: string, lifetime: number) {
  response.cookies.set(commandSessionCookie, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "strict",
    path: "/api/command-center",
    maxAge: lifetime
  });
}

export function verifyCommandOrigin(request: NextRequest) {
  const origin = request.headers.get("origin");
  const contentType = request.headers.get("content-type")?.split(";")[0];
  const deploymentOrigin = process.env.COMMAND_ORIGIN?.trim();
  if (!origin || (origin !== request.nextUrl.origin && origin !== deploymentOrigin) ||
      request.headers.get("sec-fetch-site") === "cross-site" || contentType !== "application/json") {
    throw new CommandAuthError("The request did not originate from the Command Center.", 403);
  }
}
