# Concrete Motivation Bot Team

The Command Center organizes eight specialists around one voice: motivational, disciplined, direct, faith-aware, real-life, family-centered, comeback-minded, and leadership-driven. Version 6 runs offline by default, can use OpenAI when explicitly configured, can save every response to the local content vault, can turn one theme into a weekly content calendar, and now includes a static public website foundation.

| Bot | Best used for | Response structure |
| --- | --- | --- |
| Brand Architect | Positioning, audience, voice, and offers | Message, audience, tone, offer, action |
| Motivational Speech | Talks, keynotes, and team messages | Title, hook, speech, engagement, call-to-action |
| Concrete Conversations Podcast | Episode development | Title, promise, intro, segments, questions, clips, outro |
| Social Media Content | Reels, captions, and repurposing | Hooks, script, caption, hashtags, reuse ideas |
| Athlete Outreach | Coach, school, and athlete introductions | Audience, angle, draft, follow-up, offer |
| Business Growth | Revenue and partnership experiments | Opportunity, package, pricing, sales, partners |
| Operations | Weekly execution and repeatable work | Priorities, checklist, SOP, owner, deadlines |
| Faith & Mindset | Grounded reflection and renewal | Theme, reflection, principle, action, affirmation |

## Personalization layer

Every bot response now includes `Concrete Motivation Angle`, a short section connecting the output back to Jaytee Miller, Concrete Motivation, Concrete Conversations, the core audience, and a practical next action. The optional follow-up question can tailor that angle to a specific audience, tone, platform, or personal theme.

## Provider layer

The offline provider keeps the reliable local output available with no account or API key. The OpenAI provider can create richer, custom drafts when `CONCRETE_AI_PROVIDER=openai` and `OPENAI_API_KEY` are set. If OpenAI is unavailable, the runner falls back to the offline provider for that response.

## Content vault

Every bot maps to a local `outputs/` folder so useful responses can become reusable Markdown assets. Speeches, podcast episodes, social posts, outreach messages, business growth plans, operations plans, faith and mindset drafts, and brand work each have their own folder. Menu option `9` shows the 10 most recent saved files.

## Weekly calendar engine

Menu option `10` creates a 7-day execution calendar for one theme. It covers mindset reels, podcast clips, athlete/youth messages, fatherhood/faith/leadership posts, Concrete Conversations pushes, behind-the-scenes stories, and Sunday reset challenges. Calendar files save to `outputs/content_calendars` and appear in recent outputs.

## Website foundation

The static site in `website/` presents Concrete Motivation as a speaking, podcast, youth/athlete development, and leadership platform. It includes booking and podcast calls to action, speaking topics, programs, early testimonial placeholders, and a static contact form placeholder.

## Choosing a bot

Choose the specialist closest to the deliverable you need, then make the goal specific. “Create a seven-minute talk for high school athletes rebuilding after a losing season” will produce a more focused result than “motivate athletes.” Run the same goal through another bot when you want a complementary asset—for example, Speech first and Social Media second.

## Content responsibility

Version 6 provides a strong working draft, not a claim of professional, legal, financial, pastoral, or medical advice. Review names, facts, prices, scripture wording, and promises before publishing or sending the output.
