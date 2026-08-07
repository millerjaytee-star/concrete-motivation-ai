import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json({ status: "packaged", publishEnabled: false, assets: { shorts: 3, trailer: 1, captions: true, thumbnails: true, metadata: true }, blocker: "Owner-approved founder source photography and exact upload approval." });
}
