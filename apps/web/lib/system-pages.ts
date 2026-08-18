import type { PublicPage } from "@/lib/public-pages";
import { siteConfig } from "@/lib/site-config";

export const systemPages: Record<string, PublicPage> = {
  "inside-the-app": {
    slug: "inside-the-app",
    eyebrow: "Website + app, one system",
    title: "Understand the entire Concrete system before you sign in.",
    description:
      "The website explains the full methodology, standards, programs, and member tools in public. The app is where Builders privately do the work and save their progress.",
    intro:
      "Concrete is designed as one connected ecosystem. The website should always be the deeper public reference: what each tool is, why it exists, how it connects to the Six Pillars, what members can expect, and what remains private. The app then turns those ideas into authenticated action, records, accountability, and personal progress.",
    sections: [
      {
        title: "The full loop",
        body:
          "Assessment → Blueprint → Daily Commitments → Bricks → Proof → Inspection → Passport → Community Accountability → Opportunity → Service → Story → Next Build. Every major member tool belongs somewhere in this loop."
      },
      {
        title: "What the website does",
        body:
          "The website is the public library and front door. It explains the mission, Six Pillars, Concrete OS, programs, Founding 100, Crews, Passport, Foreman, 444 Challenge, Exchange, service model, opportunities, pricing, speaking, merchandise, policies, and the standards behind each experience."
      },
      {
        title: "What the app does",
        body:
          "The app is the private workspace. Builders can complete assessments, create a 30/60/90-day Build, edit a Blueprint, lay and recover Bricks, submit Inspections, view a private Passport, use Foreman, participate in challenges and Crews, record service, browse opportunities, manage membership, and keep personal records."
      },
      {
        title: "What stays private",
        body:
          "Personal assessment answers, Build details, private reflections, proof, Passport history, Crew information, account records, orders, support tickets, notifications, and other member-specific information remain inside authenticated systems. The public website explains the feature without publishing a member’s private data."
      },
      {
        title: "The governing standard",
        body:
          "Technology never becomes a seventh pillar. Every tool must strengthen Foundation, Discipline, Resilience, Purpose, Leadership, or Legacy. Money, AI, membership, commerce, and data are supporting systems—not the identity of Concrete."
      }
    ],
    primaryCta: { label: "Explore Concrete OS", href: "/concrete-os" },
    secondaryCta: { label: "Open the app", href: siteConfig.links.app }
  },

  assessment: {
    slug: "assessment",
    eyebrow: "Concrete OS · Foundation",
    title: "The Foundation Assessment",
    description:
      "A transparent starting point for identifying where pressure is landing and which foundation needs attention first.",
    intro:
      "The assessment is not a diagnosis, personality label, or AI judgment. It is a structured self-review that helps a Builder name current conditions before choosing what to build next. The goal is clarity, not a score to impress other people.",
    sections: [
      {
        title: "What it measures",
        body:
          "The app can organize current-condition scores across practical life foundations so a Builder can see where structure is strong, where pressure is exposing a gap, and which area deserves the next focused Build."
      },
      {
        title: "How the score should be read",
        body:
          "Scores are versioned explanations of stored behavior and self-reported conditions. They are not clinical, financial, legal, or moral judgments and should never be treated as a ranking of human worth."
      },
      {
        title: "What happens next",
        body:
          "Assessment results should lead to a decision: choose one 30, 60, or 90-day Build, define what success means, and create a Blueprint small enough to execute under real-life pressure."
      },
      {
        title: "Pillar connection",
        body:
          "Foundation comes first because pressure reveals what is already supporting the Builder. Discipline, Resilience, Purpose, Leadership, and Legacy become stronger when the starting condition is honest."
      }
    ],
    primaryCta: { label: "Take the assessment in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See Builds and Blueprints", href: "/build-blueprint" }
  },

  "build-blueprint": {
    slug: "build-blueprint",
    eyebrow: "Concrete OS · Structure",
    title: "Builds and Blueprints turn intention into a plan.",
    description:
      "A Build is a meaningful 30/60/90-day objective. A Blueprint is the editable structure that makes the objective executable.",
    intro:
      "Concrete does not ask a Builder to change everything at once. One meaningful Build creates focus. The Blueprint turns that focus into milestones, commitments, evidence, support, recovery plans, and a definition of done.",
    sections: [
      {
        title: "The Build",
        body:
          "A Build should be important enough to matter and specific enough to inspect. Examples can include career, family, money habits, health routines, leadership, education, business execution, service, or rebuilding after a difficult season."
      },
      {
        title: "The Blueprint",
        body:
          "The Blueprint is editable because life changes. It can capture the objective, reason, milestones, constraints, support needed, measurable commitments, proof expectations, and the recovery plan for predictable pressure."
      },
      {
        title: "One Build at a time",
        body:
          "The system favors focus over overload. A Builder may care about many areas of life, but the active Build should make the next responsible action obvious instead of creating ten competing priorities."
      },
      {
        title: "Inspection before expansion",
        body:
          "A Blueprint is not successful because it looks organized. It is successful when Bricks are completed, evidence accumulates, Inspections reveal useful truth, and the plan gets adjusted without abandoning the standard."
      }
    ],
    primaryCta: { label: "Open my Build in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Understand Daily Bricks", href: "/daily-brick" }
  },

  "proof-of-build": {
    slug: "proof-of-build",
    eyebrow: "Concrete OS · Evidence",
    title: "Proof of Build makes progress more than a feeling.",
    description:
      "A privacy-controlled record of promises, actions, evidence, verification, outcomes, and reflection.",
    intro:
      "Concrete values proof over performance. Proof does not mean public exposure. It means a Builder can look back at what was promised, what was done, what evidence exists, what changed, and what still needs work.",
    sections: [
      {
        title: "Promise",
        body:
          "Define the Brick or milestone before completing it so the standard cannot be rewritten after the fact."
      },
      {
        title: "Action and evidence",
        body:
          "Record what actually happened. Evidence can be appropriate documentation, completion records, notes, or other proof controlled by the member and suited to the Build."
      },
      {
        title: "Verification without surveillance",
        body:
          "Concrete should verify only what is necessary and appropriate. Proof is member-controlled, privacy-aware, and never an excuse for invasive tracking or public humiliation."
      },
      {
        title: "Outcome and reflection",
        body:
          "The final record should capture what changed and what the Builder learned. A miss can still produce useful proof when the member records the breakdown and completes a Recovery Brick."
      }
    ],
    primaryCta: { label: "Track proof in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See the Concrete Passport", href: "/concrete-passport" }
  },

  "concrete-passport": {
    slug: "concrete-passport",
    eyebrow: "Concrete OS · History",
    title: "The Concrete Passport is a private history of what you built.",
    description:
      "A member-approved record of Builds, Bricks, outcomes, service, verification, and growth over time.",
    intro:
      "The Passport is not a social popularity profile. Its purpose is to help a Builder see credible progress across seasons and, when the member chooses, share selected evidence of consistency, outcomes, leadership, or service.",
    sections: [
      {
        title: "Private by default",
        body:
          "A member controls what belongs in the Passport and what, if anything, is shared. Private growth history should never automatically become public content."
      },
      {
        title: "What can belong in it",
        body:
          "Completed Builds, meaningful Bricks, documented outcomes, verified milestones, valid service/help events, reflections, and other records that show what was actually built."
      },
      {
        title: "Concrete Life Score",
        body:
          "Where a score is shown, it should explain stored behavior transparently. It is not an AI opinion, a moral grade, or a secret ranking system."
      },
      {
        title: "People Helped",
        body:
          "Service is measured through valid help events rather than likes, followers, or self-awarded popularity. Legacy means the Build eventually becomes useful to somebody else."
      }
    ],
    primaryCta: { label: "View my Passport in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Explore service and Legacy", href: "/concrete-foundation" }
  },

  "concrete-foreman": {
    slug: "concrete-foreman",
    eyebrow: "Concrete OS · Accountability",
    title: "Concrete Foreman helps the Builder return to the Blueprint.",
    description:
      "A direct, nonjudgmental accountability assistant grounded in the member’s real Build, commitments, and progress.",
    intro:
      "Foreman is not the boss of the Builder and it does not replace human judgment. Its job is to help a member clarify the next Brick, inspect a miss, simplify an overloaded plan, and reconnect action to the Blueprint and Six Pillars.",
    sections: [
      {
        title: "Grounded in the real Build",
        body:
          "Useful accountability starts with the Builder’s actual objective, commitments, deadlines, proof, and recent Inspections rather than generic motivational advice."
      },
      {
        title: "Direct without shame",
        body:
          "Foreman should name inconsistencies clearly while preserving dignity. A missed Brick triggers inspection and recovery, not demolition of the whole Build."
      },
      {
        title: "Not professional advice",
        body:
          "Foreman does not replace medical, mental-health, legal, financial, emergency, or other qualified professional services. The assistant must stay inside the product’s defined accountability role."
      },
      {
        title: "Human accountability still matters",
        body:
          "Crews, Captains, trusted relationships, mentors, and professional support remain essential. AI can help organize and reflect; it should not become the entire community."
      }
    ],
    primaryCta: { label: "Use Foreman in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Learn about Crews", href: "/crews" }
  },

  "444-challenge": {
    slug: "444-challenge",
    eyebrow: "Concrete OS · Four focused weeks",
    title: "The 444 Challenge builds four commitments across four foundations for four weeks.",
    description:
      "A focused accountability challenge across Body, Money, Family, and Purpose without turning money into a seventh pillar.",
    intro:
      "The 444 Challenge is a structure for practicing balanced responsibility. Money is included as a life skill and building method, but the Six Pillars remain the governing framework for the entire Concrete system.",
    sections: [
      {
        title: "Body",
        body:
          "Choose a sustainable commitment that supports energy, recovery, movement, nutrition, sleep, or another appropriate health behavior without turning the challenge into medical treatment."
      },
      {
        title: "Money",
        body:
          "Choose a measurable financial behavior such as tracking spending, building a buffer, reducing avoidable debt, learning a core concept, increasing income responsibly, or making a planned savings contribution."
      },
      {
        title: "Family",
        body:
          "Choose a commitment that improves presence, communication, responsibility, partnership, parenting, household stability, or another meaningful relationship behavior."
      },
      {
        title: "Purpose",
        body:
          "Choose a commitment tied to the work, learning, service, faith, leadership, or long-term reason that gives the other habits direction."
      },
      {
        title: "Four weeks of proof",
        body:
          "The challenge is not won by a perfect streak. Builders inspect misses, lay Recovery Bricks, and finish with evidence about which commitments should continue beyond the four weeks."
      }
    ],
    primaryCta: { label: "Open challenges in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Start with the free 7-Day Challenge", href: "/foundation-challenge" }
  },

  crews: {
    slug: "crews",
    eyebrow: "Concrete Nation · Accountability",
    title: "Crews make the Build relational without making it performative.",
    description:
      "Small accountability teams centered on weekly Inspection, confidentiality, recovery, useful help, and the next Brick.",
    intro:
      "A Crew is designed to keep Builders from disappearing when pressure rises. Members do not need to perform success for one another. The standard is honest progress, respectful accountability, useful help, and protection of private stories.",
    sections: [
      {
        title: "Weekly Inspection",
        body:
          "A focused rhythm can review promises, proof, misses, recovery, next Bricks, service, and needed help without turning the meeting into therapy or a sales room."
      },
      {
        title: "Captain role",
        body:
          "Captains coordinate the rhythm, protect standards, listen before correcting, help Builders return after misses, and escalate genuine safety concerns through the proper channel."
      },
      {
        title: "Hard boundaries",
        body:
          "No diagnosing, therapy, legal/medical/financial advice, pressure selling, recruitment schemes, borrowing from members, harassment, or sharing private stories without permission."
      },
      {
        title: "What good accountability feels like",
        body:
          "Clear enough to challenge avoidance, humane enough to allow recovery, and practical enough that each Builder leaves knowing the next responsible action."
      }
    ],
    primaryCta: { label: "Enter Concrete Nation in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Read Captain standards", href: "/founding-100-captains" }
  },

  opportunities: {
    slug: "opportunities",
    eyebrow: "Concrete Nation · Opportunity",
    title: "Opportunity should connect the Build to the real world.",
    description:
      "Jobs, training, mentorship, grants, service, and other useful paths organized around what members are actually building.",
    intro:
      "Concrete Nation should not promise outcomes it cannot control. The opportunity layer exists to surface legitimate next steps and useful connections while the Builder remains responsible for qualifications, applications, decisions, and follow-through.",
    sections: [
      {
        title: "Career and jobs",
        body:
          "Members can discover roles and pathways connected to skills, experience, location, and the Build they are pursuing rather than receiving generic motivation to ‘work harder.’"
      },
      {
        title: "Training and mentorship",
        body:
          "Courses, certifications, mentors, workshops, and learning opportunities can help close a specific gap identified in the Blueprint."
      },
      {
        title: "Grants and resources",
        body:
          "Business, education, community, and service opportunities should be presented with eligibility, source, deadlines, and limitations whenever that information is available."
      },
      {
        title: "No guaranteed placement",
        body:
          "Concrete can organize and connect opportunities; it cannot guarantee employment, funding, acceptance, or income. Trust depends on stating that clearly."
      }
    ],
    primaryCta: { label: "Browse opportunities in the app", href: siteConfig.links.app },
    secondaryCta: { label: "Explore Concrete Nation", href: "/concrete-nation" }
  },

  "concrete-exchange": {
    slug: "concrete-exchange",
    eyebrow: "Concrete Nation · Economic trust",
    title: "Concrete Exchange helps members discover trusted member-owned businesses.",
    description:
      "A searchable member-business directory designed around useful introductions, standards, and service—not popularity or pay-to-win status.",
    intro:
      "The Exchange is an economic-support layer inside the Nation. Its purpose is to make trustworthy businesses easier to discover while protecting members from predatory selling and keeping leadership status separate from what somebody can afford to buy.",
    sections: [
      {
        title: "Directory before marketplace",
        body:
          "The first responsibility is accurate discovery: what the business does, where it operates, who it serves, and how a member can request an introduction or learn more."
      },
      {
        title: "Built Concrete Certified",
        body:
          "A certification, when used, is human-approved and standards-based. It is never automatically granted because a business paid a fee."
      },
      {
        title: "No Crew selling pressure",
        body:
          "Crews and accountability relationships are not private lead lists. Business discovery must stay separate from coercion, schemes, or exploitation of trust."
      },
      {
        title: "Reputation through service",
        body:
          "Trust should grow from accurate information, reliable behavior, documented service, and responsible participation—not follower counts or self-awarded badges."
      }
    ],
    primaryCta: { label: "Browse the Exchange in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See the Nation standards", href: "/concrete-nation-charter" }
  },

  "concrete-foundation": {
    slug: "concrete-foundation",
    eyebrow: "Concrete Nation · Legacy",
    title: "Concrete Foundation turns personal progress into useful service.",
    description:
      "The service and community-impact layer of Concrete Nation, built around valid help events, family, community, and measurable contribution.",
    intro:
      "Legacy is incomplete if the Build only benefits the Builder. The Foundation layer creates ways to turn skills, progress, relationships, and resources outward while documenting impact honestly and protecting the dignity of the people being served.",
    sections: [
      {
        title: "People Helped",
        body:
          "The metric should come from valid help events—not likes, impressions, self-awarded popularity, or exaggerated impact claims."
      },
      {
        title: "Service connected to the Build",
        body:
          "A Builder can contribute time, knowledge, mentoring, referrals, practical support, community work, or other meaningful help that fits their capacity and the Nation’s standards."
      },
      {
        title: "Proof without exploitation",
        body:
          "Community impact must be documented responsibly. People receiving help are not marketing props, and private hardship should never be exposed merely to create content."
      },
      {
        title: "Legacy as a behavior",
        body:
          "Concrete defines Legacy as what becomes useful after the Builder has learned, recovered, grown, and built enough structure to help another person move forward."
      }
    ],
    primaryCta: { label: "Record service in the app", href: siteConfig.links.app },
    secondaryCta: { label: "See Community Impact", href: "/community-impact" }
  },

  "concrete-saturday": {
    slug: "concrete-saturday",
    eyebrow: "Concrete Nation · Community rhythm",
    title: "Concrete Saturday brings the system into the room.",
    description:
      "A recurring adult community experience combining movement, Inspection, learning, service, family, and opportunity.",
    intro:
      "Concrete Saturday is designed as a repeatable community rhythm rather than a one-time motivational event. The point is to connect physical presence, honest reflection, useful learning, relationships, opportunity, and service in one experience that sends people back to real life with a next Brick.",
    sections: [
      {
        title: "Movement",
        body:
          "An accessible movement or wellness component can reinforce energy, recovery, and discipline without turning the event into medical or athletic treatment."
      },
      {
        title: "Inspection and learning",
        body:
          "Builders review the week, learn a practical concept, identify the pressure point, and leave with a specific commitment instead of only consuming a speech."
      },
      {
        title: "Family and community",
        body:
          "The event can create appropriate space for relationships, family, mentorship, intergenerational connection, and community trust."
      },
      {
        title: "Opportunity and service",
        body:
          "Useful introductions, legitimate opportunities, community needs, and service actions connect individual growth to a wider economic and civic ecosystem."
      }
    ],
    primaryCta: { label: "Join Concrete Nation", href: "/founding-100" },
    secondaryCta: { label: "Open the app", href: siteConfig.links.app }
  }
};

export const systemSlugs = Object.keys(systemPages);
