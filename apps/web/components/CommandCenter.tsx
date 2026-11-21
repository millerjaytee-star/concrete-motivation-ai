"use client";

import Link from "next/link";
import { type FormEvent, type ReactNode, useEffect, useState } from "react";
import { approvalActions, commandAreas, commandWorkflows, recordTemplates } from "@/lib/command-areas";
import type { getCommandState } from "@/lib/command-store";
import type { listCommandIntegrations, readCommandIntegration } from "@/lib/command-integrations";
import { siteConfig } from "@/lib/site-config";
import { CommandCurriculum } from "@/components/CommandCurriculum";

type State = Awaited<ReturnType<typeof getCommandState>>;
type RecordItem = State["records"][number];
type AgentResult = import("@/lib/command-agents").CommandAgentResult;
type Integration = Awaited<ReturnType<typeof listCommandIntegrations>>[number];
type ReadResult = Awaited<ReturnType<typeof readCommandIntegration>>;
type Area = (typeof commandAreas)[number];
type AreaId = Area["id"];
type Agent = { id: string; title: string; responsibility: string; allowedContext: readonly string[] };
type Snapshot = { state: State | null; agents: Agent[]; aiConfigured: boolean };

const icons: Record<string, ReactNode> = {
  grid: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
  spark: <><path d="M12 2 9.4 9.4 2 12l7.4 2.6L12 22l2.6-7.4L22 12l-7.4-2.6L12 2Z"/><path d="M19 3v4m-2-2h4"/></>,
  mail: <><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></>,
  video: <><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/></>,
  share: <><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.7 10.5 6.6-4m-6.6 7 6.6 4"/></>,
  mic: <><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0m-7 7v3m-3 0h6"/></>,
  link: <><path d="m10 13 4-4m-5 7-2 2a3.5 3.5 0 0 1-5-5l4-4a3.5 3.5 0 0 1 5 0m2-1 2-2a3.5 3.5 0 0 1 5 5l-4 4a3.5 3.5 0 0 1-5 0"/></>,
  phone: <><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></>,
  book: <><path d="M4 4h6l2 2 2-2h6v15h-6l-2 2-2-2H4zM12 6v15"/></>,
  chart: <><path d="M3 3v18h18M8 16v-4m5 4V8m5 8V5"/></>,
  people: <><circle cx="9" cy="8" r="3"/><path d="M3 20v-2a6 6 0 0 1 12 0v2M16 5a3 3 0 0 1 0 6m1 3a5 5 0 0 1 4 5v1"/></>,
  calendar: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4m8-4v4M3 10h18"/></>,
  folder: <path d="M3 20V4h6l2 3h10v13z"/>,
  pulse: <path d="M2 12h4l3-8 5 16 3-8h5"/>,
  arrow: <path d="M4 12h15m-6-6 6 6-6 6"/>,
  lock: <><rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2"/></>
};

function Icon({ name, size = 19 }: { name: string; size?: number }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.55" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{icons[name]}</svg>;
}

async function api<Result>(data?: object): Promise<Result> {
  const response = await fetch("/api/command-center", data ? {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
  } : { cache: "no-store" });
  const result = await response.json();
  if (!response.ok) throw Object.assign(new Error(result.error ?? "The request failed."), { status: response.status });
  return result;
}

function dateLabel(value: string | null | undefined) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return "—";
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return date.toLocaleDateString(undefined, { dateStyle: "medium", timeZone: "UTC" });
  return date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

function linkTo(base: string, path: string) {
  try {
    const url = new URL(path, base);
    if (url.protocol === "https:") return url.href;
  } catch { /* A missing public link leaves the panel informational. */ }
  return undefined;
}

function evidenceLink(value: string | null | undefined) {
  try { if (value && new URL(value).protocol === "https:") return value; } catch { /* Evidence can be a reference ID. */ }
}

const contextKinds: Partial<Record<AreaId, string>> = {
  executive: "priority", email: "email", youtube: "youtube", social: "social", podcast: "podcast",
  partnerships: "opportunity", nation: "release", curriculum: "lesson", revenue: "offer", crm: "contact",
  calendar: "meeting", library: "content", analytics: "report"
};

