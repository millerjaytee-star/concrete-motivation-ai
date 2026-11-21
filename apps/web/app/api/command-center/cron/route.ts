import { timingSafeEqual } from "node:crypto";
import { type NextRequest, NextResponse } from "next/server";
import { runScheduledCommandAutomations } from "@/lib/command-store";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const owner = process.env.COMMAND_OWNER_ID?.trim().toLowerCase();
  const secret = process.env.COMMAND_CRON_SECRET;
  const headers = { "Cache-Control": "no-store" };
  if (!owner || !secret || secret.length < 32) {
    return NextResponse.json({ error: "Scheduler awaiting configuration." }, { status: 503, headers });
  }
  const provided = Buffer.from(request.headers.get("authorization") ?? "");
  const expected = Buffer.from(`Bearer ${secret}`);
  if (provided.length !== expected.length || !timingSafeEqual(provided, expected)) {
    return NextResponse.json({ error: "Unauthorized." }, { status: 401, headers });
  }
  try {
    const result = await runScheduledCommandAutomations(owner);
    return NextResponse.json(result, { headers });
  } catch {
    return NextResponse.json({ error: "Automation scheduler could not process this tick." }, { status: 503, headers });
  }
}
