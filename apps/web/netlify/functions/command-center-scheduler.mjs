export const config = { schedule: "*/5 * * * *" };

export default async function handler() {
  const origin = process.env.COMMAND_SCHEDULER_ORIGIN;
  const secret = process.env.COMMAND_CRON_SECRET;
  if (!origin || !secret || secret.length < 32) return new Response(null, { status: 204 });

  const url = new URL("/api/command-center/cron", origin);
  if (url.protocol !== "https:" || url.username || url.password) throw new Error("Invalid scheduler origin.");
  const response = await fetch(url, {
    method: "POST",
    redirect: "error",
    headers: { Authorization: `Bearer ${secret}` },
    signal: AbortSignal.timeout(14000)
  });
  if (!response.ok) throw new Error(`Command Center scheduler returned HTTP ${response.status}.`);
  return new Response(null, { status: 204 });
}
