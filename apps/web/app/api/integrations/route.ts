import { NextResponse } from "next/server";
import { integrations } from "@/lib/release-candidate";

export function GET() {
  return NextResponse.json({ release: "candidate", generatedAt: new Date().toISOString(), integrations, secretsExposed: false });
}
