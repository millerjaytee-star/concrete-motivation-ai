import { createHash } from "node:crypto";
import { type NextRequest, NextResponse } from "next/server";
import { approvalActions, commandAreas } from "@/lib/command-areas";
import {
  CommandAuthError, requireCommandOwner, setCommandSession, signInCommandOwner, verifyCommandOrigin
} from "@/lib/command-auth";
import {
  CommandStoreError, beginAgentRun, commandStoreConfigured, finishAgentRun, getCommandState,
  mutateCommand, type CommandMutation
} from "@/lib/command-store";
import {
  CommandAgentError, commandAgents, commandRecordContext, executeAgentRun, isCommandAgentConfigured, prepareAgentRun
} from "@/lib/command-agents";
import {
  CommandIntegrationError, listCommandIntegrations, readCommandIntegration,
  startCommandIntegrationAuthorization, verifyCommandIntegration
} from "@/lib/command-integrations";

export const runtime = "nodejs";
export const maxDuration = 55;

function json(data: unknown, status = 200) {
  return NextResponse.json(data, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" }
  });
}

function handleError(error: unknown) {
  if (error instanceof CommandIntegrationError) {
    const response = json({ error: error.message }, error.status);
    if (error.status === 429 && Number.isFinite(error.retryAfter)) {
      response.headers.set("Retry-After", String(error.retryAfter));
    }
    return response;
  }
  if (error instanceof CommandAuthError || error instanceof CommandStoreError) {
    return json({ error: error.message }, error.status);
  }
  if (error instanceof CommandAgentError) {
    const statuses = { input: 400, configuration: 503, rate_limit: 429, timeout: 504, provider: 502, refusal: 422 };
    return json({ error: error.message }, statuses[error.code]);
  }
  return json({ error: "The Command Center could not complete this request. Try again shortly." }, 500);
}

async function readBody(request: NextRequest) {
  const raw = await request.text();
  if (raw.length > 65536) throw new CommandAuthError("The request is too large.", 413);
  let value: unknown;
  try { value = JSON.parse(raw); } catch { throw new CommandAuthError("Enter a valid request.", 400); }
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new CommandAuthError("Enter a valid request.", 400);
  }
  return value as Record<string, unknown>;
}

function stringField(value: unknown) {
  return typeof value === "string" ? value : "";
}

async function state(owner: string) {
  return {
    state: commandStoreConfigured() ? await getCommandState(owner) : null,
    agents: commandAgents.map(({ id, title, responsibility, allowedContext }) => ({ id, title, responsibility, allowedContext })),
    aiConfigured: isCommandAgentConfigured()
  };
}

export async function GET(request: NextRequest) {
  try {
    const owner = await requireCommandOwner(request);
    return json(await state(owner));
  } catch (error) { return handleError(error); }
}

async function runAgent(owner: string, data: Record<string, unknown>) {
  if (!isCommandAgentConfigured()) throw new CommandAuthError("AI generation is awaiting an approved provider configuration.", 503);
  const records = (await getCommandState(owner)).records;
  const requested = new Set(Array.isArray(data.contextIds) ? data.contextIds.filter(id => typeof id === "string").slice(0, 6) : []);
  const context = records.filter(record => requested.has(record.id)).map(commandRecordContext);
  if (context.length !== requested.size) throw new CommandAuthError("One of the selected records is unavailable.", 400);
  const prepared = prepareAgentRun({ agentId: stringField(data.agentId) || undefined, task: stringField(data.task), context });
  const claim = await beginAgentRun(owner, { dedupe_key: prepared.deduplicationKey, agent: prepared.agentId, brief: prepared.task });
  if (!claim.claimed) return json({ ...(await state(owner)), runId: claim.run.id, duplicate: true });
  let result;
  try {
    result = await executeAgentRun(prepared);
  } catch (error) {
    await finishAgentRun(owner, {
      id: claim.run.id, lease: claim.lease,
      error: error instanceof CommandAgentError ? error.message : "Model execution was interrupted."
    });
    throw error;
  }
  await finishAgentRun(owner, { id: claim.run.id, lease: claim.lease, output: JSON.stringify(result) });
  return json({ ...(await state(owner)), runId: claim.run.id });
}

async function applyMutation(owner: string, data: Record<string, unknown>) {
  if (data.kind === "save_record") {
    const area = commandAreas.find(item => item.id === data.area);
    if (!area || !area.stages.some(stage => stage === data.stage)) {
      throw new CommandAuthError("Choose a valid workspace and stage.", 400);
    }
    if (typeof data.stage === "string" && ["Upload", "Analytics", "Improvement", "Scheduled", "Resolved", "Verified evidence linked", "Guest confirmed", "Reply received", "Member joined", "Member at risk", "Member cancelled", "Defect", "Release blocker"].includes(data.stage)
        && !stringField(data.evidence).trim()) {
      throw new CommandAuthError("Link the evidence before recording that stage.", 400);
    }
  }
  if (data.kind === "request_approval") {
    if (!approvalActions.some(([id]) => id === data.action)) throw new CommandAuthError("Choose a valid approval action.", 400);
    const key = createHash("sha256").update(JSON.stringify([
      data.action, stringField(data.title).trim(), stringField(data.body).trim(), data.record_id ?? null
    ])).digest("hex");
    data = { ...data, dedupe_key: key };
  }
  if (!["save_record", "request_approval", "decide_approval", "set_automation", "run_automation"].includes(stringField(data.kind))) {
    throw new CommandAuthError("Unknown Command Center action.", 400);
  }
  return json({ state: await mutateCommand(owner, data as CommandMutation) });
}

export async function POST(request: NextRequest) {
  try {
    verifyCommandOrigin(request);
    const data = await readBody(request);
    if (data.kind === "sign_out") {
      const response = json({ signedOut: true });
      setCommandSession(response, "", 0);
      return response;
    }
    if (data.kind === "sign_in") {
      const session = await signInCommandOwner(data.email, data.password);
      const response = json({ signedIn: true });
      setCommandSession(response, session.token, session.lifetime);
      return response;
    }
    const owner = await requireCommandOwner(request);
    const key = stringField(data.key);
    switch (data.kind) {
      case "list_integrations": return json({ integrations: await listCommandIntegrations(owner) });
      case "authorize_integration": return json(await startCommandIntegrationAuthorization(owner, key));
      case "verify_integration": return json({ integration: await verifyCommandIntegration(owner, key) });
      case "read_integration": return json(await readCommandIntegration(owner, key));
      case "run_agent": return runAgent(owner, data).catch(handleError);
      default: return applyMutation(owner, data).catch(handleError);
    }
  } catch (error) { return handleError(error); }
}
