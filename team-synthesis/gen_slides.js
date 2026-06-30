// Defense slide deck for the RBL-3 proposal (team-synthesis/proposal.md).
// Run: NODE_PATH=$(npm root -g) node gen_slides.js  -> slides_proposal_defense.pptx
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";

// ---- palette (developer / testing theme) ----
const NAVY = "0F1B2B", LIGHT = "F7FAFC", TEAL = "1C7293", BLUE = "065A82",
      MINT = "02C39A", INK = "15202B", MUTE = "5B6B7B", WHITE = "FFFFFF",
      RED = "E5484D", LINE = "DCE4EC", CARD = "FFFFFF";
const HF = "Georgia", BF = "Calibri", MONO = "Consolas";
const W = 13.333;

function numCircle(s, x, y, n, color) {
  s.addShape(p.ShapeType.ellipse, { x, y, w: 0.42, h: 0.42, fill: { color }, line: { type: "none" } });
  s.addText(String(n), { x, y, w: 0.42, h: 0.42, align: "center", valign: "middle", fontFace: HF, bold: true, color: WHITE, fontSize: 18 });
}
function title(s, t, sub, dark) {
  s.addText(t, { x: 0.6, y: 0.45, w: W - 1.2, h: 0.7, fontFace: HF, bold: true, fontSize: 32, color: dark ? WHITE : INK, align: "left" });
  if (sub) s.addText(sub, { x: 0.62, y: 1.12, w: W - 1.2, h: 0.4, fontFace: BF, italic: true, fontSize: 14, color: dark ? MINT : TEAL });
}

// ===== S1 — Title (dark) =====
let s = p.addSlide(); s.background = { color: NAVY };
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 1.0, w: 0.9, h: 0.9, rectRadius: 0.12, fill: { color: TEAL }, line: { type: "none" } });
s.addText("{ }", { x: 0.6, y: 1.0, w: 0.9, h: 0.9, align: "center", valign: "middle", fontFace: MONO, bold: true, color: MINT, fontSize: 28 });
s.addText("LLM vs Manual vs EvoMaster", { x: 0.6, y: 2.15, w: 12, h: 0.9, fontFace: HF, bold: true, fontSize: 44, color: WHITE });
s.addText("REST API Test Generation on Pre-seeded-Fault Benchmarks", { x: 0.6, y: 3.05, w: 12, h: 0.6, fontFace: HF, fontSize: 24, color: "CADCFC" });
s.addText("Research Proposal  ·  Pending instructor approval", { x: 0.62, y: 3.75, w: 12, h: 0.4, fontFace: BF, italic: true, fontSize: 15, color: MINT });
s.addText([
  { text: "Team SWT301_SU26_Group2", options: { bold: true, color: WHITE } },
  { text: "   ·   Topic SE1916   ·   2026-06-13   ·   v1.0", options: { color: "9FB3C8" } },
], { x: 0.62, y: 5.4, w: 12, h: 0.35, fontFace: BF, fontSize: 14 });
s.addText("Dung (SE190034) · Huy (SE190240) · Dat (SE190239) · Thuan (SE190305) · Nguyen (SE190220)",
  { x: 0.62, y: 5.85, w: 12, h: 0.35, fontFace: BF, fontSize: 12, color: "9FB3C8" });

// ===== S2 — Problem & Gap (light) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "The Problem & The Gap");
s.addText("LLMs can generate REST API tests from an OpenAPI spec — but is that output as good as a human's or EvoMaster's on faults we can actually count?",
  { x: 0.6, y: 1.35, w: W - 1.2, h: 0.6, fontFace: BF, fontSize: 15, color: MUTE });
