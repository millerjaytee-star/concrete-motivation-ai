import { NextResponse } from "next/server";
import { validateLead } from "@/lib/api-contracts";

export async function POST(request: Request) {
  const validation = validateLead(await request.json().catch(() => null));
  if (!validation.ok) return NextResponse.json({ error: "Validation failed", details: validation.errors }, { status: 400 });
  return NextResponse.json({ status: "staged", persisted: false, lead: { ...validation.value, email: "[redacted]" }, nextStep: "Select and approve the production CRM provider and retention policy." }, { status: 202 });
}
