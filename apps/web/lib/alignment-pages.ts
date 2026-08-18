import type { PublicPage } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

export const alignmentPages: Record<string, PublicPage> = {
  "concrete-nation": {
    slug: "concrete-nation",
    eyebrow: "The parent community",
    title: "Concrete Nation is where Builders stop building alone.",
    description:
      "A community and action ecosystem connecting accountability, Crews, proof, mentorship, opportunity, service, trusted business discovery, and a clear pathway from personal progress to Legacy.",
    intro:
      "Concrete Nation is not a passive motivation feed and it is not a sovereign government. It is the parent community around Concrete Motivation, Concrete Conversations, and Concrete OS. Members enter with something real to build, a willingness to be accountable, and a responsibility to contribute without exploiting the trust of the room.",
    sections: [
      {
        title: "The member path",
        body:
          "Assessment → Blueprint → Daily Bricks → Proof → Inspection → Passport → Crew accountability → Opportunity → Service → Story → Next Build. The path is designed to keep progress connected instead of scattering tools across unrelated experiences."
      },
      {
        title: "Crews and Captains",
        body:
          "Small accountability teams create a weekly rhythm for promises, proof, misses, recovery, support, service, and next actions. Captains coordinate the standard without becoming therapists, financial advisers, salespeople, or status figures."
      },
      {
        title: "Concrete Passport and proof",
        body:
          "Members can maintain a private-by-default history of Builds, Bricks, outcomes, service, and selected verification. Progress belongs to the Builder; the platform should never require public performance as the price of accountability."
      },
      {
        title: "Concrete Foreman",
        body:
          "A direct, nonjudgmental accountability assistant helps a Builder return to the real Blueprint, simplify the next Brick, inspect misses, and reconnect action to the Six Pillars."
      },
      {
        title: "444 Challenge",
        body:
          "Four commitments across Body, Money, Family, and Purpose for four focused weeks. Money is taught as a building skill inside the Six Pillars—not as a seventh pillar or the identity of the Nation."
      },
      {
        title: "Opportunities and Exchange",
        body:
          "Jobs, training, mentorship, grants, service paths, and trusted member-owned businesses can connect a Build to the real world. No placement, income, funding, or business result is guaranteed."
      },
      {
        title: "Foundation and Concrete Saturday",
        body:
          "Service, valid help events, community impact, and recurring in-person rhythms make Legacy practical. Growth is incomplete if it never becomes useful to another person."
      },
      {
        title: "Community hard lines",
        body:
          "Respect, confidentiality, truth, earned leadership, responsible opportunity, and service are non-negotiable. No harassment, exploitation, predatory selling, fake opportunities, schemes, or unauthorized sharing of private stories."
      }
    ],
    primaryCta: { label: "See the complete system", href: "/inside-the-app" },
    secondaryCta: { label: "Enter Concrete Nation in the app", href: siteConfig.links.app }
  },

  "foundation-challenge": {
    slug: "foundation-challenge",
    eyebrow: "Free 7-Day Experience",
    title: "Seven days to experience the Concrete standard.",
    description:
      "A public introduction to honest assessment, specific action, discipline, boundaries, self-leadership, purpose, and Legacy before a person buys anything.",
    intro:
      "The seven-day challenge is designed to be useful on its own. The website explains every day so a visitor understands the method. The app adds saved progress, authenticated records, reminders, and the ability to continue into deeper Builds.",
    sections: [
      {
        title: "Day 1 — Assess Your Foundation",
        body:
          "Take an honest inventory of habits, relationships, beliefs, and support. List what is holding you up and what is quietly cracking."
      },
      {
        title: "Day 2 — Face the Pressure",
        body:
          "Name the specific pressure instead of carrying a vague weight. Write it in one sentence, then identify what it is costing you."
      },
      {
        title: "Day 3 — Discipline Over Feelings",
        body:
          "Choose one action you will keep regardless of mood. Set a single non-negotiable and a clear time it happens."
      },
      {
        title: "Day 4 — Protect Your Peace",
        body:
          "Identify what repeatedly drains energy, focus, or stability and set one respectful, clear boundary."
      },
      {
        title: "Day 5 — Lead Yourself First",
        body:
          "Practice self-leadership before asking to lead other people. For one day, pay close attention to the promises you make to yourself and whether you keep them."
      },
      {
        title: "Day 6 — Build With Purpose",
        body:
          "Attach the daily work to a reason larger than the moment. Write one sentence explaining who or what the Build is for and keep it visible."
      },
      {
        title: "Day 7 — Commit to Your Legacy",
        body:
          "Choose the habits worth carrying forward, identify who can hold you accountable, and decide how what you build can eventually become useful to somebody else."
      },
      {
        title: "What happens after Day 7",
        body:
          "A Builder can continue into the 30-Day Concrete Reset, create a 30/60/90-day Build, enter Concrete Nation, or simply keep practicing the Bricks that proved useful. There is no requirement to buy a membership to benefit from the public method."
      }
    ],
    primaryCta: { label: "Start the challenge in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Continue to the 30-Day Reset", href: "/concrete-30-day-reset" }
  },

  memberships: {
    slug: "memberships",
    eyebrow: "Concrete Nation memberships",
    title: "Choose the depth of support that matches your Build.",
    description:
      "Foundation $9/month, Builder $19/month, and Legacy $49/month—with yearly options designed as two months free when the live billing system is enabled.",
    intro:
      "Membership pays for depth, saved progress, libraries, community experiences, and development access. It does not buy leadership, guarantee outcomes, or replace the free public method. Secure billing belongs in the authenticated app and must only be presented as live when the payment system is actually production-ready.",
    sections: [
      {
        title: "Foundation — $9/month",
        body:
          "Start the daily habit and finish your first challenge.",
        items: [
          "Daily motivation with the Daily Brick",
          "Seven-Day Foundation Challenge with saved progress",
          "Basic progress tracking",
          "Member newsletter",
          "Selected member resources",
          "Entry-level Concrete Nation community access"
        ]
      },
      {
        title: "Builder — $19/month",
        body:
          "Go deeper with the full challenge library and live development experiences.",
        items: [
          "Everything in Foundation",
          "Full challenge library",
          "Deeper worksheets",
          "Audio motivation library",
          "Expanded community participation",
          "Monthly live or recorded development session",
          "Progress insights",
          "Early content access"
        ]
      },
      {
        title: "Legacy — $49/month",
        body:
          "Leadership, Legacy work, and the ambassador/community-leadership pathway.",
        items: [
          "Everything in Builder",
          "Complete resource library",
          "Premium challenges and workshops",
          "Priority access to events",
          "Advanced leadership and legacy content",
          "Recognition opportunities",
          "Ambassador and community-leadership pathway",
          "Premium downloads"
        ]
      },
      {
        title: "Billing and cancellation",
        body:
          "The app is designed to use secure Stripe checkout and a member billing-management path when production billing is enabled. Members should be able to understand the price before checkout and manage or cancel billing without hidden friction."
      },
      {
        title: "What is free before membership",
        body:
          "A visitor can understand the Six Pillars, read the public system guide, use public Daily Brick content, learn the seven challenge days, explore the movement, and decide whether deeper saved/accountable experiences are useful before paying."
      },
      {
        title: "Membership truth",
        body:
          "No tier guarantees income, employment, health, healing, relationships, business results, leadership status, or personal transformation. Concrete provides structure, content, tools, relationships, and opportunities; the Builder remains responsible for action and decisions."
      }
    ],
    primaryCta: { label: "Open membership in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See how Concrete Nation works", href: "/concrete-nation" }
  },

  resources: {
    slug: "resources",
    eyebrow: "Builder library",
    title: "Use the website to understand. Use the app to practice and save.",
    description:
      "A connected library of public explanations, challenges, worksheets, videos, conversations, programs, and private member tools.",
    intro:
      "Resources are organized by what a Builder is trying to do, not by how much content Concrete can publish. The public website should help somebody act before asking them to buy. The app adds persistence, personalization, private records, community, and member-only depth.",
    sections: [
      {
        title: "Understand the framework",
        body:
          "Start Here, the Concrete Story, Six Pillars, Concrete Nation, Concrete OS, the Founding Charter, community guidelines, and the full Inside the App guide explain what the system believes and how the pieces connect."
      },
      {
        title: "Take action",
        body:
          "Daily Brick, Foundation Assessment, 7-Day Challenge, 30-Day Reset, Builds and Blueprints, Inspection and Recovery, and the 444 Challenge turn ideas into measurable commitments."
      },
      {
        title: "Document progress",
        body:
          "Proof of Build and the Concrete Passport explain how promises, evidence, outcomes, reflections, service, and selected verification can form a private history of growth."
      },
      {
        title: "Build with people",
        body:
          "Concrete Nation, Crews, Captains, Foreman, Concrete Conversations, community events, and Founding 100 pathways connect personal responsibility to trustworthy relationships."
      },
      {
        title: "Connect to opportunity",
        body:
          "Opportunities, Concrete Exchange, speaking/programs, partnerships, community impact, and Concrete Foundation connect the internal Build to work, business, learning, service, and community."
      }
    ],
    primaryCta: { label: "Explore the complete system", href: "/inside-the-app" },
    secondaryCta: { label: "Open the app", href: siteConfig.links.app }
  }
};

export const alignmentSlugs = Object.keys(alignmentPages);
