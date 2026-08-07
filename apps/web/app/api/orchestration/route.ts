import { NextResponse } from "next/server";
import { validateBotRun } from "@/lib/api-contracts";
import { botCatalog, findBot } from "@/lib/release-candidate";

export function GET() {
  return NextResponse.json({ mode: "dry-run", bots: botCatalog });
}

export async function POST(request: Request) {
  const validation = validateBotRun(await request.json().catch(() => null));
  if (!validation.ok) return NextResponse.json({ error: "Validation failed", details: validation.errors }, { status: 400 });
  const bot = findBot(validation.value.bot);
  if (!bot) return NextResponse.json({ error: "Unknown bot" }, { status: 404 });
  return NextResponse.json({ status: "staged", dryRun: true, bot, request: validation.value, execution: "Run through the Python BotRunner after owner review when an external provider is enabled." }, { status: 202 });
}
