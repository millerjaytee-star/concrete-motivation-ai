import { NextResponse } from "next/server";
import { dashboards, isDashboardView } from "@/lib/release-candidate";

export async function GET(_request: Request, { params }: { params: Promise<{ view: string }> }) {
  const { view } = await params;
  if (!isDashboardView(view)) return NextResponse.json({ error: "Unknown dashboard" }, { status: 404 });
  return NextResponse.json({ view, generatedFrom: "release-candidate registry", ...dashboards[view] });
}
