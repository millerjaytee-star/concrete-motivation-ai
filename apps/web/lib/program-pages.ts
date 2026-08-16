import type { PublicPage } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

export const programPages: Record<string, PublicPage> = {
  "start-here": {
    slug: "start-here", eyebrow: "Your first brick", title: "Start building here.",
    description: "A simple path from discovering Concrete Motivation to taking your first measurable action.",
    intro: "You do not need an account to understand the movement. Learn the story, name the pressure, choose a Brick, and decide what support you need next.",
    sections: [
      { title: "1. Know the story", body: "Learn why Concrete Motivation exists and what Built Under Pressure. Proven Through Purpose. means in practice." },
      { title: "2. Name the pressure", body: "Identify the area asking for stronger structure: leadership, discipline, faith, family, growth, or legacy." },
      { title: "3. Lay one Brick", body: "Use the Daily Brick to turn a large goal into one specific action you can complete today." },
      { title: "4. Build the foundation", body: "Complete the free seven-day Foundation Challenge before deciding whether a deeper program or membership fits." }
    ],
    primaryCta: { label: "See today's Daily Brick", href: "/daily-brick" },
    secondaryCta: { label: "Read the story", href: "/our-story" }
  },
  "about-jaytee": {
    slug: "about-jaytee", eyebrow: "Founder", title: "Jaytee Miller",
    description: "A leadership and family-centered story built around responsibility, resilience, discipline, and service.",
    intro: "Concrete Motivation is grounded in lived responsibility, not a polished success story. The message is for people building while life is still happening.",
    sections: [
      { title: "Leadership", body: "Years of operational leadership and team development shaped a practical view of standards, accountability, communication, and growth." },
      { title: "Family and legacy", body: "Family responsibility is central to the message: success has to become something useful for the people and communities that come after us." },
      { title: "Pressure into purpose", body: "Setbacks, loss, responsibility, and rebuilding helped form the Concrete Method: face reality, own the next decision, build structure, prove it through action, and share what works." }
    ],
    primaryCta: { label: "Read the Concrete story", href: "/our-story" },
    secondaryCta: { label: "Book Jaytee", href: "/speaking" }
  },
  "daily-brick": {
    slug: "daily-brick", eyebrow: "One Brick Every Day", title: "Turn pressure into one action today.",
    description: "The Daily Brick is Concrete Nation's smallest repeatable unit of progress.",
    intro: "A Brick is not a motivational quote. It is a specific action you can prove you completed. Small enough to execute today. Meaningful enough to move the Build.",
    sections: [
      { title: "Choose it", body: "Name one action connected to the Build that matters most right now." },
      { title: "Make it provable", body: "Define what done means before you begin. No vague promises." },
      { title: "Inspect it", body: "At the end of the day record what happened, what got in the way, and the Recovery Brick if you missed." }
    ],
    primaryCta: { label: "Open the member app", href: siteConfig.links.app },
    secondaryCta: { label: "Try the 7-Day Challenge", href: "/foundation-challenge" }
  },
  "foundation-challenge": {
    slug: "foundation-challenge", eyebrow: "Free 7-Day Experience", title: "Seven days. Seven kept promises.",
    description: "A free introduction to the Concrete standard before a longer program or membership.",
    intro: "The Foundation Challenge gives visitors a low-friction way to experience the system: one Brick daily, honest inspection, and recovery instead of quitting after a miss.",
    sections: [
      { title: "The goal", body: "Prove that consistency can start before confidence is perfect." },
      { title: "The rhythm", body: "Choose a meaningful Build, lay one Daily Brick, record proof, and inspect the result each day for seven days." },
      { title: "The bridge", body: "After seven days, continue into the 30-Day Concrete Reset or join Concrete Nation for ongoing accountability." }
    ],
    primaryCta: { label: "Start in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See the 30-Day Reset", href: "/concrete-30-day-reset" }
  },
  "concrete-30-day-reset": {
    slug: "concrete-30-day-reset", eyebrow: "Flagship public program", title: "The 30-Day Concrete Reset",
    description: "A structured month for turning one meaningful goal into daily action, weekly inspection, recovery, and a 90-day next blueprint.",
    intro: "The Reset is designed to move people from inspiration into evidence. Participants enter with one Build and leave with a repeatable standard, documented progress, and the next 90 days mapped.",
    sections: [
      { title: "Week 1 — Foundation", body: "Clarify what you are building, why it matters, and the standards that will support it." },
      { title: "Week 2 — Discipline", body: "Build the routines, environment, boundaries, and Daily Bricks that make action repeatable." },
      { title: "Week 3 — Pressure & Recovery", body: "Learn to inspect misses without shame, identify what broke down, and lay a Recovery Brick instead of quitting." },
      { title: "Week 4 — Purpose & Leadership", body: "Turn personal progress into clearer leadership, service, and a 90-day continuation plan." },
      { title: "Founding Edition — $29", body: "The founding digital edition is priced at $29. Checkout must use the secure app/Stripe path when live; no payment information is collected on this public page." }
    ],
    primaryCta: { label: "Open the Reset in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Join the Founding 100", href: "/founding-100" }
  },
  "founding-100": {
    slug: "founding-100", eyebrow: "The inaugural cohort", title: "THE FOUNDING 100",
    description: "100 Builders. One Foundation. One Brick Every Day.",
    intro: "The first hundred are not followers. They are Builders who help prove the culture through kept promises, honest recovery, service, feedback, and visible participation in a Crew.",
    sections: [
      { title: "Set the standard", body: "What the first hundred normalize becomes the Nation's default: weekly Inspection, honest recovery, service, and proof over performance." },
      { title: "The commitments", body: "Complete the Foundation Assessment, choose one meaningful Build, lay Daily Bricks, join a Crew, attend weekly Inspection, participate in the inaugural challenge, contribute service, and give honest feedback." },
      { title: "Founding status is earned", body: "A Founding 100 mark and early member number are recognition for action. Founding status cannot be bought later and is never pay-to-win." },
      { title: "Who should apply", body: "People serious about career, business, money, family, health, purpose, discipline, service, or rebuilding after real pressure." }
    ],
    primaryCta: { label: "Apply in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Read the Founding Charter", href: "/concrete-nation-charter" }
  },
  "founding-100-captains": {
    slug: "founding-100-captains", eyebrow: "Earned leadership", title: "Founding Captains",
    description: "A target of 10 trained Captains to lead the inaugural Crews with consistency, empathy, confidentiality, and nonjudgmental accountability.",
    intro: "Captains are not therapists, financial advisers, or status holders. They run a focused weekly Inspection, protect confidentiality, help Builders recover after misses, and escalate safety issues to staff.",
    sections: [
      { title: "The standard", body: "Show up consistently, listen before correcting, protect private Crew information, and hold the standard without shaming people." },
      { title: "The Inspection", body: "Run a focused 30–45 minute weekly rhythm: promises, proof, misses, recovery, next Bricks, service, and help." },
      { title: "Hard lines", body: "No diagnosing, therapy, legal/medical/financial advice, selling to the Crew, recruiting into schemes, or sharing private stories without written consent." }
    ],
    primaryCta: { label: "Captain pathway in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Founding 100", href: "/founding-100" }
  },
  "concrete-nation-charter": {
    slug: "concrete-nation-charter", eyebrow: "Charter v2026.1", title: "The Concrete Nation Founding Charter",
    description: "The behavior, safety, dignity, truth, service, and leadership standards the Nation is expected to protect.",
    intro: "The Nation is a community and business ecosystem — not a sovereign government. Membership creates no legal citizenship or governmental rights. The Charter exists to protect people and the culture.",
    sections: [
      { title: "One Brick Every Day", body: "The core behavior is a single kept promise laid daily. Not a perfect day. One brick." },
      { title: "Action over performance", body: "We measure kept promises and useful progress, not follower counts, highlight reels, or how good a post sounded." },
      { title: "Dignity and confidentiality", body: "No mockery, contempt, harassment, discrimination, or unauthorized sharing of private stories, photos, documents, or Proof of Build." },
      { title: "Earned leadership and service", body: "Ranks are earned through consistency and service. Leadership is never sold. Progress that never reaches another person is incomplete." },
      { title: "No exploitation", body: "No pressure selling inside Crews, no schemes, no borrowing from members, no using the Nation as a private lead list." }
    ],
    primaryCta: { label: "Join Concrete Nation", href: "/founding-100" },
    secondaryCta: { label: "Captain standards", href: "/founding-100-captains" }
  },
  programs: {
    slug: "programs", eyebrow: "Concrete Method in action", title: "Programs built for real change.",
    description: "Public programs for individuals, youth, schools, employers, churches, nonprofits, teams, and community organizations.",
    intro: "One methodology can be delivered in different environments without becoming seven unrelated businesses: Pressure → Structure → Action → Proof → Leadership → Service.",
    sections: [
      { title: "30-Day Concrete Reset", body: "The repeatable public program for individuals and cohorts." },
      { title: "Leadership sessions", body: "Workshops and facilitated programs built around accountability, communication, resilience, culture, and leadership before the title." },
      { title: "Youth and community cohorts", body: "Structured challenges and workshops focused on direction, confidence, workforce readiness, discipline, and service." },
      { title: "Concrete Conversations", body: "Moderated conversations that turn lived experience into transferable lessons and next actions." }
    ],
    primaryCta: { label: "Explore the 30-Day Reset", href: "/concrete-30-day-reset" },
    secondaryCta: { label: "Book a program", href: "/speaking" }
  },
  catalog: {
    slug: "catalog", eyebrow: "Official 2026 catalog", title: "Membership + merch + programs",
    description: "A clear public view of the active Concrete Motivation offer stack.",
    intro: "Public pricing should be transparent. Secure checkout remains in the app/Stripe flow; this website never asks visitors to enter card data into an unverified form.",
    sections: [
      { title: "Memberships", body: "Foundation — $9/month or $90/year. Builder — $19/month or $190/year. Legacy — $49/month or $490/year." },
      { title: "Merchandise", body: "T-shirt — $28. Hoodie — $55. Cap — $25. Bottle — $24. Wristband — $8." },
      { title: "Digital program", body: "30-Day Concrete Reset Founding Edition — $29." },
      { title: "Speaking and team programs", body: "Organization programs are scoped to audience, format, location, outcomes, and requirements rather than sold through a generic one-click checkout." }
    ],
    primaryCta: { label: "Shop", href: "/shop" },
    secondaryCta: { label: "Memberships", href: "/memberships" }
  },
  "community-impact": {
    slug: "community-impact", eyebrow: "Proof over hype", title: "Build people. Measure what changes.",
    description: "Concrete Nation is being designed to document participation, progress, service, and outcomes without inventing impact claims.",
    intro: "The movement will publish real evidence only after it exists and consent allows it. Until then, the public standard is transparent targets and measurable signals — not manufactured success stories.",
    sections: [
      { title: "What we measure", body: "Assessment completion, first-Brick rate, 7-day activity, challenge completion, Crew Inspection participation, recovery after misses, Build progress, service, opportunities used, and partner contributions delivered." },
      { title: "Service is part of the system", body: "Every cohort is expected to contribute useful help beyond itself. Progress that never reaches another person is incomplete." }
    ],
    primaryCta: { label: "See the Founding 100", href: "/founding-100" },
    secondaryCta: { label: "Partner with Concrete", href: "/join" }
  },
  resources: {
    slug: "resources", eyebrow: "Builder resources", title: "Tools for the next Brick.",
    description: "A growing public library of challenges, worksheets, videos, conversations, and practical tools.",
    intro: "Resources should help a visitor act before asking them to buy. Start with the Daily Brick and Foundation Challenge, then move into deeper programs when useful.",
    sections: [
      { title: "Free", body: "Daily Brick, seven-day Foundation Challenge, selected videos, Concrete Conversations, and public guides." },
      { title: "Programs", body: "30-Day Concrete Reset, leadership workshops, organization sessions, and cohort experiences." }
    ],
    primaryCta: { label: "Daily Brick", href: "/daily-brick" },
    secondaryCta: { label: "Watch", href: "/videos" }
  },
  app: {
    slug: "app", eyebrow: "Member experience", title: "Take the work with you.",
    description: "The Concrete Nation app is where Builders track Bricks, programs, progress, membership, and private community experiences.",
    intro: "The public website explains the movement. The app delivers authenticated member tools and private experiences.",
    sections: [
      { title: "What stays public", body: "Story, programs, pricing, merch, movement standards, videos, speaking, and ways to join." },
      { title: "What belongs in the app", body: "Saved progress, assessments, tracked challenges, private community, member content, account management, purchase history, and personal profile tools." }
    ],
    primaryCta: { label: "Open the app", href: siteConfig.links.app },
    secondaryCta: { label: "Start here first", href: "/start-here" }
  }
};

export const programSlugs = Object.keys(programPages);
