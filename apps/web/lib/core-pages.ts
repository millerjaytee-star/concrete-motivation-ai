import type { PublicPage } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

export const corePages: Record<string, PublicPage> = {
  "concrete-os": {
    slug: "concrete-os",
    eyebrow: "The accountable action layer",
    title: "Concrete OS is what happens after motivation.",
    description:
      "A closed-loop building system that moves a person from pressure and assessment to action, proof, accountability, opportunity, service, story, and the next Build.",
    intro:
      "Concrete OS is the measurable action layer of Concrete Motivation and Concrete Nation. It does not replace the Six Pillars; it operationalizes them. The system exists so a person can move from ‘I need to change’ to a documented pattern of responsible action without pretending progress is always linear.",
    sections: [
      {
        title: "1. Assessment",
        body:
          "Name the current condition honestly. Identify where pressure is landing and which foundation deserves focused attention before choosing a Build."
      },
      {
        title: "2. Blueprint",
        body:
          "Choose one meaningful 30/60/90-day Build and create an editable plan with milestones, commitments, support, proof expectations, and recovery strategies."
      },
      {
        title: "3. Daily commitments and Bricks",
        body:
          "Turn the Blueprint into measurable actions small enough to complete under real pressure. One Brick every day is the operating behavior."
      },
      {
        title: "4. Proof and Inspection",
        body:
          "Document what actually happened. Review promises, outcomes, pressure, misses, recovery, and the next action instead of relying on memory or mood."
      },
      {
        title: "5. Passport and accountability",
        body:
          "Build a private history of progress while Crews, Captains, and Foreman provide accountability without turning growth into public performance."
      },
      {
        title: "6. Opportunity and service",
        body:
          "Connect the Build to jobs, learning, mentorship, business discovery, community resources, legitimate opportunities, and meaningful ways to help another person."
      },
      {
        title: "7. Story and next Build",
        body:
          "Reflect on what was built, share only what is appropriate and consented to, turn the lesson into service, and choose the next structure worth building."
      },
      {
        title: "The full loop",
        body:
          "Assessment → Blueprint → Daily Commitments → Bricks → Proof → Inspection → Passport → Community Accountability → Opportunity → Service → Story → Next Build."
      }
    ],
    primaryCta: { label: "See every app tool", href: "/inside-the-app" },
    secondaryCta: { label: "Open Concrete OS in the app", href: siteConfig.links.app }
  },

  "inspection-recovery": {
    slug: "inspection-recovery",
    eyebrow: "Concrete OS · Resilience",
    title: "Inspection tells the truth. Recovery keeps one miss from becoming demolition.",
    description:
      "A repeatable review of promises, results, pressure, lessons, and the next action—with a Recovery Brick when the plan breaks.",
    intro:
      "Concrete does not confuse accountability with punishment. A Builder should be able to name a miss clearly without rewriting the goal, hiding the result, or deciding the entire Build is ruined. Inspection produces information. Recovery turns that information into the next responsible action.",
    sections: [
      {
        title: "Promises",
        body:
          "What did you say you would do? The original commitment matters because accountability starts with a clear standard."
      },
      {
        title: "Results",
        body:
          "What actually happened? Record the result without exaggerating success or treating a miss as a character verdict."
      },
      {
        title: "Pressure",
        body:
          "What changed, interfered, or exposed a weakness in the Blueprint? Pressure is data when the Builder is willing to inspect it honestly."
      },
      {
        title: "Recovery Brick",
        body:
          "Choose the smallest credible action that re-establishes movement. Recovery is not lowering every standard; it is refusing to let one miss become permanent disengagement."
      },
      {
        title: "Next action",
        body:
          "Finish every Inspection with a specific next Brick, any Blueprint adjustment required, and a clear support request when help is needed."
      }
    ],
    primaryCta: { label: "Inspect my Build in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See Proof of Build", href: "/proof-of-build" }
  },

  "pressure-to-purpose-reset-call": {
    slug: "pressure-to-purpose-reset-call",
    eyebrow: "Work with Jaytee · Individual",
    title: "Pressure-to-Purpose Reset Call",
    description:
      "A focused private working session designed to turn a current pressure point into a practical 30-day action plan.",
    intro:
      "This is not a therapy session or a promise that one conversation fixes a life. The purpose is to clarify the pressure, identify what the person can responsibly control, choose a meaningful Build, and leave with a concrete next-step structure.",
    sections: [
      {
        title: "Who it is for",
        body:
          "Adults carrying a real decision, transition, leadership challenge, rebuilding season, career pressure, family responsibility, discipline gap, or goal that needs structure rather than more vague motivation."
      },
      {
        title: "What the session does",
        body:
          "Clarify the situation, separate controllable actions from noise, choose priorities, identify obstacles, define the first Bricks, and map a realistic 30-day execution rhythm."
      },
      {
        title: "What you leave with",
        body:
          "A written action direction, a first set of commitments, accountability questions, and a clearer connection between the immediate pressure and the larger purpose behind the Build."
      },
      {
        title: "Scope and boundaries",
        body:
          "The session does not replace licensed medical, mental-health, legal, financial, tax, or emergency support. When a pressure point requires qualified professional care, the responsible move is to use it."
      }
    ],
    primaryCta: { label: "Start a booking conversation", href: "/join" },
    secondaryCta: { label: "Explore the 30-Day Reset", href: "/concrete-30-day-reset" }
  },

  "leadership-sessions": {
    slug: "leadership-sessions",
    eyebrow: "Schools · Teams · Organizations",
    title: "Leadership sessions turn the Concrete Method into a room-level experience.",
    description:
      "Practical facilitated sessions for youth, teams, schools, workplaces, churches, nonprofits, and community organizations.",
    intro:
      "Concrete leadership work is designed around clear outcomes rather than one-size-fits-all hype. The same Six Pillars can be translated for different audiences while keeping the core standard: pressure, ownership, disciplined action, communication, recovery, service, and leadership before the title.",
    sections: [
      {
        title: "Leadership Before the Title",
        body:
          "Standards, communication, emotional control, ownership, trust, influence, follow-through, and becoming somebody other people can responsibly follow before authority arrives."
      },
      {
        title: "Built Under Pressure",
        body:
          "A resilience and rebuilding experience focused on facing setbacks honestly, making responsible decisions under pressure, recovering from misses, and turning the next action into evidence."
      },
      {
        title: "Youth and athlete development",
        body:
          "Identity beyond performance, coachability, discipline, confidence, transition, teamwork, education/career direction, responsibility, and transferable leadership."
      },
      {
        title: "Workplace and community teams",
        body:
          "Accountability, culture, difficult conversations, standards, change, resilience, customer/community responsibility, leadership pipelines, and practical follow-up."
      },
      {
        title: "Follow-through",
        body:
          "Where appropriate, a session can connect to a challenge, worksheet, 30-day Build, team commitment, follow-up Inspection, or other structure that makes the event useful after the room clears."
      }
    ],
    primaryCta: { label: "Request a leadership session", href: "/join" },
    secondaryCta: { label: "See all speaking programs", href: "/speaking" }
  },

  partners: {
    slug: "partners",
    eyebrow: "Build with the Nation",
    title: "Partnership should create useful value on both sides.",
    description:
      "A public framework for schools, employers, nonprofits, faith communities, sponsors, mentors, businesses, media, and community organizations interested in working with Concrete.",
    intro:
      "Concrete partnerships should be specific, ethical, and measurable. A logo exchange is not enough. The relationship should make a program stronger, create legitimate opportunity, increase useful service, expand responsible access, or improve what Builders can actually do.",
    sections: [
      {
        title: "Program partners",
        body:
          "Schools, employers, teams, churches, nonprofits, and community organizations can host or co-design programs around leadership, resilience, workforce readiness, family, youth development, and accountability."
      },
      {
        title: "Opportunity partners",
        body:
          "Organizations can contribute legitimate jobs, training, mentorship, internships, grants, education, service opportunities, or other resources that connect to member Builds."
      },
      {
        title: "Business and Exchange partners",
        body:
          "Responsible businesses can support member commerce, vendor relationships, learning, procurement, referrals, and community economic activity without turning the Nation into a lead-harvesting scheme."
      },
      {
        title: "Media and storytelling partners",
        body:
          "Podcasts, platforms, creators, and media organizations can collaborate on useful stories and conversations when consent, accuracy, dignity, and audience value remain more important than attention alone."
      },
      {
        title: "What we measure",
        body:
          "Partnership success should be tied to agreed deliverables and real outputs—participation, completion, opportunity delivered, service, referrals, learning, or other relevant outcomes—not invented impact claims."
      }
    ],
    primaryCta: { label: "Start a partnership conversation", href: "/join" },
    secondaryCta: { label: "See Community Impact", href: "/community-impact" }
  },

  "community-guidelines": {
    slug: "community-guidelines",
    eyebrow: "Concrete Nation · Conduct",
    title: "Build people. Do not exploit them.",
    description:
      "The practical community rules that protect dignity, confidentiality, accountability, opportunity, and earned leadership.",
    intro:
      "Concrete Nation can only become useful if members trust the room. The Charter sets the culture. These guidelines translate that culture into everyday behavior across Crews, messages, events, opportunities, business discovery, stories, and member interactions.",
    sections: [
      {
        title: "Respect and dignity",
        body:
          "No harassment, discrimination, mockery, threats, humiliation, stalking, targeted abuse, or retaliation. Accountability is direct, but dignity is not optional."
      },
      {
        title: "Confidentiality",
        body:
          "Do not share another person’s private story, reflection, proof, document, image, contact information, or Crew conversation without appropriate permission."
      },
      {
        title: "No exploitation",
        body:
          "No pressure selling inside accountability relationships, recruitment schemes, predatory opportunities, borrowing based on member trust, fake jobs, impersonation, fraud, or using the Nation as a private lead list."
      },
      {
        title: "Truth over performance",
        body:
          "Do not manufacture achievements, testimonials, certifications, impact, business results, partnerships, or proof. A miss recorded honestly is more Concrete than a fake win."
      },
      {
        title: "Safety and escalation",
        body:
          "Captains and members are not substitutes for emergency or professional services. Serious safety, abuse, fraud, or policy concerns should be escalated through the appropriate reporting and support channels."
      }
    ],
    primaryCta: { label: "Read the Founding Charter", href: "/concrete-nation-charter" },
    secondaryCta: { label: "Contact support", href: "/support" }
  }
};

export const coreSlugs = Object.keys(corePages);
