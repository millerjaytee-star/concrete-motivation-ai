import { NextResponse } from "next/server";

export function GET() {
  const configured = /^G-[A-Z0-9]+$/.test(process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID ?? "");
  return NextResponse.json({ provider: "Google Analytics 4", configured, consentRequired: true, advertisingSignals: false, events: ["page_view", "cta_click", "join_intent", "speaking_intent", "video_intent", "checkout_intent", "email_intent", "bot_stage"] });
}
