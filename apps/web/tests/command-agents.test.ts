// @vitest-environment node
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { commandAgents, commandRecordContext, executeAgentRun, isCommandAgentConfigured, prepareAgentRun } from "../lib/command-agents";

const approvedSource = { id: "yt-42", kind: "youtube", title: "Editorial notes", content: "Test the first 15 seconds." };
const draft = {
  title: "Opening hook experiment",
  summary: "Test a specific opening for the next draft.",
  draft: "Open with the decision a captain makes after a missed play.",
  nextSteps: ["Produce two cuts."],
  evidenceIds: [approvedSource.id],
  missingInformation: ["Recent retention data."],
  ownerDecisions: ["Approve the cut to prepare for upload."]
};

function providerResponse(content: object[], status = "completed") {
  return Response.json({
    id: "resp_test",
    model: "gpt-4.1-mini-2025-04-14",
    status,
    output: [{ type: "message", role: "assistant", content }],
    usage: { input_tokens: 120, output_tokens: 89 }
  });
}

describe("agent orchestration", () => {
  beforeEach(() => {
    vi.stubEnv("OPENAI_API_KEY", "demo-test-key");
    vi.stubEnv("COMMAND_OPENAI_MODEL", "gpt-4.1-mini");
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("routes all twelve specialist roles", () => {
    const tasks = {
      ceo: "Prepare an executive briefing",
      coo: "Build an SOP for project tracking",
      assistant: "Triage the Gmail inbox",
      cmo: "Plan a marketing campaign",
      content: "Draft a caption and creative brief",
      youtube: "Write a YouTube script",
      podcast: "Prepare the next podcast episode and interview questions",
      outreach: "Qualify a sponsor for outreach",
      curriculum: "Build a financial literacy lesson",
      membership: "Plan membership onboarding and daily bricks",
      cfo: "Review revenue and unit economics",
      engineering: "Review GitHub test results and TestFlight status"
    } as const;
    expect(commandAgents.map(({ id }) => id)).toEqual(Object.keys(tasks));
    for (const [agentId, task] of Object.entries(tasks)) {
      expect(prepareAgentRun({ task }).agentId).toBe(agentId);
    }
  });

  it("rejects arbitrary, duplicate and incompatible context", () => {
    expect(() => prepareAgentRun({ agentId: "cfo", task: "Analyze this", context: [approvedSource] })).toThrow(/outside the scope/);
    expect(() => prepareAgentRun({ task: "Analyze this", context: [{ ...approvedSource, kind: "private-reflection" }] })).toThrow(/outside the scope/);
    expect(() => prepareAgentRun({ task: "Analyze this", context: [approvedSource, approvedSource] })).toThrow(/unique ID/);
    expect(() => prepareAgentRun({ task: " ".repeat(4) })).toThrow(/3,000/);
    expect(() => prepareAgentRun({ task: "Prepare a draft", agentId: "unregistered" })).toThrow(/Choose a command center agent/);
  });

  it("preserves the source and status of owner-entered projections without treating them as revenue evidence", () => {
    const context = commandRecordContext({ id: "projection-2", area: "revenue", title: "Week two forecast", stage: "Projection", body: "Projection ".repeat(400), evidence: "Source worksheet" });
    expect(context.kind).toBe("revenue");
    expect(context.content).toContain("Recorded stage: Projection");
    expect(context.content).toContain("Evidence reference: Source worksheet");
    expect(context.content).toContain("Verify external claims");
    expect(context.content.length).toBeLessThan(1400);
    expect(prepareAgentRun({ agentId: "cfo", task: "Review projections", context: [context] }).context[0]).toEqual(context);
  });

  it("hashes equivalent runs identically and treats new evidence as a new run", () => {
    const otherSource = { ...approvedSource, id: "yt-77" };
    const first = prepareAgentRun({ agentId: "youtube", task: "Prepare a video", context: [approvedSource, otherSource] });
    const second = prepareAgentRun({ agentId: "auto", task: "  Prepare a video  ", context: [otherSource, approvedSource] });
    const changed = prepareAgentRun({ agentId: "youtube", task: "Prepare a video", context: [{ ...approvedSource, content: "New approved evidence." }, otherSource] });
    expect(second.agentId).toBe("youtube");
    expect(second.deduplicationKey).toBe(first.deduplicationKey);
    expect(changed.deduplicationKey).not.toBe(first.deduplicationKey);
  });

  it("makes one bounded, tool-free API request and returns usage and evidence", async () => {
    const run = prepareAgentRun({ agentId: "youtube", task: "Review the opening", context: [approvedSource] });
    const request = vi.fn<typeof fetch>().mockResolvedValue(providerResponse([{ type: "output_text", text: JSON.stringify(draft) }]));
    vi.stubGlobal("fetch", request);
    await expect(executeAgentRun(run)).resolves.toEqual({
      ...draft, agentId: "youtube", responseId: "resp_test", model: "gpt-4.1-mini-2025-04-14", usage: { inputTokens: 120, outputTokens: 89 }
    });
    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0][0]).toBe("https://api.openai.com/v1/responses");
    const body = JSON.parse(String(request.mock.calls[0][1]?.body));
    expect(body).toMatchObject({ store: false, tools: [], tool_choice: "none", max_output_tokens: 1600, text: { format: { type: "json_schema", strict: true } } });
    expect(body.instructions).toContain("YouTube Producer");
    expect(JSON.parse(body.input)).toEqual({ task: run.task, selectedContext: [approvedSource] });
  });

  it("blocks a changed reservation before fetching", async () => {
    const run = prepareAgentRun({ task: "Prepare an executive briefing" });
    const request = vi.fn();
    vi.stubGlobal("fetch", request);
    await expect(executeAgentRun({ ...run, task: "A new prompt" })).rejects.toMatchObject({ code: "input" });
    expect(request).not.toHaveBeenCalled();
  });

  it("fails closed for an unconfigured or unsupported model", async () => {
    const request = vi.fn();
    vi.stubGlobal("fetch", request);
    vi.stubEnv("OPENAI_API_KEY", "");
    expect(isCommandAgentConfigured()).toBe(false);
    await expect(executeAgentRun(prepareAgentRun({ task: "Executive briefing" }))).rejects.toMatchObject({ code: "configuration" });
    vi.stubEnv("OPENAI_API_KEY", "demo-test-key");
    vi.stubEnv("COMMAND_OPENAI_MODEL", "another-model");
    expect(isCommandAgentConfigured()).toBe(false);
    await expect(executeAgentRun(prepareAgentRun({ task: "Executive briefing" }))).rejects.toMatchObject({ code: "configuration" });
    expect(request).not.toHaveBeenCalled();
  });

  it("rejects invented evidence, incomplete drafts, refusals and rate limits", async () => {
    const run = prepareAgentRun({ agentId: "youtube", task: "Review the opening", context: [approvedSource] });
    const request = vi.fn<typeof fetch>()
      .mockResolvedValueOnce(providerResponse([{ type: "output_text", text: JSON.stringify({ ...draft, evidenceIds: ["not-provided"] }) }]))
      .mockResolvedValueOnce(providerResponse([], "incomplete"))
      .mockResolvedValueOnce(providerResponse([{ type: "refusal", refusal: "Provider refusal" }]))
      .mockResolvedValueOnce(new Response(null, { status: 429 }));
    vi.stubGlobal("fetch", request);
    await expect(executeAgentRun(run)).rejects.toMatchObject({ code: "provider", message: expect.stringContaining("unknown evidence") });
    await expect(executeAgentRun(run)).rejects.toMatchObject({ code: "provider", message: expect.stringContaining("completed run") });
    await expect(executeAgentRun(run)).rejects.toMatchObject({ code: "refusal" });
    await expect(executeAgentRun(run)).rejects.toMatchObject({ code: "rate_limit" });
    expect(request).toHaveBeenCalledTimes(4);
  });
});
