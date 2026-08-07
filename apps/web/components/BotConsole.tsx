"use client";

import { useState } from "react";
import { botCatalog } from "@/lib/release-candidate";

type Result = { status?: string; error?: string; bot?: { name: string }; execution?: string };

export function BotConsole() {
  const [result, setResult] = useState<Result | null>(null);
  const [pending, setPending] = useState(false);

  async function stage(formData: FormData) {
    setPending(true);
    setResult(null);
    const response = await fetch("/api/orchestration", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bot: formData.get("bot"), goal: formData.get("goal"), detail: formData.get("detail") }),
    });
    setResult(await response.json());
    setPending(false);
  }

  return (
    <section className="bot-console" aria-labelledby="bot-console-title">
      <div><p className="eyebrow">Local orchestration</p><h2 id="bot-console-title">Stage a bot assignment.</h2><p>Creates a validated dry-run plan. It does not call paid AI, publish, send, deploy, or charge.</p></div>
      <form action={stage}>
        <label htmlFor="bot">Specialist</label>
        <select id="bot" name="bot" required>{botCatalog.map((bot) => <option value={bot.slug} key={bot.slug}>{bot.name}</option>)}</select>
        <label htmlFor="goal">Goal</label>
        <textarea id="goal" name="goal" required maxLength={600} placeholder="Build the next responsible campaign asset" />
        <label htmlFor="detail">Audience or context</label>
        <input id="detail" name="detail" maxLength={600} placeholder="Founders carrying family responsibility" />
        <button className="button button-primary" disabled={pending} type="submit">{pending ? "Staging…" : "Stage assignment"}</button>
        <div className="console-result" aria-live="polite">{result ? (result.error ? `Blocked: ${result.error}` : `${result.status}: ${result.bot?.name}. ${result.execution}`) : "Ready for a dry-run assignment."}</div>
      </form>
    </section>
  );
}
