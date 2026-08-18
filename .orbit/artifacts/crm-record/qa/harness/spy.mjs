/**
 * QA egress spy + offline LLM stub. Loaded with `node --import` BEFORE dist/index.js, so it
 * replaces globalThis.fetch before the openai SDK captures it. Product code is UNMODIFIED.
 *
 * 1. SEND SPY (CLAUDE.md §8 / BR-4). Every outbound fetch is appended to $QA_SPY_LOG. Any request
 *    whose host is api.gupshup.io is REFUSED with a throw and recorded as `blocked`. There is
 *    therefore no code path in this run that can put a WhatsApp message on the wire.
 * 2. LLM STUB. api.openai.com/v1/chat/completions is answered from $QA_LLM_SCRIPT (a JSON array,
 *    consumed in order), so `agent.handleInbound` runs its REAL tool-dispatch loop with zero
 *    network egress, zero spend and a deterministic script.
 * 3. Everything else is refused too — this run makes no third-party call at all.
 */
import fs from "node:fs";

const LOG = process.env.QA_SPY_LOG || "/tmp/qa-spy.jsonl";
const SCRIPT = process.env.QA_LLM_SCRIPT || "";
let cursor = 0;
let scriptMtime = 0;

function record(entry) {
  try { fs.appendFileSync(LOG, JSON.stringify({ ts: Date.now(), ...entry }) + "\n"); } catch {}
}

const realFetch = globalThis.fetch;
globalThis.fetch = async function qaFetch(input, init) {
  const url = String(typeof input === "string" ? input : (input && input.url) || input);
  const method = (init && init.method) || (input && input.method) || "GET";
  const host = (() => { try { return new URL(url).host; } catch { return "?"; } })();

  if (host === "api.gupshup.io") {
    record({ kind: "gupshup", verdict: "BLOCKED", method, url });
    throw new Error("QA SPY: outbound WhatsApp send BLOCKED — no send, to any number, for any reason");
  }

  if (host === "api.openai.com" && url.includes("/chat/completions")) {
    let body = {};
    try { body = JSON.parse(String((init && init.body) || "{}")); } catch {}
    // The insights reader is the ONLY caller that asks for json_object. Branch on it so the
    // conversation script and the record's «فهم المساعد» card cannot consume each other's steps,
    // and so the card is byte-identical on every run (pixel determinism).
    if (body.response_format && body.response_format.type === "json_object") {
      record({ kind: "openai-insights", verdict: "STUBBED", step: 0, tools: [], system_prompt_chars: 0 });
      const ins = JSON.parse(fs.readFileSync(process.env.QA_INSIGHTS_JSON, "utf8"));
      return new Response(JSON.stringify({ id: "chatcmpl-qa-ins", object: "chat.completion",
        created: 1787000000, model: body.model || "stub",
        choices: [{ index: 0, message: { role: "assistant", content: JSON.stringify(ins) }, finish_reason: "stop" }],
        usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 } }),
        { status: 200, headers: { "content-type": "application/json" } });
    }
    let script = [];
    try {
      const st = fs.statSync(SCRIPT);
      if (st.mtimeMs !== scriptMtime) { scriptMtime = st.mtimeMs; cursor = 0; }
      script = JSON.parse(fs.readFileSync(SCRIPT, "utf8"));
    } catch {}
    const step = script[Math.min(cursor, script.length - 1)] || { content: "تمام." };
    cursor += 1;
    const message = step.tool_calls
      ? { role: "assistant", content: null, tool_calls: step.tool_calls.map((t, i) => ({
          id: "call_" + cursor + "_" + i, type: "function",
          function: { name: t.name, arguments: JSON.stringify(t.args || {}) } })) }
      : { role: "assistant", content: step.content ?? "تمام." };
    // The FULL request, so the tool-result strings the model is actually handed (BR-7c) and the
    // grounded-facts block (BR-7d) are observable evidence rather than an inference from source.
    try { fs.appendFileSync(process.env.QA_LLM_TRACE || "/tmp/qa-llm-trace.jsonl",
      JSON.stringify({ ts: Date.now(), step: cursor, messages: body.messages }) + "\n"); } catch {}
    record({ kind: "openai", verdict: "STUBBED", step: cursor,
             tools: step.tool_calls ? step.tool_calls.map((t) => t.name) : [],
             system_prompt_chars: String(((body.messages || [])[0] || {}).content || "").length });
    const payload = { id: "chatcmpl-qa", object: "chat.completion", created: Math.floor(Date.now() / 1e3),
      model: body.model || "stub", choices: [{ index: 0, message,
        finish_reason: step.tool_calls ? "tool_calls" : "stop" }],
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 } };
    return new Response(JSON.stringify(payload), { status: 200, headers: { "content-type": "application/json" } });
  }

  record({ kind: "other", verdict: "BLOCKED", method, url: url.slice(0, 200) });
  throw new Error("QA SPY: third-party egress refused in the QA run: " + host);
};
globalThis.fetch.__qaSpy = true;
record({ kind: "boot", verdict: "SPY_INSTALLED", url: "-", method: "-", realFetch: typeof realFetch });
