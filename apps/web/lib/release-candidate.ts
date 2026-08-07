export const dashboardViews = [
  "owner",
  "analytics",
  "revenue",
  "crm",
  "email",
  "youtube",
  "community",
  "stripe",
] as const;

export type DashboardView = (typeof dashboardViews)[number];
export type Readiness = "ready" | "staged" | "blocked";

export type Integration = {
  key: string;
  name: string;
  readiness: Readiness;
  mode: string;
  detail: string;
  approvalRequired: string;
};

export const integrations: Integration[] = [
  { key: "openai", name: "OpenAI", readiness: "staged", mode: "optional", detail: "Offline fallback is always available.", approvalRequired: "API spend and production key" },
  { key: "youtube", name: "YouTube", readiness: "ready", mode: "approval-gated", detail: "Connected through Composio; upload tooling is confirmation-gated.", approvalRequired: "Exact upload and visibility" },
  { key: "gmail", name: "Gmail", readiness: "ready", mode: "draft-only", detail: "Connected through Composio; campaigns remain staged.", approvalRequired: "Recipients, message, and send" },
  { key: "stripe", name: "Stripe", readiness: "staged", mode: "test-only", detail: "Adapter rejects live secret keys and defaults to dry-run.", approvalRequired: "Products, prices, and test-session creation" },
  { key: "elevenlabs", name: "ElevenLabs", readiness: "ready", mode: "approval-gated", detail: "Narration assets and an active connection are present.", approvalRequired: "Voice, script, and credit use" },
  { key: "analytics", name: "Google Analytics", readiness: "blocked", mode: "consent-ready", detail: "Consent-aware loader is ready; no measurement ID is configured.", approvalRequired: "Property, ID, privacy, and consent behavior" },
  { key: "crm", name: "CRM", readiness: "staged", mode: "local-first", detail: "Validated intake and pipeline contracts are ready for a selected data provider.", approvalRequired: "Provider, retention, and notifications" },
  { key: "deployment", name: "Deployment", readiness: "staged", mode: "not-deployed", detail: "Container, health endpoint, CI, and environment contract are prepared.", approvalRequired: "Hosting target and deploy" },
];

export type BotDefinition = {
  id: number;
  slug: string;
  name: string;
  group: "Brand & Content" | "Growth & Revenue" | "Operations";
  purpose: string;
  outputs: string[];
};

export const botCatalog: BotDefinition[] = [
  { id: 1, slug: "brand_architect", name: "Brand Architect", group: "Brand & Content", purpose: "Protect positioning, voice, offers, and brand consistency.", outputs: ["message", "audience", "tone", "offer", "next action"] },
  { id: 2, slug: "motivational_speech", name: "Motivational Speech", group: "Brand & Content", purpose: "Create original speeches grounded in responsibility and action.", outputs: ["hook", "speech", "engagement", "CTA"] },
  { id: 3, slug: "concrete_conversations_podcast", name: "Podcast", group: "Brand & Content", purpose: "Build complete Concrete Conversations episodes.", outputs: ["promise", "segments", "questions", "clips"] },
  { id: 4, slug: "social_media_content", name: "Social Content", group: "Brand & Content", purpose: "Turn ideas into ethical platform-ready content.", outputs: ["hooks", "script", "caption", "repurpose"] },
  { id: 5, slug: "athlete_outreach", name: "Athlete Outreach", group: "Growth & Revenue", purpose: "Open doors with athletes, coaches, and sports organizations.", outputs: ["target", "angle", "draft", "follow-up"] },
  { id: 6, slug: "business_growth", name: "Business Growth", group: "Growth & Revenue", purpose: "Develop practical offers, pricing ideas, and partnerships.", outputs: ["opportunity", "offer", "pricing", "sales action"] },
  { id: 7, slug: "operations", name: "Operations", group: "Operations", purpose: "Turn objectives into accountable execution systems.", outputs: ["priorities", "checklist", "SOP", "owner"] },
  { id: 8, slug: "faith_mindset", name: "Faith & Mindset", group: "Brand & Content", purpose: "Create responsible faith-aware mindset content.", outputs: ["theme", "reflection", "principle", "action"] },
  { id: 9, slug: "ceo", name: "CEO", group: "Operations", purpose: "Set executive priorities, risks, scoreboards, and next commands.", outputs: ["decision", "priorities", "risks", "scoreboard"] },
  { id: 10, slug: "content_director", name: "Content Director", group: "Brand & Content", purpose: "Plan campaigns across every brand channel.", outputs: ["thesis", "channels", "queue", "rhythm"] },
  { id: 11, slug: "podcast_producer", name: "Podcast Producer", group: "Brand & Content", purpose: "Move episodes from concept through production prep.", outputs: ["concept", "run of show", "guest prep", "clip plan"] },
  { id: 12, slug: "sales_outreach", name: "Sales Outreach", group: "Growth & Revenue", purpose: "Stage ethical speaking, sponsor, and partner outreach.", outputs: ["segment", "offer angle", "email", "follow-up"] },
  { id: 13, slug: "youtube_growth", name: "YouTube Growth", group: "Growth & Revenue", purpose: "Build searchable video and retention systems.", outputs: ["opportunity", "title", "thumbnail", "retention"] },
  { id: 14, slug: "crm", name: "CRM", group: "Operations", purpose: "Organize leads, stages, next actions, and follow-ups.", outputs: ["snapshot", "segments", "actions", "schedule"] },
  { id: 15, slug: "gmail_outreach", name: "Gmail Workflow", group: "Operations", purpose: "Stage Gmail-ready messages and tracking rules without sending.", outputs: ["goal", "lead list", "sequence", "tracking"] },
];

