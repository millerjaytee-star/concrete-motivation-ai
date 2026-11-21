export const commandAreas = [
  { id: "executive", name: "Executive Headquarters", icon: "grid", group: "Overview", description: "Today’s priorities, decisions and operating activity.", stages: ["Priority", "In progress", "Complete", "Draft"] },
  { id: "agents", name: "AI Agent Team", icon: "spark", group: "Overview", description: "Send a task to a specialist and review the result.", stages: [] },
  { id: "email", name: "Email & Communications", icon: "mail", group: "Business", description: "Review inbox activity, prepare replies and track follow-ups.", stages: ["Needs reply", "Draft", "Review", "Follow-up"] },
  { id: "youtube", name: "YouTube Studio", icon: "video", group: "Production", description: "Take videos and Shorts from research to performance review.", stages: ["Idea", "Research", "Script", "Production", "Editing", "Review", "Approval", "Upload", "Analytics", "Improvement"] },
  { id: "social", name: "Social Media Studio", icon: "share", group: "Production", description: "Plan social campaigns, captions and repurposed content.", stages: ["Idea", "Draft", "Review", "Approval"] },
  { id: "podcast", name: "Concrete Conversations Podcast", icon: "mic", group: "Production", description: "Manage guest research, interviews and episode production.", stages: ["Guest research", "Invitation draft", "Guest confirmed", "Episode prep", "Draft", "Scheduled", "Recording", "Editing", "Review", "Distribution prep"] },
  { id: "partnerships", name: "Speaking & Partnerships", icon: "link", group: "Business", description: "Track speaking, sponsorship and partnership opportunities.", stages: ["Prospect", "Qualified", "Proposal draft", "Negotiation", "Closed"] },
  { id: "nation", name: "Concrete Nation App", icon: "phone", group: "Business", description: "Open the existing release center and track engineering blockers.", stages: ["Release blocker", "Defect", "In progress", "Ready for verification", "Resolved"] },
  { id: "curriculum", name: "Curriculum & Education", icon: "book", group: "Production", description: "Use the Concrete Motivation framework to teach financial decision-making.", stages: ["Planning", "In review", "Completed"] },
  { id: "revenue", name: "Memberships & Revenue", icon: "chart", group: "Business", description: "Manage offers and projections and open the existing owner commerce dashboard.", stages: ["Current offer", "Proposed offer", "Projection", "Member joined", "Member at risk", "Member cancelled", "Engagement draft", "Draft"] },
  { id: "crm", name: "CRM & Outreach", icon: "people", group: "Business", description: "Track contact history, opportunities and follow-up plans.", stages: ["New lead", "Qualified", "Outreach draft", "Reply received", "Draft", "Follow-up", "Closed"] },
  { id: "calendar", name: "Calendar & Scheduling", icon: "calendar", group: "Business", description: "View upcoming meetings and plan tentative events.", stages: ["Proposed", "Needs approval", "Scheduled"] },
  { id: "library", name: "Content Library", icon: "folder", group: "Production", description: "Find approved themes, working drafts and production assets.", stages: ["Approved theme", "Draft", "Review", "Reference"] },
  { id: "analytics", name: "Analytics & Reporting", icon: "chart", group: "System", description: "Record analysis and link to the underlying evidence.", stages: ["Draft", "Verified evidence linked"] },
  { id: "integrations", name: "Integrations & Permissions", icon: "link", group: "System", description: "Authorize provider accounts and verify read access.", stages: [] },
  { id: "health", name: "System Health & Automation Logs", icon: "pulse", group: "System", description: "Manage workflow schedules, outcomes and the owner approval queue.", stages: [] }
] as const;

export const approvalActions = [
  ["external_communication", "Send external communication"],
  ["publish_content", "Publish public content"],
  ["spend_money", "Spend money"],
  ["change_pricing", "Change subscription pricing"],
  ["production_database_change", "Change production data"],
  ["delete_records", "Delete records"],
  ["change_permissions", "Change ownership or permissions"],
  ["production_deploy", "Deploy a high-risk production change"],
  ["app_release_submission", "Submit an app for public release"],
  ["sign_agreement", "Sign an agreement"]
] as const;

export const commandWorkflows = {
  "daily-briefing": "Daily executive briefing",
  "content-draft": "Content draft preparation",
  "podcast-confirmation": "Podcast guest confirmation",
  "outreach-reply": "Outreach reply follow-up",
  "membership-event": "Membership event follow-up",
  "engineering-monitor": "Engineering health review"
} as const;

export const recordTemplates: Partial<Record<(typeof commandAreas)[number]["id"], string>> = {
  email: "Recipient or thread reference:\nContext and deadline:\nDraft reply:\nFollow-up date:",
  youtube: "Audience and search intent:\nTitle and thumbnail direction:\nScript hook and outline:\nProduction assets and rights:\nUpload checklist and review notes:",
  podcast: "Guest and contact reference:\nEpisode promise and relevant pillar:\nResearch and evidence:\nInterview questions:\nRecording, transcription and distribution checklist:\nSponsor or rights notes:",
  crm: "Contact and organization:\nOffer or relationship goal:\nLast interaction and original thread:\nNext step, owner and due date:\nCheck for existing outreach before any send:",
  revenue: "Offer and audience:\nExisting price and source, if verified:\nAssumptions for any projection:\nConversion/retention evidence:"
};
