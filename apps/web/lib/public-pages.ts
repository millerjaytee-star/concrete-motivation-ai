export type PublicPage = {
  slug: string;
  eyebrow: string;
  title: string;
  description: string;
  intro: string;
  sections: Array<{ title: string; body: string; items?: string[] }>;
  primaryCta: { label: string; href: string };
  secondaryCta?: { label: string; href: string };
};

export const publicPages: Record<string, PublicPage> = {
  "our-story": {
    slug: "our-story",
    eyebrow: "Why the movement exists",
    title: "Pressure became purpose.",
    description: "The responsibility-first story behind Concrete Motivation, Concrete Conversations, and Concrete Nation.",
    intro: "Concrete Motivation was built for people who carry real responsibility while still learning, healing, rebuilding, and becoming. The brand does not promise a life without pressure. It teaches people how to use pressure without letting pressure use them.",
    sections: [
      { title: "The responsibility", body: "Jaytee Miller did not start with a polished speaker story. He started with family, leadership, loss, work, mistakes, responsibility, and the daily demand to keep moving while other people were depending on him." },
      { title: "The lesson", body: "Pressure reveals the foundation. Discipline strengthens it. Honest relationships protect it. Purpose determines what gets built next." },
      { title: "The movement", body: "Concrete Motivation earns attention. Concrete Conversations earns trust. Concrete Nation turns trust into accountability, mentorship, shared resources, referrals, collaboration, and measurable action." },
      { title: "The promise", body: "You do not have to build alone. Members are expected to take ownership, contribute value, respect the process, and help other people move forward." }
    ],
    primaryCta: { label: "Join the movement", href: "/join" },
    secondaryCta: { label: "See who we serve", href: "/who-we-serve" }
  },
  "who-we-serve": {
    slug: "who-we-serve",
    eyebrow: "Built for real responsibility",
    title: "For people ready to stop building alone.",
    description: "Concrete Motivation serves people with meaningful goals who are willing to act, accept accountability, and contribute.",
    intro: "Our audience is connected by mindset more than age, title, or income. They are carrying responsibility, pursuing growth, and looking for structure and trustworthy people—not empty hype.",
    sections: [
      { title: "Parents, guardians, and providers", body: "Support for people balancing family responsibility, identity, finances, relationships, and personal growth." },
      { title: "Students and young adults", body: "Direction, discipline, communication, career readiness, confidence, and leadership before the title." },
      { title: "Athletes and coaches", body: "Mental resilience, team culture, identity beyond performance, accountability, recovery, and transferable leadership." },
      { title: "Frontline workers and emerging leaders", body: "Practical tools for standards, difficult conversations, career development, emotional control, and responsible influence." },
      { title: "Entrepreneurs, creators, and builders", body: "Structure, execution, relationships, visibility, customer focus, and the discipline to build while life is still happening." },
      { title: "Educators, mentors, and community leaders", body: "Programs and conversations that strengthen connection, responsibility, opportunity, and long-term community capacity." }
    ],
    primaryCta: { label: "Find your path", href: "/join" },
    secondaryCta: { label: "Explore speaking", href: "/speaking" }
  },
  "concrete-conversations": {
    slug: "concrete-conversations",
    eyebrow: "The trust engine",
    title: "Real stories. Real lessons. Real impact.",
    description: "A video and podcast platform for honest conversations about what success, leadership, healing, and responsibility actually cost.",
    intro: "Concrete Conversations brings together parents, athletes, educators, entrepreneurs, frontline leaders, and community builders. Guests are not presented as perfect. They are invited to explain what pressure taught them and what other people can apply.",
    sections: [
      { title: "Core topics", body: "Every conversation must leave the audience with something usable.", items: ["Leadership before the title", "The provider’s pressure", "More than an athlete", "Building a business while building yourself", "Family, faith, healing, and legacy", "What community owes community"] },
      { title: "Guest standard", body: "Guests should bring lived experience, humility, specific lessons, and a willingness to discuss both results and costs. No manufactured success stories." },
      { title: "Audience journey", body: "A viewer discovers a message, trusts the conversation, takes a practical challenge, and enters Concrete Nation for accountability and connection." }
    ],
    primaryCta: { label: "Watch on YouTube", href: "https://youtube.com/@concretemotivation444" },
    secondaryCta: { label: "Become a guest", href: "/join" }
  },
  "concrete-nation": {
    slug: "concrete-nation",
    eyebrow: "The action engine",
    title: "Success grows faster when people build together.",
    description: "Concrete Nation connects accountability, mentorship, relationships, practical resources, referrals, and opportunity.",
    intro: "Concrete Nation is not a passive motivation feed. Members enter with a goal, define the pressure point, commit to action, contribute something useful, and document progress honestly.",
    sections: [
      { title: "The member journey", body: "Connect → Clarify → Commit → Contribute → Compound." },
      { title: "Community experiences", body: "The first version centers on structured accountability and useful relationships.", items: ["Accountability circles", "Mentor and skill exchange", "Career and business referrals", "30-day challenges", "Member-led workshops", "Live Concrete Conversations", "Resource library", "Opportunities to lead and contribute"] },
      { title: "Community standard", body: "Respect, confidentiality, truth, responsibility, contribution, and follow-through. No harassment, exploitation, fake opportunities, or predatory selling." },
      { title: "What success means", body: "Completed goals, healthier habits, stronger relationships, useful introductions, jobs, collaborations, businesses, leadership growth, and service to others." }
    ],
    primaryCta: { label: "Become a founding member", href: "/memberships" },
    secondaryCta: { label: "Read community expectations", href: "/support" }
  },
  videos: {
    slug: "videos",
    eyebrow: "Concrete Motivation media",
    title: "Messages built to move people.",
    description: "Long-form videos, Shorts, conversations, challenges, and practical lessons connected to the Concrete Method.",
    intro: "The video hub is organized around pressure, ownership, emotional release, clear choices, disciplined building, relationships, proof, and legacy. Every piece should lead to a next action—not endless consumption.",
    sections: [
      { title: "Start here", body: "Welcome to Concrete Motivation; Built Under Pressure; Discipline After Motivation Leaves; Stop Building Alone." },
      { title: "Official playlists", body: "Content will be organized for discovery and transformation.", items: ["The Concrete Method", "Concrete Conversations", "Built Under Pressure", "Discipline Over Feelings", "Leadership Before the Title", "Fathers, Families, and Legacy", "More Than an Athlete", "Business, Ownership, and Opportunity", "Concrete Nation Challenges", "Concrete Motivation Shorts"] },
      { title: "Publishing standard", body: "Every long-form video creates useful Shorts, a discussion question, a pinned action step, and a clear path into the website, app, or community." }
    ],
    primaryCta: { label: "Open YouTube", href: "https://youtube.com/@concretemotivation444" },
    secondaryCta: { label: "Join Concrete Nation", href: "/concrete-nation" }
  },
  speaking: {
    slug: "speaking",
    eyebrow: "Keynotes, workshops, and facilitated conversations",
    title: "Pressure can become disciplined action.",
    description: "Programs for schools, athletics, workplaces, government, churches, conferences, and community organizations.",
    intro: "Concrete Motivation programs combine a credible personal story with practical frameworks, facilitated reflection, clear commitments, and follow-up options. The goal is not temporary excitement. The goal is responsible action.",
    sections: [
      { title: "Leadership Before the Title", body: "A practical program about standards, communication, ownership, emotional control, influence, and becoming trustworthy before receiving authority." },
      { title: "Built Under Pressure", body: "A keynote or workshop about facing setbacks, separating feelings from decisions, rebuilding identity, and creating a repeatable discipline." },
      { title: "More Than an Athlete", body: "Identity, team culture, pressure, transition, responsibility, mental resilience, and life beyond performance." },
      { title: "The Provider’s Pressure", body: "A responsible conversation about family expectations, work, finances, emotional weight, relationships, and asking for support before isolation becomes damage." },
      { title: "Formats", body: "Programs are scoped around the audience and desired outcomes.", items: ["20–60 minute keynote", "60–120 minute workshop", "Panel or moderated Concrete Conversation", "Multi-session leadership series", "30-day action challenge", "Custom organizational program"] }
    ],
    primaryCta: { label: "Request a speaking conversation", href: "/join" },
    secondaryCta: { label: "See the audience", href: "/who-we-serve" }
  },
  memberships: {
    slug: "memberships",
    eyebrow: "Concrete Nation memberships",
    title: "Choose the support level that matches your build.",
    description: "Foundation, Builder, and Legacy memberships are designed around access, accountability, contribution, and opportunity.",
    intro: "Pricing remains in Stripe Test mode until the full independent payment system passes staging acceptance. This page explains the intended structure without taking live payments.",
    sections: [
      { title: "Foundation — $9 monthly / $90 yearly", body: "Core community access, selected challenges, member resources, announcements, and foundational accountability tools." },
      { title: "Builder — $19 monthly / $190 yearly", body: "Foundation access plus deeper accountability experiences, workshops, progress tools, and expanded member opportunities." },
      { title: "Legacy — $49 monthly / $490 yearly", body: "Builder access plus premium leadership experiences, priority opportunities, selected small-group sessions, and deeper contribution pathways." },
      { title: "Membership truth", body: "No membership guarantees income, employment, healing, business results, or personal transformation. The platform provides structure, content, relationships, and opportunities; members remain responsible for action and decisions." }
    ],
    primaryCta: { label: "Join the waitlist", href: "/join" },
    secondaryCta: { label: "Explore Concrete Nation", href: "/concrete-nation" }
  },
  shop: {
    slug: "shop",
    eyebrow: "Wear the standard",
    title: "Merchandise connected to the message.",
    description: "Purpose-driven apparel and accessories designed to reinforce discipline, identity, and belonging.",
    intro: "The independent store is being rebuilt with secure Stripe checkout, order records, inventory controls, shipping logic, and honest product photography. Live sales remain disabled until testing is complete.",
    sections: [
      { title: "Launch catalog", body: "Initial products planned for the independent store.", items: ["Concrete Motivation T-shirt — $28", "Concrete Motivation Hoodie — $55", "Concrete Motivation Cap — $25", "Concrete Motivation Bottle — $24", "Concrete Motivation Wristband — $8"] },
      { title: "Product standard", body: "Every product must have accurate images, sizing, materials, fulfillment time, return rules, inventory status, and total price before purchase." },
      { title: "Why merchandise matters", body: "The product is not a substitute for the work. It is a visible reminder of the standard: build from pressure, lead with purpose, and move with discipline." }
    ],
    primaryCta: { label: "Join the launch list", href: "/join" },
    secondaryCta: { label: "Read refunds and returns", href: "/refunds" }
  },
  join: {
    slug: "join",
    eyebrow: "Take the next step",
    title: "Tell us what you are building.",
    description: "One clear entry point for community, speaking, partnerships, sponsorships, media, guests, and general support.",
    intro: "The production inquiry form and Gmail/CRM workflow will be connected in the next backend milestone. Until then, this page defines the exact intake paths and information required.",
    sections: [
      { title: "Concrete Nation", body: "Share your 90-day goal, current pressure point, support needed, and what you can contribute." },
      { title: "Speaking and programs", body: "Provide organization, audience, date range, location, desired outcome, format, budget range, and decision timeline." },
      { title: "Concrete Conversations guest", body: "Provide your story, useful lessons, relevant links, proposed topic, and why the audience can apply it." },
      { title: "Partnership, sponsor, or media", body: "Explain the organization, proposed value exchange, audience fit, deliverables, timeline, and responsible contact." },
      { title: "General support", body: "Describe the issue without including passwords, payment card data, Social Security numbers, medical records, or other unnecessary sensitive information." }
    ],
    primaryCta: { label: "Email the team", href: "mailto:concretemotivation444@gmail.com" },
    secondaryCta: { label: "Review support guidance", href: "/support" }
  },
  privacy: {
    slug: "privacy",
    eyebrow: "Legal and trust",
    title: "Privacy policy foundation.",
    description: "How Concrete Motivation intends to collect, use, protect, and delete personal information.",
    intro: "This is a launch-stage policy foundation and must receive legal review before broad production launch or processing sensitive information.",
    sections: [
      { title: "Information collected", body: "Account details, contact and inquiry information, community content, progress data, transaction references, support communications, device and analytics data, and preferences when those systems are enabled." },
      { title: "How information is used", body: "To operate accounts, memberships, orders, community features, support, communications, safety, analytics, fraud prevention, legal compliance, and product improvement." },
      { title: "Sharing", body: "Information may be processed by necessary service providers such as hosting, authentication, database, payment, email, analytics, and support vendors under appropriate agreements. Personal information is not sold as a business model." },
      { title: "Rights and choices", body: "Users may request access, correction, deletion, export, communication preferences, or account closure, subject to identity verification and legal retention obligations." },
      { title: "Children", body: "The general platform is not designed to collect personal information directly from children without appropriate organizational and guardian controls. Youth programs require separate safeguards and agreements." }
    ],
    primaryCta: { label: "Contact privacy support", href: "/support" }
  },
  terms: {
    slug: "terms",
    eyebrow: "Legal and trust",
    title: "Terms of use foundation.",
    description: "The standards for using Concrete Motivation content, community, services, memberships, and future applications.",
    intro: "These terms are a production foundation and require legal review before live memberships, commerce, or broad community launch.",
    sections: [
      { title: "Responsible use", body: "Users must follow applicable law, respect other people, protect account credentials, provide accurate information, and avoid harassment, fraud, exploitation, impersonation, scraping, malware, or abuse." },
      { title: "No guaranteed outcomes", body: "Content, coaching tools, community access, introductions, and programs do not guarantee money, employment, health, relationships, legal results, business performance, or personal transformation." },
      { title: "Content and intellectual property", body: "Concrete Motivation content and brand assets remain protected. Users keep ownership of their original community content while granting the limited permissions necessary to operate the service." },
      { title: "Community enforcement", body: "Access may be limited or removed for safety, fraud, harassment, exploitation, repeated disruption, nonpayment, or material violation of community standards." },
      { title: "Professional advice", body: "The platform does not replace qualified medical, mental-health, legal, tax, financial, or emergency services." }
    ],
    primaryCta: { label: "Contact support", href: "/support" }
  },
  refunds: {
    slug: "refunds",
    eyebrow: "Purchases and memberships",
    title: "Refund and return policy foundation.",
    description: "Clear expectations for memberships, programs, events, digital products, and merchandise.",
    intro: "Live payments remain disabled during independent platform development. Final terms must match the actual product, fulfillment system, event contract, and applicable law before launch.",
    sections: [
      { title: "Memberships", body: "Cancellation should stop future renewal while preserving access through the paid period unless misuse requires earlier termination. Refund eligibility must be clearly disclosed before checkout." },
      { title: "Merchandise", body: "Return windows, condition requirements, exclusions, shipping responsibility, damaged-item procedures, and processing times must appear on product and checkout surfaces." },
      { title: "Events and programs", body: "The proposal or registration page must state cancellation deadlines, transfer options, deposits, nonrefundable costs, rescheduling terms, and force-majeure handling." },
      { title: "Digital products", body: "Refund treatment depends on whether access or download has begun and must comply with applicable consumer law." }
    ],
    primaryCta: { label: "Request support", href: "/support" }
  },
  accessibility: {
    slug: "accessibility",
    eyebrow: "Access for more people",
    title: "Accessibility commitment.",
    description: "Concrete Motivation is being built to support keyboard use, readable contrast, semantic structure, reduced motion, captions, and clear language.",
    intro: "Accessibility is an ongoing product requirement, not a one-time statement. We will test automated checks and real user journeys as the platform grows.",
    sections: [
      { title: "Current foundation", body: "Semantic headings, skip navigation, visible keyboard focus, responsive layouts, reduced-motion support, descriptive link text, and high-contrast visual design." },
      { title: "Media", body: "Published videos should include accurate captions. Important audio-only content should include transcripts or equivalent text when feasible." },
      { title: "Known limitations", body: "Some future community, payment, and interactive app features are still under development and will require dedicated accessibility testing before production launch." },
      { title: "Report a barrier", body: "Tell us the page, device, browser, assistive technology if relevant, expected behavior, and what prevented access. Do not include unnecessary sensitive information." }
    ],
    primaryCta: { label: "Report an accessibility issue", href: "/support" }
  },
  support: {
    slug: "support",
    eyebrow: "Help and safety",
    title: "Support built around clarity and responsibility.",
    description: "Get help with accounts, memberships, orders, community safety, accessibility, privacy, partnerships, and technical issues.",
    intro: "The dedicated support form and ticket workflow will be connected in a later backend milestone. For now, use the official email and include enough detail to investigate without exposing sensitive credentials or records.",
    sections: [
      { title: "Account and technical support", body: "Include the page or feature, device, browser, time of issue, expected behavior, actual behavior, and a screenshot with sensitive information removed." },
      { title: "Billing and orders", body: "Include the account email, order or payment reference, date, amount, and issue. Never email full card numbers, bank credentials, or passwords." },
      { title: "Community safety", body: "Report the account, post, message, date, concern, and supporting context. Immediate danger should be directed to local emergency services rather than the platform." },
      { title: "Response standard", body: "Requests should be acknowledged, categorized, protected, investigated, and resolved or escalated with a clear record." }
    ],
    primaryCta: { label: "Email support", href: "mailto:concretemotivation444@gmail.com" },
    secondaryCta: { label: "Return home", href: "/" }
  }
};

export const publicSlugs = Object.keys(publicPages);
