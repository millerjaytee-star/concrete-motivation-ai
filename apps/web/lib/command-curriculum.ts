import { siteConfig } from "@/lib/site-config";

export const curriculumTracks = {
  children: "Children",
  teenagers: "Teenagers",
  adults: "Adults"
} as const;

export type CurriculumTrack = keyof typeof curriculumTracks;

type Pillar = (typeof siteConfig.pillars)[number];

type Exercise = {
  scenario: string;
  choices: readonly [string, string, string];
  answer: 0 | 1 | 2;
  explanation: string;
};

type Lesson = {
  id: string;
  title: string;
  pillar: Pillar;
  outcome: string;
  introduction: string;
  educator: string;
  brick: string;
  exercises: Record<CurriculumTrack, Exercise>;
};

export const curriculumLessons: readonly Lesson[] = [
  {
    id: "history-of-money",
    title: "History of money",
    pillar: "Foundation",
    outcome: "Explain the jobs money performs and compare ways people record and exchange value.",
    introduction: "People have recorded what they owe on ledgers and exchanged goods using coins, notes and digital balances. These forms have overlapped across places and eras. Money can help people pay, compare prices and carry buying power forward.",
    educator: "Use classroom tokens to exchange imaginary goods. Replace the tokens with a shared ledger and ask learners what still needs to be trusted.",
    brick: "Compare two forms of money and name one thing that makes each usable.",
    exercises: {
      children: {
        scenario: "Sam trades apples at a pretend market. Every stall accepts the same tokens. What problem do the tokens help solve?",
        choices: ["Sellers must like apples before trading.", "Sam can trade with a seller even if that seller does not want apples.", "Every item must cost one token."],
        answer: 1,
        explanation: "An agreed means of payment lets people trade even when they want different things."
      },
      teenagers: {
        scenario: "A seller records all prices in dollars and accepts several forms of payment. Which function do the posted dollar prices demonstrate?",
        choices: ["Store of value", "A guarantee against inflation", "Unit of account"],
        answer: 2,
        explanation: "A unit of account provides a standard way to quote and compare prices."
      },
      adults: {
        scenario: "A community examines historical account ledgers, coins and modern bank balances. What feature helps all three support exchange?",
        choices: ["People trust the rules for recording, transferring or redeeming value.", "Each form must be backed by the same metal.", "Each developed in the same order in every society."],
        answer: 0,
        explanation: "Exchange relies on a shared system people accept and trust. Different societies have used different combinations of credit, recordkeeping and currency."
      }
    }
  },
  {
    id: "earning",
    title: "Earning and value creation",
    pillar: "Purpose",
    outcome: "Explain how solving a problem creates value and distinguish what is earned from what can be kept.",
    introduction: "People earn money by doing work or offering goods and services others value. Gross pay is the amount earned before deductions. A business also needs to account for the costs of doing the work.",
    educator: "Give pairs a fictional customer problem. Have them describe an honest offer and identify which resources the work consumes.",
    brick: "Identify a problem you can help solve and define one way to check whether the solution helps.",
    exercises: {
      children: {
        scenario: "Lee earns three tokens by sorting classroom supplies. Why did the class offer tokens?",
        choices: ["Sorting created more tokens by magic.", "Lee already had a place to keep the tokens.", "Sorting did work that helped the class."],
        answer: 2,
        explanation: "Lee earned the tokens by doing useful work. Creating value means helping meet a need."
      },
      teenagers: {
        scenario: "River earns $15 per hour for four hours. The pay statement shows $8 in deductions. How much is the take-home pay?",
        choices: ["$52", "$60", "$68"],
        answer: 0,
        explanation: "Gross pay is $60. Subtracting $8 in deductions leaves $52 in take-home pay."
      },
      adults: {
        scenario: "A contractor receives $450 for a job and pays $80 in supplies and $40 in travel. What remains before taxes and other business costs?",
        choices: ["$450", "$330", "$370"],
        answer: 1,
        explanation: "The payment is revenue. Subtracting the listed direct costs leaves $330 before taxes and other costs."
      }
    }
  },
  {
    id: "saving",
    title: "Saving",
    pillar: "Discipline",
    outcome: "Choose an achievable savings amount and connect it to a goal over time.",
    introduction: "Saving means setting something aside for later. Write the target, what you have today and when you need it. Break the gap into smaller steps that fit the money you have available.",
    educator: "Set a fictional target and let learners adjust the amount or timeline when a surprise expense arrives. Ask them to explain how they recovered.",
    brick: "Choose a fictional savings target and calculate the next deposit and its date.",
    exercises: {
      children: {
        scenario: "Mika wants a book that costs eight tokens and has saved five. How many more tokens does Mika need?",
        choices: ["3", "5", "13"],
        answer: 0,
        explanation: "Subtract what Mika already has from the goal. Eight minus five is three."
      },
      teenagers: {
        scenario: "You are saving $120 for equipment and start with $30. You have six weeks. What equal weekly amount closes the gap?",
        choices: ["$20", "$30", "$15"],
        answer: 2,
        explanation: "The gap is $90. Divide $90 by six weeks to get $15 per week."
      },
      adults: {
        scenario: "A fictional budget leaves $120 per month after required expenses. A $600 savings goal is due in six months. Which plan meets it within the budget?",
        choices: ["Save $80 monthly and hope the remainder arrives.", "Save $100 monthly and leave $20 for other uses.", "Save $140 monthly without changing expenses."],
        answer: 1,
        explanation: "Six deposits of $100 meet the $600 goal and stay within the modeled $120 available."
      }
    }
  },
  {
    id: "budgeting",
    title: "Budgeting",
    pillar: "Discipline",
    outcome: "Allocate available money across essentials, savings and choices, then adjust when conditions change.",
    introduction: "A budget says where money will go before it gets spent. Make room for daily needs, planned choices and goals. Check whether the money arrives before each payment is due.",
    educator: "Give each group a fictional budget. Introduce a cost increase after the initial plan and ask groups to identify what they changed and why.",
    brick: "Balance a made-up budget, then change one cost and show how the plan still works.",
    exercises: {
      children: {
        scenario: "You have ten tokens. Lunch costs four and you want to save three. How many tokens remain for a game?",
        choices: ["6", "3", "7"],
        answer: 1,
        explanation: "Set aside four for lunch and three for saving. That leaves three tokens for a choice."
      },
      teenagers: {
        scenario: "You plan for $80 income, $25 transportation and $20 savings. Transportation increases to $35 and the savings goal stays fixed. What can you spend on other items?",
        choices: ["$25", "$35", "$45"],
        answer: 0,
        explanation: "$80 minus $35 and $20 leaves $25. Updating the plan makes the tradeoff clear."
      },
      adults: {
        scenario: "The next check arrives Friday, but Wednesday's bills exceed available cash by $50. Which planning action best addresses the timing problem?",
        choices: ["Count Friday's check as available today.", "Ignore the due dates if the month balances.", "Review due dates and arrange a feasible change before Wednesday."],
        answer: 2,
        explanation: "A cash-flow plan compares payment dates with when money is available. A monthly total alone misses an earlier shortfall."
      }
    }
  },
  {
    id: "debt-and-interest",
    title: "Debt and interest",
    pillar: "Resilience",
    outcome: "Compare borrowing costs and explain why the full repayment obligation matters.",
    introduction: "Borrowing lets you use resources now and repay them later. The original amount is the principal. Interest and fees can increase the total you pay, even when each payment looks small.",
    educator: "Put two fictional loan offers on one page. Ask learners to include stated fees and identify assumptions before choosing.",
    brick: "Compare total repayment under two hypothetical borrowing terms.",
    exercises: {
      children: {
        scenario: "You borrow five game tokens and agree that you will repay six. How many tokens are the extra cost of borrowing?",
        choices: ["5", "6", "1"],
        answer: 2,
        explanation: "The extra cost is one token. Repaying what you borrow and any agreed extra uses future resources."
      },
      teenagers: {
        scenario: "A loan of $100 charges 10% simple interest for one year and a $5 fee paid at the end. What is the total repayment?",
        choices: ["$110", "$115", "$105"],
        answer: 1,
        explanation: "The repayment includes the $100 borrowed, $10 interest and $5 fee."
      },
      adults: {
        scenario: "Two fixed-term offers provide the same $1,000. A totals $1,140 across all payments with no fee. B totals $1,100 across payments plus a $60 fee. Which costs less overall?",
        choices: ["A by $20", "B by $40", "The two cost the same"],
        answer: 0,
        explanation: "B totals $1,160 after its fee. A totals $1,140. Comparing total cost with equal amounts and terms helps reveal the effect of fees."
      }
    }
  },
  {
    id: "investing",
    title: "Investing fundamentals",
    pillar: "Legacy",
    outcome: "Distinguish investing from saving and explain diversification as one way to manage exposure.",
    introduction: "Cash savings can keep money within reach for upcoming needs. An investment puts resources at risk for a chance of future gains. Spreading investments across different holdings can reduce dependence on any single one.",
    educator: "Run two simulated portfolios with tokens. Pause at a loss scenario and ask learners how a shorter deadline changes the decision.",
    brick: "Write down a hypothetical goal, its deadline and one reason the deadline matters when comparing risk.",
    exercises: {
      children: {
        scenario: "Ada may need her tokens tomorrow. She can keep them in a jar or trade them for a game card whose value changes. Which keeps the number of tokens known for tomorrow?",
        choices: ["The jar", "The game card", "Either option guarantees the same value"],
        answer: 0,
        explanation: "Keeping the tokens preserves the count. Trading for something that can change in value introduces risk."
      },
      teenagers: {
        scenario: "One imaginary portfolio holds only one company. Another holds many companies across different industries. What is one benefit of the second?",
        choices: ["It turns every loss into a gain.", "It guarantees the price stays flat.", "A problem at one company has less effect on the whole portfolio."],
        answer: 2,
        explanation: "Diversification spreads exposure. Individual company losses matter less to a broadly spread portfolio, which can still decline."
      },
      adults: {
        scenario: "A fictional expense is due in two months. The money set aside covers it today. Which factor should carry the most weight when comparing storage and investing options?",
        choices: ["A friend's biggest recent return", "Whether the amount stays available when the bill is due", "The largest possible return regardless of timing"],
        answer: 1,
        explanation: "For a known near-term obligation, access and exposure to loss matter. An investment can fall in value before the payment date."
      }
    }
  },
  {
    id: "entrepreneurship",
    title: "Entrepreneurship",
    pillar: "Leadership",
    outcome: "Define a customer need, estimate costs and test demand with a limited experiment.",
    introduction: "A business starts with a problem someone values enough to pay you to solve. Track what a sale brings in and what it costs. A small test can help you learn before you spend more.",
    educator: "Give learners an imaginary small business. Ask them to calculate what each sale contributes after direct costs and describe a test they can afford.",
    brick: "Sketch a one-customer test and decide what result would justify a next step.",
    exercises: {
      children: {
        scenario: "It takes two tokens of materials to make one bookmark. You sell one for five tokens. How many tokens remain after paying for the materials?",
        choices: ["2", "3", "5"],
        answer: 1,
        explanation: "Five tokens come in and two go back to materials. Three are left before other costs."
      },
      teenagers: {
        scenario: "A project costs $24 to set up. Each sale brings in $6 and uses $3 of materials. How many sales cover the setup cost?",
        choices: ["4", "6", "8"],
        answer: 2,
        explanation: "Each sale contributes $3 toward the setup. Eight sales cover $24."
      },
      adults: {
        scenario: "A new service idea has no customers yet. Which step produces evidence while limiting the first investment?",
        choices: ["Offer a small pilot to a defined customer group and track willingness to pay and delivery cost.", "Sign a year-long lease before discussing the offer.", "Buy enough equipment for a year's forecast sales."],
        answer: 0,
        explanation: "A limited pilot can reveal whether people value the offer and whether delivering it is viable."
      }
    }
  },
  {
    id: "ownership",
    title: "Ownership",
    pillar: "Leadership",
    outcome: "Describe the rights, upkeep and possible obligations associated with owning an asset.",
    introduction: "Ownership gives you rights such as using, selling or sharing something. It can also bring upkeep, costs and obligations. When ownership is shared, clear terms help everyone understand their role.",
    educator: "Assign buyer, borrower and co-owner roles for an imaginary asset. Ask groups to write who decides, who pays and what happens if someone leaves.",
    brick: "For a fictional asset, list one ownership right, one responsibility and who carries each.",
    exercises: {
      children: {
        scenario: "You borrow a classmate's jump rope for recess. Who decides whether you can give it away?",
        choices: ["Anyone who used it today", "You, because you are holding it", "Its owner"],
        answer: 2,
        explanation: "Borrowing grants a limited right to use something. The owner still controls whether it can be given to someone else."
      },
      teenagers: {
        scenario: "Two teammates buy equipment together. What should they agree on before paying?",
        choices: ["Who can use it, how maintenance is paid, and how either person can leave the arrangement.", "Only the equipment color.", "Who posts a photo first."],
        answer: 0,
        explanation: "Shared ownership works better when the owners agree on use, costs and decisions before a disagreement occurs."
      },
      adults: {
        scenario: "A startup offers you a small ownership stake. Which information best helps you evaluate the offer?",
        choices: ["The company name and logo", "The written terms for voting, dilution, transfer and possible loss", "Only the stated percentage"],
        answer: 1,
        explanation: "The written terms define what the stake gives you and the risks it carries. The percentage is only one input."
      }
    }
  },
  {
    id: "risk",
    title: "Risk",
    pillar: "Resilience",
    outcome: "Identify what could go wrong, estimate the impact and name a way to reduce exposure.",
    introduction: "Before making a money decision, ask what could go wrong, how likely it seems and how serious the impact might be. A backup plan can reduce harm if the expected outcome changes.",
    educator: "Ask groups to identify likelihood and impact for the same fictional risk. Have them propose one mitigation each and explain what risk remains.",
    brick: "Name one realistic downside of a fictional money decision and make a recovery plan.",
    exercises: {
      children: {
        scenario: "It might rain at a pretend outdoor sale. Which choice lowers the chance that the paper signs get ruined?",
        choices: ["Put the signs under cover.", "Make the signs bigger.", "Use brighter colors."],
        answer: 0,
        explanation: "Covering the signs reduces the damage rain could cause."
      },
      teenagers: {
        scenario: "An account message asks for your password and says you must act now. What is the safest next step?",
        choices: ["Send the password before the deadline.", "Open the message's link to see whether it looks official.", "Open the provider's official site or app separately and check there."],
        answer: 2,
        explanation: "An independent trusted channel helps you verify the request without sharing credentials or following a suspicious link."
      },
      adults: {
        scenario: "A fictional business gets 80% of sales from one buyer. Which plan most directly reduces dependence on that buyer?",
        choices: ["Assume the account will renew indefinitely.", "Develop additional customer relationships and plan for a period of reduced sales.", "Increase the current buyer's share of sales."],
        answer: 1,
        explanation: "A broader customer base reduces concentration. A contingency plan prepares for the remaining risk."
      }
    }
  },
  {
    id: "long-term-wealth",
    title: "Long-term wealth building",
    pillar: "Legacy",
    outcome: "Explain compounding and purchasing power using simple assumptions without treating model outcomes as guarantees.",
    introduction: "Consistent contributions build over time. When returns are added to a balance, later returns apply to that new balance. Rising prices can reduce what the balance buys, so the number alone tells only part of the story.",
    educator: "Compare repeated contributions with and without modeled growth. Change the assumed return or inflation rate and ask what the model can and cannot tell you.",
    brick: "Model a repeated contribution and explain one assumption that could change the outcome.",
    exercises: {
      children: {
        scenario: "You put two tokens into a project jar every week for five weeks. How many tokens are in the jar if you start with zero?",
        choices: ["5", "10", "2"],
        answer: 1,
        explanation: "Two tokens each week for five weeks adds up to ten. Repeatable actions can build toward a bigger goal."
      },
      teenagers: {
        scenario: "A pretend account starts at $100 and earns 10% each year for two years with no fees or withdrawals. How much does it have at the end?",
        choices: ["$110", "$120", "$121"],
        answer: 2,
        explanation: "Year one ends at $110. Year two adds $11 because the modeled growth applies to the new balance. Real returns vary."
      },
      adults: {
        scenario: "A balance grows by 3% over a year while the price of a representative basket rises by 5%. What generally happens to the balance's buying power for that basket?",
        choices: ["It falls.", "It rises by 8%.", "It stays the same because the balance increased."],
        answer: 0,
        explanation: "When the basket costs rise faster than the balance, the same balance buys less of that basket than before."
      }
    }
  },
  {
    id: "financial-ethics",
    title: "Ethics and financial decisions",
    pillar: "Purpose",
    outcome: "Recognize conflicts of interest and make a transparent decision under pressure.",
    introduction: "A fair exchange depends on people understanding what they are agreeing to. When a decision could bring you a private benefit, disclose that benefit before the other person decides.",
    educator: "Role-play buyer and seller scenarios. Ask learners to identify who benefits, who bears risk and what the other person needs to know.",
    brick: "Write a plain-language disclosure for a fictional sale that includes the full price and relevant restrictions.",
    exercises: {
      children: {
        scenario: "You accidentally get two tokens back instead of one from a classmate running the pretend store. What shows fairness?",
        choices: ["Keep it a secret.", "Spend the extra token quickly.", "Tell the classmate and return the extra token."],
        answer: 2,
        explanation: "Being honest about a mistake respects the other person and keeps the exchange fair."
      },
      teenagers: {
        scenario: "A brand offers to pay you to recommend a product to classmates. What do classmates need to know before evaluating the recommendation?",
        choices: ["That the brand is paying you and any material limits you know about.", "Only how many followers you have.", "Only that you like the product."],
        answer: 0,
        explanation: "Disclosing a material benefit helps people judge the recommendation and understand the relationship behind it."
      },
      adults: {
        scenario: "You are recommending a supplier and will receive a referral fee if selected. Which step protects the decision process?",
        choices: ["Wait until selection is final to mention it.", "Disclose the arrangement in advance and follow the organization's conflict rules.", "Leave the fee off the records if the supplier appears qualified."],
        answer: 1,
        explanation: "Early disclosure allows the decision-maker to assess the conflict and apply procedures such as independent review."
      }
    }
  }
];

export function curriculumCompletionTitle(lesson: Lesson, track: CurriculumTrack) {
  return `${lesson.title} · ${curriculumTracks[track]}`;
}

export function checkCurriculumAnswer(lesson: Lesson, track: CurriculumTrack, choice: number) {
  const exercise = lesson.exercises[track];
  if (!Number.isInteger(choice) || choice < 0 || choice >= exercise.choices.length) {
    return null;
  }
  return { correct: choice === exercise.answer, explanation: exercise.explanation };
}

export function curriculumProgress(
  track: CurriculumTrack,
  completed: readonly { title: string }[]
) {
  const completedTitles = new Set(completed.map(({ title }) => title));
  return curriculumLessons.filter((lesson) =>
    completedTitles.has(curriculumCompletionTitle(lesson, track))
  ).length;
}
