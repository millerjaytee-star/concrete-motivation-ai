export const siteConfig = {
  name: "Concrete Motivation",
  phrase: "Build from pressure. Lead with purpose. Move with discipline.",
  promise: "You do not have to build alone.",
  description:
    "A movement that turns pressure into purpose through practical motivation, honest conversations, disciplined action, and a community built for shared success.",
  links: {
    website:
      process.env.NEXT_PUBLIC_SITE_URL ??
      "https://concretemotivation.com",
    youtube:
      process.env.NEXT_PUBLIC_YOUTUBE_URL ??
      "https://youtube.com/@concretemotivation444",
    app:
      process.env.NEXT_PUBLIC_APP_URL ??
      "https://app.concretemotivation.com",
    booking: process.env.NEXT_PUBLIC_BOOKING_URL ?? "/speaking",
    instagram:
      process.env.NEXT_PUBLIC_INSTAGRAM_URL ??
      "https://www.instagram.com/concretemotivation444/",
    tiktok: process.env.NEXT_PUBLIC_TIKTOK_URL ?? "#",
    facebook: process.env.NEXT_PUBLIC_FACEBOOK_URL ?? "#"
  },
  pillars: ["Foundation", "Discipline", "Resilience", "Purpose", "Leadership", "Legacy"],
  method: [
    ["Face It", "Tell the truth about the pressure."],
    ["Own It", "Take responsibility for the next decision."],
    ["Release It", "Let go of what keeps you trapped."],
    ["Choose It", "Set your direction on purpose."],
    ["Build It", "Create standards and repeatable habits."],
    ["Connect It", "Build relationships that strengthen the work."],
    ["Prove It", "Let consistent results build confidence."],
    ["Share It", "Turn progress into opportunity for others."]
  ] as const
} as const;