const gaps = [
  ["C", "Comparison", "No study puts LLM vs Manual vs EvoMaster on the same APIs. The only manual comparison (EvoMaster '19) is non-LLM — and scored below manual."],
  ["D", "Dataset / Ground truth", "Fault detection = raw 500-error counts on live APIs. No shared pre-seeded-fault set → ground-truth Recall is never computed."],
  ["M", "Metric", "Coverage-biased. No per-endpoint edge-case/error-code metric, no endpoint-type miss profile (CRUD / auth / error-handling)."],
];
gaps.forEach((g, i) => {
  const x = 0.6 + i * 4.11;
  s.addShape(p.ShapeType.roundRect, { x, y: 2.5, w: 3.85, h: 3.45, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 1 } });
  s.addShape(p.ShapeType.roundRect, { x, y: 2.5, w: 3.85, h: 0.12, rectRadius: 0, fill: { color: [TEAL, BLUE, MINT][i] }, line: { type: "none" } });
  s.addText("GAP-" + g[0], { x: x + 0.3, y: 2.78, w: 3.2, h: 0.5, fontFace: MONO, bold: true, fontSize: 26, color: [TEAL, BLUE, "0E8C6F"][i] });
  s.addText(g[1], { x: x + 0.3, y: 3.38, w: 3.3, h: 0.5, fontFace: HF, bold: true, fontSize: 17, color: INK });
  s.addText(g[2], { x: x + 0.3, y: 3.92, w: 3.3, h: 1.9, fontFace: BF, fontSize: 13, color: MUTE, valign: "top" });
});
s.addText("Primary cluster: GAP-C + GAP-D  ·  GAP-M = metric facet  ·  (59 papers, 2018–2026)",
  { x: 0.6, y: 6.15, w: W - 1.2, h: 0.4, fontFace: BF, italic: true, fontSize: 13, color: TEAL });

// ===== S3 — Evidence (light) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Evidence — 59 papers (representative)");
const rows = [
  [{ text: "Paper", options: { bold: true } }, { text: "Tool / LLM", options: { bold: true } }, { text: "Metric", options: { bold: true } }, { text: "Best result", options: { bold: true } }],
  ["RESTGPT '24", "GPT-3.5", "rule P/R/F1", "97% precision"],
  ["KAT '24", "GPT-3.5-turbo", "status-code cov", "74.9% (+15.7pp)"],
  ["AutoRestTest '25", "GPT-3.5 + MARL", "code cov / 500s", "42 500s vs EvoMaster 20"],
  ["LlamaRestTest '25", "Llama3-8B", "code cov / faults", "204 faults vs 130"],
  ["RESTifAI '26", "GPT-4.1-mini", "operation coverage", "128/134 ≈ 95.5%"],
  ["EvoMaster '19", "search-based", "cov vs MANUAL", "41% gen vs 82% manual"],
];
s.addTable(rows, { x: 0.6, y: 1.5, w: 7.7, colW: [1.9, 1.9, 1.9, 2.0], rowH: 0.52, fontFace: BF, fontSize: 12.5, color: INK,
  border: { type: "solid", color: LINE, pt: 1 }, fill: { color: WHITE }, align: "left", valign: "middle" });
// pattern callout card on right
s.addShape(p.ShapeType.roundRect, { x: 8.6, y: 1.5, w: 4.13, h: 4.2, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
s.addText("Pattern", { x: 8.85, y: 1.7, w: 3.6, h: 0.4, fontFace: HF, bold: true, fontSize: 18, color: MINT });
s.addText([
  { text: "GPT dominates the LLM line.", options: { bullet: true } },
  { text: "Metrics = coverage + 500-error counts only.", options: { bullet: true } },
  { text: "Baselines are automated-only — no manual suite.", options: { bullet: true } },
  { text: "Fault numbers are live-API counts — never Recall vs a known total.", options: { bullet: true } },
], { x: 8.85, y: 2.2, w: 3.65, h: 3.3, fontFace: BF, fontSize: 13.5, color: "E6EEF5", lineSpacingMultiple: 1.1, valign: "top" });

// ===== S4 — Research Questions (light, FOCUS) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Research Questions", "Locked after approval — no changes (No-HARKing)");
const rq = [
  ["RQ1", "Coverage", "H1: LLM endpoint coverage > 90%", "endpoint coverage %", "≥ 90%  (Case 2)", "1-sample Wilcoxon"],
  ["RQ2", "Fault detection", "H1: Recall(LLM) > Manual & EvoMaster", "mutation-kill Recall", "comparative", "Friedman + McNemar"],
  ["RQ3", "Edge cases", "H1: edge-cases/endpoint LLM > Manual", "scenarios / endpoint", "comparative (Case 3)", "paired Wilcoxon"],
];
rq.forEach((r, i) => {
  const y = 1.75 + i * 1.78;
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y, w: W - 1.2, h: 1.6, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 1 } });
  numCircle(s, 0.85, y + 0.25, "", [TEAL, BLUE, MINT][i]);
  s.addText(r[0], { x: 0.85, y: y + 0.25, w: 0.42, h: 0.42, align: "center", valign: "middle", fontFace: MONO, bold: true, fontSize: 12, color: WHITE });
  s.addText(r[1], { x: 1.45, y: y + 0.18, w: 3.0, h: 0.45, fontFace: HF, bold: true, fontSize: 18, color: INK });
  s.addText(r[2], { x: 1.45, y: y + 0.72, w: 6.0, h: 0.7, fontFace: BF, fontSize: 14, color: TEAL });
  s.addText([
    { text: "metric  ", options: { color: MUTE } }, { text: r[3] + "\n", options: { fontFace: MONO, color: INK, bold: true } },
    { text: "threshold  ", options: { color: MUTE } }, { text: r[4] + "\n", options: { fontFace: MONO, color: BLUE, bold: true } },
    { text: "test  ", options: { color: MUTE } }, { text: r[5], options: { fontFace: MONO, color: INK } },
  ], { x: 7.7, y: y + 0.2, w: 4.9, h: 1.2, fontFace: BF, fontSize: 12.5, valign: "top", lineSpacingMultiple: 1.15 });
});

