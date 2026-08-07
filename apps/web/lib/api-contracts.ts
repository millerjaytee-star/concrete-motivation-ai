const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export type ValidationResult<T> = { ok: true; value: T } | { ok: false; errors: string[] };

export function cleanText(value: unknown, maxLength = 2000): string {
  return typeof value === "string" ? value.replace(/\s+/g, " ").trim().slice(0, maxLength) : "";
}

export function validateBotRun(body: unknown): ValidationResult<{ bot: string; goal: string; detail: string }> {
  const data = body && typeof body === "object" ? body as Record<string, unknown> : {};
  const bot = cleanText(data.bot, 80);
  const goal = cleanText(data.goal, 600);
  const detail = cleanText(data.detail, 600);
  const errors = [];
  if (!bot) errors.push("Bot is required.");
  if (!goal) errors.push("Goal is required.");
  return errors.length ? { ok: false, errors } : { ok: true, value: { bot, goal, detail } };
}

export function validateLead(body: unknown): ValidationResult<{ name: string; email: string; path: string; goal: string; consent: boolean }> {
  const data = body && typeof body === "object" ? body as Record<string, unknown> : {};
  const name = cleanText(data.name, 120);
  const email = cleanText(data.email, 254).toLowerCase();
  const path = cleanText(data.path, 80);
  const goal = cleanText(data.goal, 1200);
  const consent = data.consent === true;
  const errors = [];
  if (name.length < 2) errors.push("Name is required.");
  if (!emailPattern.test(email)) errors.push("A valid email is required.");
  if (!path) errors.push("An inquiry path is required.");
  if (!goal) errors.push("A goal is required.");
  if (!consent) errors.push("Consent is required.");
  return errors.length ? { ok: false, errors } : { ok: true, value: { name, email, path, goal, consent } };
}

export function validateCheckout(body: unknown): ValidationResult<{ priceId: string; customerEmail?: string }> {
  const data = body && typeof body === "object" ? body as Record<string, unknown> : {};
  const priceId = cleanText(data.priceId, 120);
  const customerEmail = cleanText(data.customerEmail, 254).toLowerCase();
  const errors = [];
  if (!priceId.startsWith("price_")) errors.push("A Stripe price ID is required.");
  if (customerEmail && !emailPattern.test(customerEmail)) errors.push("Customer email is invalid.");
  return errors.length ? { ok: false, errors } : { ok: true, value: { priceId, ...(customerEmail ? { customerEmail } : {}) } };
}