function draftFrom(output: string | null) {
  try {
    const data = JSON.parse(output ?? "") as AgentResult;
    return typeof data.draft === "string" ? data : null;
  } catch { return null; }
}

export function CommandCenter({ signInAvailable }: { signInAvailable: boolean }) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [checking, setChecking] = useState(signInAvailable);
  const [areaId, setAreaId] = useState<AreaId>("executive");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [integrations, setIntegrations] = useState<Integration[] | null>(null);
  const [providerReads, setProviderReads] = useState<Record<string, ReadResult["items"] | undefined>>({});
  const [authUrl, setAuthUrl] = useState("");
  const [editing, setEditing] = useState<RecordItem | null>(null);
  const [agentId, setAgentId] = useState("auto");
  const [contextIds, setContextIds] = useState<string[]>([]);
  const [mobileNav, setMobileNav] = useState(false);
  const area = commandAreas.find(item => item.id === areaId) ?? commandAreas[0];
  const state = snapshot?.state;
  const records = state?.records ?? [];
  const locationRecords = records.filter(record => record.area === areaId);
  const pending = state?.approvals.filter(approval => approval.status === "pending") ?? [];

  useEffect(() => {
    if (!signInAvailable) return;
    let active = true;
    void api<Snapshot>().then(data => { if (active) setSnapshot(data); }).catch(reason => {
      if (active && reason.status !== 401) setError(reason.message);
    }).finally(() => { if (active) setChecking(false); });
    return () => { active = false; };
  }, [signInAvailable]);

  const signedIn = snapshot !== null;
  useEffect(() => {
    if (!signedIn) return;
    let active = true;
    void api<{ integrations: Integration[] }>({ kind: "list_integrations" })
      .then(data => { if (active) setIntegrations(data.integrations); })
      .catch(() => { if (active) setIntegrations(null); });
    return () => { active = false; };
  }, [signedIn]);

  function navigate(id: AreaId) {
    setAreaId(id);
    setEditing(null);
    setMobileNav(false);
    setNotice("");
    setError("");
  }

  async function perform(action: () => Promise<void>, success = "") {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await action();
      setNotice(success);
    } catch (reason) {
      if (reason instanceof Error) {
        if ("status" in reason && reason.status === 401) setSnapshot(null);
        setError(reason.message);
      } else setError("The request failed.");
    } finally { setBusy(false); }
  }

  async function mutate(data: object) {
    const updated = await api<{ state: State }>(data);
    setSnapshot(previous => previous ? { ...previous, state: updated.state } : previous);
  }

  function login(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    void perform(async () => {
      await api({ kind: "sign_in", email: data.get("email"), password: data.get("password") });
      setSnapshot(await api<Snapshot>());
    });
  }

  function saveRecord(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    void perform(async () => {
      await mutate({ kind: "save_record", area: areaId, id: editing?.id, title: data.get("title"),
        stage: data.get("stage"), body: data.get("body"), evidence: data.get("evidence") });
      setEditing(null);
      form.reset();
    }, "Record saved.");
  }

  function requestApproval(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    void perform(async () => {
      await mutate({ kind: "request_approval", action: data.get("action"), title: data.get("title"),
        body: data.get("body"), record_id: data.get("record_id") || undefined });
      form.reset();
    }, "Approval request recorded.");
  }

  async function providerAction(kind: string, key: string) {
    await perform(async () => {
      if (kind === "authorize_integration") {
        const result = await api<{ authorizationUrl: string }>({ kind, key });
        setAuthUrl(result.authorizationUrl);
        return;
      }
      const result = await api<ReadResult>({ kind, key });
      setIntegrations(previous => previous?.map(row => row.id === key ? result.integration : row) ?? [result.integration]);
      if ("items" in result) setProviderReads(previous => ({ ...previous, [key]: result.items }));
    });
  }

  function renderProvider(key: string, heading: string) {
    const integration = integrations?.find(row => row.id === key);
    const items = providerReads[key];
    return <section className="cm-card">
      <div className="cm-card-head"><h2>{heading}</h2>{integration && <span className="cm-status">{integration.status}</span>}</div>
      <p>{integration?.detail ?? "Load integrations to check provider access."}</p>
      <div className="cm-actions">
        <button className="cm-button secondary" disabled={busy || !integration?.canVerify} onClick={() => void providerAction("read_integration", key)}>Read from provider</button>
        <button className="cm-text" onClick={() => navigate("integrations")}>Manage connection <Icon name="arrow" size={16}/></button>
      </div>
      {items && (items.length ? <ul className="cm-list">{items.map(item => <li key={item.id}>
        <strong>{item.title}</strong><span>{item.detail}</span>{item.date && <small>{dateLabel(item.date)}</small>}
        {evidenceLink(item.url) && <a href={item.url} target="_blank" rel="noreferrer">Open source</a>}
      </li>)}</ul> : <p className="cm-empty">The verified read returned no items.</p>)}
    </section>;
  }

  return <div className="cm-shell">
    <aside className={`cm-sidebar ${mobileNav ? "is-open" : ""}`}>
      <Link className="cm-brand" href="/"><span className="cm-logo" aria-hidden="true"><i/><i/><i/></span><span>CONCRETE<small>MOTIVATION</small></span></Link>
      <nav aria-label="Command Center" id="cm-navigation">
        {(["Overview", "Production", "Business", "System"] as const).map(group => <div className="cm-nav-group" key={group}>
          <p>{group}</p>
          {commandAreas.filter(item => item.group === group).map(item =>
            <button key={item.id} aria-current={areaId === item.id ? "page" : undefined} onClick={() => navigate(item.id)}>
              <Icon name={item.icon} size={17}/><span>{item.name}</span>
            </button>
          )}
        </div>)}
      </nav>
      <div className="cm-sidebar-footer"><span className="cm-avatar" aria-hidden="true">CM</span><div><b>Owner workspace</b><small>Concrete Motivation</small></div><Icon name="lock" size={15}/></div>
    </aside>
    <div className="cm-frame">
      <header className="cm-top">
        <button className="cm-menu cm-button secondary" aria-controls="cm-navigation" aria-expanded={mobileNav} onClick={() => setMobileNav(!mobileNav)}>{mobileNav ? "Close" : "Menu"}</button>
        <div className="cm-crumb"><span>Command Center</span><span aria-hidden="true">/</span><strong>{area.name}</strong></div>
        {snapshot ? <button className="cm-button secondary" disabled={busy} onClick={() => void perform(async () => {
          await api({ kind: "sign_out" }); setSnapshot(null); setIntegrations(null); setProviderReads({}); setAuthUrl("");
        })}>Sign out</button> : <span className="cm-status"><Icon name="lock" size={14}/> Private</span>}
      </header>
      <main id="main-content" className="cm-main">
        {(areaId === "executive" || !snapshot) ? <section className="cm-hero">
          <div className="cm-hero-copy"><span className="cm-kicker"><span/> Owner operations</span>
            <h1>Concrete <em>Command Center</em></h1>
            <p>Manage Concrete Motivation, Concrete Conversations and Concrete Nation from one workspace.</p>
          </div>
          <span aria-hidden="true" className="cm-hero-mark"><i/><i/><i/></span>
        </section> : <div className="cm-heading"><span className="cm-kicker">{area.group}</span><h1>{area.name}</h1><p>{area.description}</p></div>}
        <div className="cm-feedback" aria-live="polite">
          {error && <p className="cm-alert" role="alert">{error}</p>}{notice && <p className="cm-alert success">{notice}</p>}
        </div>
        {checking ? <p className="cm-card" role="status">Checking owner session…</p> : !snapshot ? <section className="cm-card cm-login">
          <div className="cm-card-head"><Icon name="lock"/><h2>Owner sign-in</h2></div>
          {signInAvailable ? <form onSubmit={login} className="cm-form">
            <label>Email<input name="email" type="email" autoComplete="username" required maxLength={254}/></label>
            <label>Password<input name="password" type="password" autoComplete="current-password" required maxLength={1024}/></label>
            <button className="cm-button primary" disabled={busy} type="submit">{busy ? "Signing in…" : "Sign in"}</button>
          </form> : <p>Owner sign-in is awaiting configuration for this environment.</p>}
        </section> : <>
          {!state && <p className="cm-alert">Workspace storage is awaiting configuration. Integration setup is available independently.</p>}
          {areaId === "executive" && <>
            <div className="cm-stat-grid">
              <Stat icon="link" label="Connected accounts" value={integrations ? integrations.filter(row => row.status === "Verified").length : "—"} sub={integrations ? `${integrations.filter(row => row.status === "Pending Authorization").length} awaiting authorization` : "Verified provider reads"}/>
              <Stat icon="grid" label="Pending decisions" value={state ? pending.length : "—"} sub="Owner approval queue"/>
              <Stat icon="folder" label="Production pipeline" value={state ? records.filter(item => ["youtube", "social", "podcast"].includes(item.area)).length : "—"} sub="Video, social and podcast records"/>
              <Stat icon="pulse" label="Automation failures" value={state ? state.runs.filter(item => item.status === "failed").length : "—"} sub={state ? `${state.runs.filter(item => item.status === "succeeded").length} recent successful runs` : "Recent workflow runs"}/>
            </div>
            <div className="cm-columns">
              <section className="cm-card"><div className="cm-card-head"><h2>Today’s priorities</h2><button className="cm-text" onClick={() => document.getElementById("cm-record-form")?.scrollIntoView()}>Add priority <Icon name="arrow" size={16}/></button></div>
                {locationRecords.filter(item => item.stage !== "Complete").length ? <ul className="cm-list">{locationRecords.filter(item => item.stage !== "Complete").slice(0, 5).map(item => <li key={item.id}><strong>{item.title}</strong><small>{item.stage}</small></li>)}</ul> : <p className="cm-empty">No active priorities recorded.</p>}
              </section>
              {renderProvider("googlecalendar", "Upcoming meetings")}
              <section className="cm-card"><div className="cm-card-head"><h2>Business activity</h2></div>
                <div className="cm-actions cm-tall-actions">
                  <button className="cm-text" onClick={() => navigate("podcast")}>Podcast pipeline <Icon name="arrow" size={16}/></button>
                  <button className="cm-text" onClick={() => navigate("crm")}>Outreach opportunities <Icon name="arrow" size={16}/></button>
                  <a className="cm-text" href={linkTo(siteConfig.links.app, "/owner")} target="_blank" rel="noreferrer">Membership and revenue <Icon name="arrow" size={16}/></a>
                </div>
              </section>
              <section className="cm-card"><div className="cm-card-head"><h2>App release readiness</h2></div><p>Check native build evidence and submission blockers in the existing release center.</p>
                <a className="cm-text" href={linkTo(siteConfig.links.app, "/release")} target="_blank" rel="noreferrer">Open release center <Icon name="arrow" size={16}/></a>
              </section>
            </div>
          </>}
          {areaId === "email" && renderProvider("gmail", "Business inbox")}
          {areaId === "calendar" && renderProvider("googlecalendar", "Calendar events")}
          {areaId === "youtube" && renderProvider("youtube", "YouTube channel")}
          {areaId === "library" && renderProvider("googledrive", "Google Drive content")}
          {(areaId === "nation" || areaId === "revenue") && <section className="cm-card">
            <h2>{areaId === "nation" ? "Concrete Nation release center" : "Verified commerce and memberships"}</h2>
            <p>{areaId === "nation" ? "Review current builds, native test evidence and owner submission requirements." : "Open the owner dashboard for payment records and membership activity. This workspace tracks offers and projections."}</p>
            <a className="cm-text" href={linkTo(siteConfig.links.app, areaId === "nation" ? "/release" : "/owner")} target="_blank" rel="noreferrer">Open existing dashboard <Icon name="arrow" size={16}/></a>
          </section>}
          {areaId === "curriculum" && <section className="cm-card"><CommandCurriculum completed={locationRecords.filter(record => record.stage === "Completed" && record.evidence === "curriculum-assessment")} onComplete={async result => {
            await mutate({ kind: "save_record", area: "curriculum", stage: "Completed", evidence: "curriculum-assessment", ...result,
              id: locationRecords.find(record => record.stage === "Completed" && record.evidence === "curriculum-assessment" && record.title === result.title)?.id });
          }}/></section>}
          {areaId === "integrations" && <section className="cm-card">
            <div className="cm-card-head"><h2>Provider connections</h2><button className="cm-button secondary" disabled={busy} onClick={() => void perform(async () => {
              const data = await api<{ integrations: Integration[] }>({ kind: "list_integrations" }); setIntegrations(data.integrations);
            })}>Refresh</button></div>
            {authUrl && <p className="cm-alert success"><a href={authUrl} target="_blank" rel="noreferrer">Open provider authorization ↗</a>. Return here to verify the connection.</p>}
            <ul className="cm-list">{integrations?.map(integration => <li key={integration.id}>
              <div className="cm-card-head"><strong>{integration.name}</strong><span className="cm-status">{integration.status}</span></div>
              <span>{integration.detail}</span><small>{integration.limitation}</small>
              {integration.permissions.length > 0 && <small>Access requested for {integration.permissions.join(", ")}</small>}
              {integration.verifiedAt && <small>Read verified {dateLabel(integration.verifiedAt)}</small>}
              <div className="cm-actions">
                {integration.canAuthorize && <button className="cm-button secondary" disabled={busy} onClick={() => void providerAction("authorize_integration", integration.id)}>Authorize</button>}
                {integration.canVerify && <button className="cm-button secondary" disabled={busy} onClick={() => void providerAction("verify_integration", integration.id)}>Verify read access</button>}
              </div>
            </li>)}</ul>
            {!integrations && <p className="cm-empty">Provider status is unavailable. Refresh to check.</p>}
          </section>}
          {areaId === "agents" && <section className="cm-card">
            <div className="cm-card-head"><h2>Assign a task</h2><span className="cm-status">{snapshot.aiConfigured ? "Provider configured" : "Awaiting Authorization"}</span></div>
            <form className="cm-form" onSubmit={event => {
              event.preventDefault(); const form = event.currentTarget;
              const task = new FormData(form).get("task");
              void perform(async () => { setSnapshot(await api<Snapshot>({ kind: "run_agent", agentId, task, contextIds })); }, "Agent run recorded. Review the history below.");
            }}>
              <label>Agent<select value={agentId} onChange={event => { setAgentId(event.target.value); setContextIds([]); }}><option value="auto">Choose automatically</option>{snapshot.agents.map(agent => <option key={agent.id} value={agent.id}>{agent.title}</option>)}</select></label>
              <label>Task<textarea name="task" required minLength={8} maxLength={3000} placeholder="Describe the draft, analysis or decision you need."/></label>
              {agentId !== "auto" && (() => {
                const allowed = snapshot.agents.find(agent => agent.id === agentId)?.allowedContext ?? [];
                const choices = records.filter(record => allowed.includes(contextKinds[record.area as AreaId] ?? ""));
                return choices.length > 0 && <fieldset className="cm-context"><legend>Records to share with the model</legend>
                  {choices.slice(0, 20).map(record => <label key={record.id}><input type="checkbox" checked={contextIds.includes(record.id)}
                    disabled={!contextIds.includes(record.id) && contextIds.length >= 6}
                    onChange={event => setContextIds(event.target.checked ? [...contextIds, record.id] : contextIds.filter(id => id !== record.id))}/>{record.title}</label>)}
                </fieldset>;
              })()}
              <button className="cm-button primary" disabled={!snapshot.aiConfigured || !state || busy}>Run agent</button>
            </form>
            <div className="cm-agent-grid">{snapshot.agents.map(agent => <article key={agent.id}><h3>{agent.title}</h3><p>{agent.responsibility}</p></article>)}</div>
            <h2>Run history</h2>
            <ul className="cm-list">{state?.agent_runs.map(run => {
              const output = draftFrom(run.output);
              return <li key={run.id}><div className="cm-card-head"><strong>{output?.title || run.brief}</strong><span className="cm-status">{run.status}</span></div>
                <small>{dateLabel(run.created_at)}</small>
                {run.error && <span>{run.error}</span>}
                {output && <><p>{output.summary}</p><details><summary>Read draft and next steps</summary><p className="cm-pre">{output.draft}</p>
                  <ul>{output.nextSteps?.map((step: string, index: number) => <li key={index}>{step}</li>)}</ul>
                  {output.missingInformation.length > 0 && <p>Missing information: {output.missingInformation.join(", ")}</p>}
                </details><button className="cm-button secondary" disabled={busy} onClick={() => void perform(() => mutate({
                  kind: "save_record", area: "library", title: output.title, stage: "Draft", body: output.draft, evidence: run.id,
                  id: records.find(record => record.area === "library" && record.evidence === run.id)?.id
                }), "Draft saved to the content library.")}>Save draft to library</button></>}
              </li>;
            })}</ul>
          </section>}
          {areaId === "health" && <>
            <section className="cm-card">
              <div className="cm-card-head"><h2>Owner approvals</h2><span className="cm-status">{pending.length} pending</span></div>
              <p>Approval records your decision. Provider execution must be verified separately.</p>
              <form className="cm-form" onSubmit={requestApproval}>
                <label>Action<select name="action">{approvalActions.map(([key, title]) => <option key={key} value={key}>{title}</option>)}</select></label>
                <label>Title<input name="title" required maxLength={160}/></label>
                <label>Related record<select name="record_id" defaultValue=""><option value="">None</option>{records.map(record => <option key={record.id} value={record.id}>{record.title}</option>)}</select></label>
                <label>Exact details<textarea name="body" required maxLength={12000} placeholder="Include recipients, content, scope or cost as applicable."/></label>
                <button disabled={busy || !state} className="cm-button primary">Queue approval</button>
              </form>
              <ul className="cm-list">{state?.approvals.map(approval => <li key={approval.id}>
                <div className="cm-card-head"><strong>{approval.title}</strong><span className="cm-status">{approval.status}</span></div>
                <small>{approvalActions.find(([id]) => id === approval.action)?.[1] ?? approval.action} · {dateLabel(approval.created_at)}</small>
                <p className="cm-pre">{approval.body}</p>
                {approval.status === "pending" && <form className="cm-form compact" onSubmit={event => {
                  event.preventDefault(); const decision = (event.nativeEvent as SubmitEvent).submitter?.getAttribute("value");
                  const note = new FormData(event.currentTarget).get("note");
                  if (decision === "approved" || decision === "rejected") void perform(() => mutate({ kind: "decide_approval", id: approval.id, decision, note }), "Owner decision recorded.");
                }}>
                  <label>Decision note<input name="note" maxLength={1000}/></label>
                  <div className="cm-actions"><button className="cm-button primary" disabled={busy} value="approved">Approve</button><button className="cm-button secondary" disabled={busy} value="rejected">Reject</button></div>
                </form>}
                {approval.decided_at && <small>Decided {dateLabel(approval.decided_at)} {approval.decision_note}</small>}
              </li>)}</ul>
            </section>
            <section className="cm-card"><h2>Automations</h2><p>Schedules and outcomes are recorded here. Event-driven jobs require a trusted event source.</p>
              <ul className="cm-list">{Object.entries(commandWorkflows).map(([key, title]) => {
                const workflow = state?.automations.find(item => item.key === key);
                return <li key={key}><form className="cm-form compact" onSubmit={event => {
                  event.preventDefault(); const form = new FormData(event.currentTarget);
                  void perform(() => mutate({
                    kind: "set_automation", key, paused: form.get("paused") === "yes", interval_minutes: Number(form.get("interval"))
                  }), "Schedule updated.");
                }}><div className="cm-card-head"><strong>{title}</strong><span className="cm-status">{workflow?.paused === false ? "Enabled" : "Paused"}</span></div>
                  {key !== "daily-briefing" && key !== "engineering-monitor" && <small>Uses eligible workspace records. Live provider events require a connection.</small>}
                  <>
                    <small>Next scheduled run {dateLabel(workflow?.next_run_at)}</small>
                    <div className="cm-actions"><label>Every (minutes)<input type="number" name="interval" min={5} max={10080} defaultValue={workflow?.interval_minutes ?? 1440} required/></label>
                      <label>Scheduling<select key={String(workflow?.paused)} name="paused" defaultValue={workflow?.paused === false ? "no" : "yes"}><option value="yes">Paused</option><option value="no">Enabled</option></select></label>
                      <button className="cm-button secondary" disabled={busy || !state}>Save schedule</button>
                    </div>
                  </>
                </form></li>;
              })}</ul>
            </section>
            <section className="cm-card"><h2>Execution history</h2>
              <ul className="cm-list">{state?.runs.map(run => <li key={run.id}><div className="cm-card-head"><strong>{run.key}</strong><span className="cm-status">{run.status}</span></div>
                <small>{dateLabel(run.created_at)} · Attempts {run.attempts}</small>{run.error && <span>{String(run.error)}</span>}
                {run.output && <details><summary>Run output</summary><pre className="cm-pre">{typeof run.output === "string" ? run.output : JSON.stringify(run.output, null, 2)}</pre></details>}</li>)}</ul>
              {!state?.runs.length && <p className="cm-empty">No runs recorded.</p>}
            </section>
            <section className="cm-card"><h2>Audit log</h2>
              <ul className="cm-list">{state?.audit.map(entry => <li key={entry.id}><strong>{entry.event}</strong><small>{dateLabel(entry.created_at)}</small>
                <details><summary>View event details</summary>{entry.subject_id && <small>Reference {entry.subject_id}</small>}
                  <pre className="cm-pre">{JSON.stringify(entry.details, null, 2)}</pre></details>
              </li>)}</ul>
              {!state?.audit.length && <p className="cm-empty">No audit events recorded.</p>}
            </section>
          </>}
          {area.stages.length > 0 && state && <section className="cm-card">
            <div className="cm-card-head"><h2>{areaId === "executive" ? "Priority records" : "Workspace records"}</h2><span className="cm-status">{locationRecords.length} records</span></div>
            <ul className="cm-list">{locationRecords.map(record => <li key={record.id}>
              <div className="cm-card-head"><strong>{record.title}</strong><span className="cm-status">{record.stage}</span></div>
              {record.body && <p className="cm-pre">{record.body}</p>}
              {evidenceLink(record.evidence) ? <a href={record.evidence ?? undefined} target="_blank" rel="noreferrer">Open evidence</a> : record.evidence && <small>Evidence reference {record.evidence}</small>}
              <div className="cm-actions"><button className="cm-button secondary" onClick={() => { setEditing(record); document.getElementById("cm-record-form")?.scrollIntoView(); }}>Edit</button></div>
            </li>)}</ul>
            {locationRecords.length === 0 && <p className="cm-empty">No records in this workspace yet.</p>}
            <form key={editing?.id ?? areaId} id="cm-record-form" className="cm-form" onSubmit={saveRecord}>
              <h3>{editing ? "Edit record" : "Add a record"}</h3>
              <label>Title<input name="title" defaultValue={editing?.title} required maxLength={160}/></label>
              <label>Stage<select name="stage" defaultValue={editing?.stage}>{area.stages.map(stage => <option key={stage}>{stage}</option>)}</select></label>
              <label>Details<textarea name="body" defaultValue={editing?.body ?? ""} maxLength={12000}/></label>
              {recordTemplates[areaId] && <button type="button" className="cm-text" onClick={event => {
                const body = event.currentTarget.form?.elements.namedItem("body");
                if (body instanceof HTMLTextAreaElement && !body.value.trim()) {
                  body.value = recordTemplates[areaId] ?? "";
                  body.focus();
                }
              }}>Insert workspace template</button>}
              <label>Evidence link or reference<input name="evidence" defaultValue={editing?.evidence ?? ""} maxLength={1000}/></label>
              <div className="cm-actions"><button className="cm-button primary" disabled={busy}>Save record</button>
                {editing && <button type="button" className="cm-button secondary" onClick={() => setEditing(null)}>Cancel edit</button>}
                {areaId !== "executive" && <button type="button" className="cm-text" onClick={() => navigate("health")}>Open approval queue <Icon name="arrow" size={16}/></button>}</div>
            </form>
          </section>}
        </>}
      </main>
      <footer className="cm-footer">Build from pressure. Lead with purpose. Move with discipline.</footer>
    </div>
  </div>;
}

function Stat({ icon, label, value, sub }: { icon: string; label: string; value: string | number; sub: string }) {
  return <article className="cm-stat"><span className="cm-stat-icon"><Icon name={icon} size={18}/></span><span>{label}</span><strong>{value}</strong><small>{sub}</small></article>;
}
