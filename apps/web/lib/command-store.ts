export const AUTOMATION_KEYS = [
  "daily-briefing",
  "content-draft",
  "podcast-confirmation",
  "outreach-reply",
  "membership-event",
  "engineering-monitor"
] as const;

export type AutomationKey = (typeof AUTOMATION_KEYS)[number];

export type CommandRecord = {
  id: string;
  area: string;
  title: string;
  stage: string;
  body: string;
  evidence: string;
  created_at: string;
  updated_at: string;
};

export type Approval = {
  id: string;
  action: string;
  title: string;
  body: string;
  record_id: string | null;
  dedupe_key: string;
  status: "pending" | "approved" | "rejected";
  decision_note: string;
  created_at: string;
  decided_at: string | null;
};

export type AuditEntry = {
  id: string;
  event: string;
  subject_id: string | null;
  details: Record<string, unknown>;
  created_at: string;
};

export type Automation = {
  key: AutomationKey;
  paused: boolean;
  interval_minutes: number;
  next_run_at: string | null;
  updated_at: string | null;
};

export type AutomationRun = {
  id: string;
  key: AutomationKey;
  event_key: string;
  status: "running" | "succeeded" | "skipped" | "retrying" | "failed";
  attempts: number;
  created_at: string;
  started_at: string;
  finished_at: string | null;
  retry_at: string | null;
  output: string | null;
  error: string | null;
};

export type AgentRun = {
  id: string;
  agent: string;
  brief: string;
  status: "running" | "succeeded" | "failed" | "uncertain";
  output: string | null;
  error: string | null;
  created_at: string;
  finished_at: string | null;
};

export type CommandState = {
  records: CommandRecord[];
  approvals: Approval[];
  audit: AuditEntry[];
  automations: Automation[];
  runs: AutomationRun[];
  agent_runs: AgentRun[];
};

export type CommandMutation =
  | { kind: "save_record"; id?: string; area: string; title: string; stage: string; body?: string; evidence?: string }
  | { kind: "request_approval"; action: string; title: string; body?: string; record_id?: string; dedupe_key: string }
  | { kind: "decide_approval"; id: string; decision: "approved" | "rejected"; note?: string }
  | { kind: "set_automation"; key: string; paused: boolean; interval_minutes: number }
  | { kind: "run_automation"; key: string; event_key: string; trigger?: Record<string, unknown> }
  | { kind: "tick_automations" };

export class CommandStoreError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message);
    this.name = "CommandStoreError";
  }
}

function storeConfig() {
  const url = process.env.COMMAND_SUPABASE_URL?.trim();
  const key = process.env.COMMAND_SUPABASE_SERVICE_KEY?.trim();
  if (!url || !key) return null;
  try {
    const endpoint = new URL(url);
    const local = ["localhost", "127.0.0.1"].includes(endpoint.hostname);
    if (endpoint.protocol !== "https:" && !(endpoint.protocol === "http:" && local)) return null;
    if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash || endpoint.pathname !== "/") return null;
    return { endpoint: endpoint.origin, key };
  } catch {
    return null;
  }
}

export function commandStoreConfigured() {
  return storeConfig() !== null;
}

const rpcErrors: Record<string, [number, string]> = {
  CM001: [400, "Check the workspace entry and try again."],
  CM002: [404, "This workspace entry could not be found."],
  CM003: [409, "This action conflicts with an existing request or decision."],
  CM004: [400, "Add source evidence before recording this status."],
  CM005: [409, "Enable this automation before starting a run."],
  CM006: [409, "An agent request already uses this identifier."],
  CM007: [409, "This agent run cannot accept another result."],
  CM008: [503, "The owner workspace is not configured."],
  CM009: [429, "The workspace has reached 30 agent requests in the last 24 hours."],
  "22P02": [400, "Check the workspace entry and try again."],
  "22003": [400, "Check the workspace entry and try again."],
  "23502": [400, "Check the workspace entry and try again."],
  "23514": [400, "Check the workspace entry and try again."],
  "22001": [400, "Check the workspace entry and try again."]
};

async function commandRpc<T>(name: string, args: Record<string, unknown>): Promise<T> {
  const config = storeConfig();
  if (!config) throw new CommandStoreError(503, "Workspace storage is not configured.");
  const { endpoint, key } = config;
  const headers: Record<string, string> = { apikey: key, "Content-Type": "application/json" };
  if (!key.startsWith("sb_secret_")) headers.Authorization = `Bearer ${key}`;

  let response: Response;
  try {
    response = await fetch(`${endpoint}/rest/v1/rpc/${name}`, {
      method: "POST",
      headers,
      body: JSON.stringify(args),
      cache: "no-store",
      redirect: "error",
      signal: AbortSignal.timeout(12_000)
    });
  } catch {
    throw new CommandStoreError(502, "Workspace storage is temporarily unavailable.");
  }

  if (!response.ok) {
    const failure = await response.json().catch(() => null) as { code?: string } | null;
    const known = typeof failure?.code === "string" && Object.hasOwn(rpcErrors, failure.code) && rpcErrors[failure.code];
    if (known) throw new CommandStoreError(...known);
    throw new CommandStoreError(502, "Workspace storage could not complete the request.");
  }

  try {
    const payload: unknown = await response.json();
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("Expected an object");
    return payload as T;
  } catch {
    throw new CommandStoreError(502, "Workspace storage returned an invalid response.");
  }
}

export function getCommandState(actorId: string): Promise<CommandState> {
  return commandRpc("cm_command_state", { p_actor: actorId });
}

export function mutateCommand(actorId: string, mutation: CommandMutation): Promise<CommandState> {
  return commandRpc("cm_command_mutate", { p_actor: actorId, p_mutation: mutation });
}

export function beginAgentRun(actorId: string, request: { dedupe_key: string; agent: string; brief: string }): Promise<
  { claimed: true; run: AgentRun; lease: string } | { claimed: false; run: AgentRun }
> {
  return commandRpc("cm_command_begin_agent", { p_actor: actorId, p_request: request });
}

export function finishAgentRun(actorId: string, result: { id: string; lease: string; output?: string; error?: string }): Promise<AgentRun> {
  return commandRpc("cm_command_finish_agent", { p_actor: actorId, p_result: result });
}

export function runScheduledCommandAutomations(actorId: string): Promise<{ processed: number }> {
  return commandRpc("cm_command_tick", { p_actor: actorId });
}
