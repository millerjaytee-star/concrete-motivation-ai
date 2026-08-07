import { NextResponse } from "next/server";
import { cleanText } from "@/lib/api-contracts";

export async function POST(request: Request) {
  const data = await request.json().catch(() => null) as Record<string, unknown> | null;
  const subject = cleanText(data?.subject, 160);
  const body = cleanText(data?.body, 8000);
  if (!subject || !body) return NextResponse.json({ error: "Subject and body are required." }, { status: 400 });
  return NextResponse.json({ status: "drafted", sent: false, subject, bodyPreview: body.slice(0, 180), approvalRequired: "Exact recipients, sender, content, and send instruction." }, { status: 202 });
}