export type DashboardCard = { label: string; value: string; note: string; tone?: Readiness };
export type DashboardDefinition = { title: string; eyebrow: string; description: string; cards: DashboardCard[]; queue: string[] };

export const dashboards: Record<DashboardView, DashboardDefinition> = {
  owner: { title: "Owner Command Center", eyebrow: "Release control", description: "One view of readiness, approvals, integrations, and the next responsible move.", cards: [
    { label: "Bots", value: "15 / 15", note: "Registered in orchestration", tone: "ready" },
    { label: "Python tests", value: "154", note: "Passing release-candidate suite", tone: "ready" },
    { label: "Web build", value: "PASS", note: "Next.js production build", tone: "ready" },
    { label: "External actions", value: "LOCKED", note: "Owner approval required", tone: "staged" },
  ], queue: ["Choose canonical public site", "Approve staging provider", "Complete legal acceptance", "Supply approved founder photography"] },
  analytics: { title: "Analytics Dashboard", eyebrow: "Measurement", description: "Consent-aware measurement architecture with no fabricated audience metrics.", cards: [
    { label: "GA4", value: "Not configured", note: "Measurement ID requires approval", tone: "blocked" },
    { label: "Core events", value: "8", note: "Page, CTA, join, speaking, video, checkout, email, bot", tone: "ready" },
    { label: "Consent", value: "Required", note: "No tracking before opt-in", tone: "ready" },
    { label: "Data truth", value: "Verified only", note: "No fake or placeholder KPIs", tone: "ready" },
  ], queue: ["Approve GA property and stream", "Approve privacy/consent text", "Verify events in staging DebugView"] },
  revenue: { title: "Revenue Dashboard", eyebrow: "Offer engine", description: "Readiness across membership, speaking, sponsorship, and commerce offers.", cards: [
    { label: "Membership tiers", value: "3", note: "Foundation, Builder, Legacy", tone: "staged" },
    { label: "Payment links", value: "0 / 4", note: "Kept disabled", tone: "blocked" },
    { label: "Checkout mode", value: "Test only", note: "Live keys rejected", tone: "ready" },
    { label: "Charges", value: "$0", note: "No charges performed", tone: "ready" },
  ], queue: ["Approve test products and prices", "Test success/cancel/refund journeys", "Approve live activation separately"] },
  crm: { title: "CRM Dashboard", eyebrow: "Relationship pipeline", description: "Validated lead intake and next-action management without inventing pipeline results.", cards: [
    { label: "Stages", value: "7", note: "New through won/lost", tone: "ready" },
    { label: "Source lists", value: "Local", note: "CSV workflow available", tone: "staged" },
    { label: "Data provider", value: "Not selected", note: "Owner decision required", tone: "blocked" },
    { label: "Retention", value: "Pending", note: "Policy approval required", tone: "blocked" },
  ], queue: ["Select CRM data provider", "Approve fields and retention", "Run synthetic staging import", "Configure role access"] },
  email: { title: "Email Dashboard", eyebrow: "Draft-to-send control", description: "Campaign staging, consent, suppression, and owner approval boundaries.", cards: [
    { label: "Gmail", value: "Connected", note: "One active connection", tone: "ready" },
    { label: "Mode", value: "Draft only", note: "No mass sends", tone: "ready" },
    { label: "Suppression", value: "Required", note: "Before campaign sending", tone: "staged" },
    { label: "Sent", value: "0", note: "No emails sent in Phase 2", tone: "ready" },
  ], queue: ["Approve sender identity", "Approve recipients and consent basis", "Verify unsubscribe/suppression", "Approve exact send batch"] },
  youtube: { title: "YouTube Dashboard", eyebrow: "Media engine", description: "Channel assets, publishing packages, metadata, captions, and owner-gated uploads.", cards: [
    { label: "Connection", value: "Active", note: "Composio verified", tone: "ready" },
    { label: "Final Shorts", value: "3", note: "1080×1920 with audio/captions", tone: "ready" },
    { label: "Channel trailer", value: "1", note: "Packaged locally", tone: "ready" },
    { label: "Uploads", value: "0", note: "Publishing locked", tone: "ready" },
  ], queue: ["Approve founder imagery", "Review metadata and thumbnails", "Approve exact channel/visibility", "Use single confirmation-gated upload"] },
  community: { title: "Community Dashboard", eyebrow: "Concrete Nation", description: "Member journey, safety controls, and contribution standards before account launch.", cards: [
    { label: "Journey", value: "5 stages", note: "Connect to Compound", tone: "ready" },
    { label: "Memberships", value: "3 tiers", note: "Pricing staged", tone: "staged" },
    { label: "Auth", value: "Not selected", note: "Provider decision required", tone: "blocked" },
    { label: "Youth safeguards", value: "Legal review", note: "Required before youth data", tone: "blocked" },
  ], queue: ["Approve community rules", "Select auth/data providers", "Complete youth/privacy review", "Test moderation and deletion"] },
  stripe: { title: "Stripe Dashboard", eyebrow: "Payment safety", description: "Test-mode readiness with live-key rejection and separate owner activation gates.", cards: [
    { label: "Connection", value: "Active", note: "Composio connection exists", tone: "ready" },
    { label: "Local links", value: "0 / 4", note: "No active checkout URLs", tone: "blocked" },
    { label: "Adapter", value: "Test only", note: "Dry-run by default", tone: "ready" },
    { label: "Live mode", value: "Blocked", note: "Requires explicit owner approval", tone: "ready" },
  ], queue: ["Approve catalog and prices", "Configure Stripe test IDs", "Verify webhooks/refunds", "Approve production activation separately"] },
};

export function isDashboardView(value: string): value is DashboardView {
  return dashboardViews.includes(value as DashboardView);
}

export function findBot(slug: string) {
  return botCatalog.find((bot) => bot.slug === slug);
}
