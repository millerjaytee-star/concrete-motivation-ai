import { NextResponse } from "next/server";
import { botCatalog, integrations } from "@/lib/release-candidate";

export function GET() {
  return NextResponse.json({ status: "ok", release: "candidate", externalActions: "locked", bots: botCatalog.length, integrations: integrations.length });
}