// ===== S5 — Protocol / Pipeline (light) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Experiment Protocol");
const steps = ["OpenAPI\nspec", "GPT-4o\nfew-shot", "REST-assured\ntests", "run vs original\n+ mutants", "coverage · Recall\n· edge-cases"];
steps.forEach((t, i) => {
  const x = 0.6 + i * 2.5;
  s.addShape(p.ShapeType.roundRect, { x, y: 1.9, w: 2.1, h: 1.3, rectRadius: 0.1, fill: { color: i === 1 ? TEAL : WHITE }, line: { color: i === 1 ? TEAL : LINE, width: 1.2 } });
  s.addText(t, { x, y: 1.9, w: 2.1, h: 1.3, align: "center", valign: "middle", fontFace: BF, bold: true, fontSize: 13, color: i === 1 ? WHITE : INK });
  if (i < steps.length - 1) s.addText("→", { x: x + 2.06, y: 1.9, w: 0.5, h: 1.3, align: "center", valign: "middle", fontFace: HF, fontSize: 22, color: MINT });
});
const facts = [
  ["Dataset", "3 EMB APIs (rest-ncs, rest-scs, features-service) = 35 ops; mutation-seeded faults (ground truth)"],
  ["LLM config", "gpt-4o-2024-08-06 · temp 0 · few-shot from spec · prompt logged verbatim (pilot: Claude proxy)"],
  ["Baselines", "Manual (EP/BVA, blind) + EvoMaster 6.0.0 black-box (--maxTime 120s)"],
  ["Stats", "Wilcoxon / Friedman+McNemar / paired Wilcoxon · α=0.05 · Holm+Bonferroni · effect sizes"],
];
facts.forEach((f, i) => {
  const y = 3.65 + i * 0.8;
  s.addText(f[0], { x: 0.6, y, w: 2.1, h: 0.7, fontFace: HF, bold: true, fontSize: 15, color: TEAL, valign: "top" });
  s.addText(f[1], { x: 2.8, y, w: 9.9, h: 0.7, fontFace: BF, fontSize: 13.5, color: INK, valign: "top" });
});

// ===== S6 — Timeline & Roles (light) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Timeline & Roles");
const tl = [["Week 5–6", "Proposal + GV approval", BLUE], ["Week 7", "Pilot  done", MINT], ["Week 8", "Full run (GPT-4o)", TEAL]];
tl.forEach((t, i) => {
  const x = 0.6 + i * 4.0;
  s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 3.8, h: 1.1, rectRadius: 0.08, fill: { color: t[2] }, line: { type: "none" } });
  s.addText(t[0], { x: x + 0.25, y: 1.85, w: 3.3, h: 0.45, fontFace: MONO, bold: true, fontSize: 16, color: WHITE });
  s.addText(t[1], { x: x + 0.25, y: 2.3, w: 3.3, h: 0.4, fontFace: BF, fontSize: 14, color: "EAF6F2" });
});
s.addText("Roles  (1 deliverable each · LR != MS enforced)", { x: 0.6, y: 3.05, w: 12, h: 0.4, fontFace: HF, bold: true, fontSize: 17, color: INK });
const roles = [
  ["PL", "Nguyen", "Coordinate · merge · GV liaison"],
  ["DG", "Dat", "Dataset · fault catalog · §3"],
  ["LR", "Dung", "Harness · LLM/EvoMaster runs"],
  ["MS", "Huy", "Metrics · statistical tests · §6"],
  ["RW", "Thuan", "Threats · format · slides"],
];
roles.forEach((r, i) => {
  const x = 0.6 + i * 2.46;
  s.addShape(p.ShapeType.roundRect, { x, y: 3.75, w: 2.3, h: 2.4, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 1 } });
  s.addShape(p.ShapeType.ellipse, { x: x + 0.85, y: 3.95, w: 0.6, h: 0.6, fill: { color: NAVY }, line: { type: "none" } });
  s.addText(r[0], { x: x + 0.85, y: 3.95, w: 0.6, h: 0.6, align: "center", valign: "middle", fontFace: MONO, bold: true, fontSize: 15, color: MINT });
  s.addText(r[1], { x, y: 4.65, w: 2.3, h: 0.4, align: "center", fontFace: HF, bold: true, fontSize: 16, color: INK });
  s.addText(r[2], { x: x + 0.15, y: 5.1, w: 2.0, h: 0.95, align: "center", fontFace: BF, fontSize: 11.5, color: MUTE, valign: "top" });
});

// ===== S7 — Threats (light) =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Threats to Validity — top 3");
const th = [
  ["Internal", "LLM & Manual both Claude-authored in pilot (author bias)", "Blind protocol (suites built before faults; spec-only sub-agent logs) + human cohort + GPT-4o for the full run"],
  ["External", "3 small EMB APIs; n=3 limits Friedman power", "Per-fault McNemar pooled (N≈133) is the primary RQ2 test; EMB/JVM-only stated as a limit"],
  ["Construct", "Mutation kill ≠ real-fault detection; coverage ≠ quality", "Standard PIT/Offutt operators (cited); report Recall + coverage + edge-cases jointly"],
];
th.forEach((t, i) => {
  const y = 1.7 + i * 1.65;
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y, w: W - 1.2, h: 1.48, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 1 } });
  s.addText(t[0], { x: 0.85, y: y + 0.2, w: 2.0, h: 0.5, fontFace: HF, bold: true, fontSize: 18, color: RED });
  s.addText(t[1], { x: 0.85, y: y + 0.72, w: 4.7, h: 0.65, fontFace: BF, fontSize: 12.5, color: MUTE, valign: "top" });
  s.addText("→ ", { x: 5.7, y: y + 0.2, w: 0.4, h: 1.1, fontFace: HF, bold: true, fontSize: 18, color: MINT, valign: "top" });
  s.addText(t[2], { x: 6.1, y: y + 0.25, w: 6.5, h: 1.05, fontFace: BF, fontSize: 13, color: INK, valign: "top" });
});

// ===== S8 — Pilot signal (dark) =====
s = p.addSlide(); s.background = { color: NAVY };
title(s, "Preliminary Pilot Signal (Week 7)", "Feasibility evidence — full run with GPT-4o will confirm", true);
const stat = [
  ["100%", "LLM endpoint coverage\n(RQ1 · 35/35 ops · p≈1.6e-9)", MINT],
  ["217 vs 141", "edge-case scenarios LLM vs Manual\n(RQ3 · median 5 vs 4 · p≈6.2e-7)", "CADCFC"],
  ["0.135 vs 0.068", "fault Recall EvoMaster vs LLM/Manual\n(RQ2 · value-oracle catches logic faults)", "F9E795"],
];
stat.forEach((c, i) => {
  const x = 0.6 + i * 4.11;
  s.addShape(p.ShapeType.roundRect, { x, y: 2.2, w: 3.85, h: 3.0, rectRadius: 0.1, fill: { color: "16263A" }, line: { color: TEAL, width: 1 } });
  s.addText(c[0], { x: x + 0.15, y: 2.7, w: 3.55, h: 1.0, align: "center", fontFace: MONO, bold: true, fontSize: 34, color: c[2] });
  s.addText(c[1], { x: x + 0.25, y: 3.8, w: 3.35, h: 1.2, align: "center", fontFace: BF, fontSize: 13.5, color: "E6EEF5", valign: "top" });
});
s.addText("Pilot used Claude Sonnet 4.6 as an available-model proxy; approved full run uses gpt-4o-2024-08-06.",
  { x: 0.6, y: 5.7, w: W - 1.2, h: 0.4, align: "center", fontFace: BF, italic: true, fontSize: 13, color: "9FB3C8" });

p.writeFile({ fileName: "D:/SWT301_SU26_Group2/team-synthesis/slides_proposal_defense.pptx" })
  .then(f => console.log("WROTE", f)).catch(e => { console.error(e); process.exit(1); });
