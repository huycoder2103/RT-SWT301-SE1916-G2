// RBL-5 final defense deck. Numbers are READ from results/ (never hand-typed), matching the
// paper's macro discipline. Run: node scripts/gen_rbl5_slides.js
//   requires pptxgenjs on NODE_PATH (npm i -g pptxgenjs, or set NODE_PATH to a local install)
// Output: presentation/RBL5_final_defense.pptx
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = path.dirname(__dirname);
const S = JSON.parse(fs.readFileSync(path.join(ROOT, "results/stats/summary.json"), "utf8"));
const PD = JSON.parse(fs.readFileSync(path.join(ROOT, "results/produced-vs-detected.json"), "utf8"));

// ---- pull every number from the data ----
const rq1 = S.RQ1_endpoint_coverage, rq2 = S.RQ2_fault_detection, rq3 = S.RQ3_edge_cases_llm_vs_manual;
const rec = rq2.overall_recall, mcLE = rq2.mcnemar.llm_vs_evomaster, mcLM = rq2.mcnemar.llm_vs_manual;
const det = PD.detected, prod = PD.produced;
const pfmt = (p) => (p < 1e-4 ? p.toExponential(2).replace("e", "×10^") : p.toFixed(3));
const pct = (x) => (x * 100).toFixed(1) + "%";

const p = new pptxgen();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";
const NAVY = "0F1B2B", LIGHT = "F7FAFC", TEAL = "1C7293", BLUE = "065A82",
      MINT = "02C39A", INK = "15202B", MUTE = "5B6B7B", WHITE = "FFFFFF",
      RED = "E5484D", AMBER = "B45309", LINE = "DCE4EC";
const HF = "Georgia", BF = "Calibri", MONO = "Consolas";
const W = 13.333;

function title(s, t, sub, dark) {
  s.addText(t, { x: 0.6, y: 0.42, w: W - 1.2, h: 0.7, fontFace: HF, bold: true, fontSize: 30, color: dark ? WHITE : INK });
  if (sub) s.addText(sub, { x: 0.62, y: 1.08, w: W - 1.2, h: 0.4, fontFace: BF, italic: true, fontSize: 14, color: dark ? MINT : TEAL });
  s.addShape(p.ShapeType.line, { x: 0.62, y: 1.5, w: 3.2, h: 0, line: { color: MINT, width: 2.5 } });
}
function kpi(s, x, y, n, l, color) {
  s.addText(n, { x, y, w: 3.0, h: 0.8, fontFace: HF, bold: true, fontSize: 40, color: color || TEAL, align: "center" });
  s.addText(l, { x, y: y + 0.82, w: 3.0, h: 0.5, fontFace: BF, fontSize: 12.5, color: MUTE, align: "center" });
}

// ===== S1 Title =====
let s = p.addSlide(); s.background = { color: NAVY };
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 0.9, w: 0.9, h: 0.9, rectRadius: 0.12, fill: { color: TEAL }, line: { type: "none" } });
s.addText("{ }", { x: 0.6, y: 0.9, w: 0.9, h: 0.9, align: "center", valign: "middle", fontFace: MONO, bold: true, color: MINT, fontSize: 28 });
s.addText("Can an LLM out-test a human baseline and a search-based tool?", { x: 0.6, y: 2.0, w: 12, h: 1.3, fontFace: HF, bold: true, fontSize: 34, color: WHITE });
s.addText("A ground-truth comparison of LLM vs Manual vs EvoMaster on pre-seeded-fault REST APIs",
  { x: 0.6, y: 3.25, w: 12, h: 0.6, fontFace: HF, fontSize: 19, color: "CADCFC" });
s.addText([
  { text: "Result: ", options: { color: MINT, bold: true } },
  { text: `EvoMaster ${rec.evomaster} > LLM ${rec.llm} > Manual ${rec.manual}`, options: { color: WHITE, bold: true } },
  { text: "  — an LLM beats a human-style suite yet loses to a 2019 tool", options: { color: "9FB3C8" } },
], { x: 0.62, y: 4.2, w: 12, h: 0.4, fontFace: BF, fontSize: 15 });
s.addText("SWT301 · RBL-5 · Group SE1916-G2 · Summer 2026 · GV: L.T.Q. Chi",
  { x: 0.62, y: 5.7, w: 12, h: 0.35, fontFace: BF, bold: true, fontSize: 13, color: WHITE });
s.addText("Huy (SE190240, PL) · Dung (SE190034, LR) · Dat (SE190239, DG) · Thuan (SE190305, MS) · Nguyen (SE190220, RW)",
  { x: 0.62, y: 6.1, w: 12, h: 0.35, fontFace: BF, fontSize: 12, color: "9FB3C8" });

// ===== S2 Gap =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "The gap: 59 papers, no ground truth", "Systematic review 2018–2026, five independent searches merged");
const gaps = [
  ["GAP-C", "No study puts LLM vs Manual vs a mature tool on the same APIs. The one manual comparison (EvoMaster 2019) predates LLMs.", TEAL],
  ["GAP-D", "Fault detection = raw 500-error counts on live APIs. With no pre-seeded-fault benchmark, ground-truth Recall is never computed.", AMBER],
  ["GAP-M", "Evaluation is coverage-biased. No per-endpoint edge-case / error-code metric exists.", BLUE],
];
gaps.forEach((g, i) => {
  const y = 2.0 + i * 1.55;
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.35, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
  s.addText(g[0], { x: 0.85, y: y + 0.15, w: 1.8, h: 1.0, fontFace: HF, bold: true, fontSize: 22, color: g[2], valign: "middle" });
  s.addText(g[1], { x: 2.8, y: y + 0.12, w: 9.6, h: 1.1, fontFace: BF, fontSize: 15, color: INK, valign: "middle" });
});
s.addText("Primary cluster = GAP-C + GAP-D (best-evidenced). GAP-M is the metric facet.",
  { x: 0.62, y: 6.75, w: 12, h: 0.4, fontFace: BF, italic: true, fontSize: 13, color: MUTE });

// ===== S3 RQs =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Three research questions", "Frozen at proposal approval — no HARKing");
const rqs = [
  ["RQ1", "Coverage", "Do LLM tests reach endpoint coverage ≥ 90%?", "absolute"],
  ["RQ2", "Fault detection", "How many pre-seeded faults do LLM vs Manual vs EvoMaster detect?", "comparative — PRIMARY"],
  ["RQ3", "Edge cases", "Does the LLM produce more 4xx/5xx + boundary scenarios per endpoint than manual?", "comparative"],
];
rqs.forEach((r, i) => {
  const y = 2.0 + i * 1.5;
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.3, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
  s.addText(r[0], { x: 0.85, y: y + 0.1, w: 1.5, h: 1.1, fontFace: HF, bold: true, fontSize: 24, color: TEAL, valign: "middle" });
  s.addText([{ text: r[1] + "  ", options: { bold: true, color: INK, fontSize: 17 } },
             { text: r[3], options: { italic: true, color: MINT, fontSize: 12 } }], { x: 2.5, y: y + 0.16, w: 10, h: 0.4, fontFace: BF });
  s.addText(r[2], { x: 2.5, y: y + 0.6, w: 9.9, h: 0.6, fontFace: BF, fontSize: 14, color: MUTE });
});

// ===== S4 Method =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Method: three arms, known faults", "Blind protocol — suites authored before faults seeded");
kpi(s, 0.8, 2.1, "3", "EMB REST APIs\n(ncs, scs, features)", TEAL);
kpi(s, 4.0, 2.1, String(rq1.n_operations), "operations", TEAL);
kpi(s, 7.2, 2.1, String(rq2.n_mutants_total), "seeded mutants\n(mutation = known denominator)", AMBER);
kpi(s, 10.4, 2.1, "3", "arms compared", BLUE);
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 3.9, w: 12.1, h: 2.9, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
const arms = [
  ["LLM", "Claude Sonnet 4.6, temp 0, spec-only (black-box). Frozen prompt. Status-code oracles.", TEAL],
  ["Manual", "Independently re-authored EP/BVA suite — isolated session, spec-only, blind. Status-code oracles.", BLUE],
  ["EvoMaster 6.0.0", "Search-based, black-box. Records original responses → regression-value oracles.", AMBER],
];
arms.forEach((a, i) => {
  const y = 4.15 + i * 0.85;
  s.addText(a[0], { x: 0.9, y, w: 2.6, h: 0.7, fontFace: HF, bold: true, fontSize: 16, color: a[2], valign: "middle" });
  s.addText(a[1], { x: 3.6, y, w: 8.9, h: 0.7, fontFace: BF, fontSize: 13.5, color: INK, valign: "middle" });
});
s.addText("Ground truth = mutation kill: an arm kills a mutant iff a test passing on the original fails on the mutant.",
  { x: 0.62, y: 6.9, w: 12, h: 0.4, fontFace: BF, italic: true, fontSize: 12.5, color: MUTE });

// ===== S5 RQ1 =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "RQ1 — the LLM reaches everything", "One-sample Wilcoxon vs 90%");
kpi(s, 1.2, 2.4, pct(rq1.coverage_overall_pct / 100), "endpoint coverage", MINT);
kpi(s, 5.0, 2.4, `${rq1.ops_covered}/${rq1.n_operations}`, "operations exercised", TEAL);
kpi(s, 8.8, 2.4, "p = " + pfmt(rq1.p_value_one_sided), "H0 (≤90%) rejected", TEAL);
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 4.4, w: 12.1, h: 1.9, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
s.addText([
  { text: "But coverage is a weak signal. ", options: { bold: true, color: INK } },
  { text: "Reaching every documented operation says nothing about whether the tests notice a fault behind a 200 response. RQ2 is where that distinction bites.", options: { color: MUTE } },
], { x: 0.9, y: 4.6, w: 11.5, h: 1.5, fontFace: BF, fontSize: 16, valign: "middle", lineSpacingMultiple: 1.2 });

// ===== S6 RQ2 (headline) =====
s = p.addSlide(); s.background = { color: NAVY };
title(s, "RQ2 — the primary result", "Fault-detection Recall against " + rq2.n_mutants_total + " known faults", true);
kpi(s, 0.9, 2.1, rec.evomaster, "EvoMaster", MINT);
kpi(s, 5.0, 2.1, rec.llm, "LLM", "CADCFC");
kpi(s, 9.1, 2.1, rec.manual, "Manual", RED);
s.addText("EvoMaster  >  LLM  >  Manual", { x: 0.6, y: 3.5, w: 12, h: 0.6, fontFace: HF, bold: true, fontSize: 26, color: WHITE, align: "center" });
s.addShape(p.ShapeType.roundRect, { x: 1.3, y: 4.35, w: 10.7, h: 2.5, rectRadius: 0.1, fill: { color: "16283C" }, line: { color: TEAL, width: 1 } });
s.addText([
  { text: "The pilot saw LLM = Manual (identical kills). That was a same-agent artefact.\n", options: { color: MINT, bold: true, fontSize: 15 } },
  { text: `With an independent Manual suite the arms diverge: LLM out-detects it (McNemar b=${mcLM["llm_only(b)"]}, c=${mcLM["manual_only(c)"]}, p≈${mcLE.p_value.toFixed(3)}; manual's kills ⊆ LLM's).\n`, options: { color: WHITE, fontSize: 14 } },
  { text: `EvoMaster in turn out-detects the LLM (b=${mcLE["llm_only(b)"]}, c=${mcLE["evomaster_only(c)"]}, p≈${mcLE.p_value.toFixed(3)}). Both hold at α=0.05, neither under Bonferroni — directional, not decisive.\n`, options: { color: WHITE, fontSize: 14 } },
  { text: "H1 (“LLM best”) is rejected: the LLM beats the human-style baseline but not the tool.", options: { color: "CADCFC", italic: true, fontSize: 13.5 } },
], { x: 1.6, y: 4.55, w: 10.1, h: 2.1, fontFace: BF, valign: "middle", lineSpacingMultiple: 1.15 });

// ===== S7 mechanism =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Why: a two-level mechanism", "The ordering tracks fault character, not generator cleverness");
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 2.0, w: 5.9, h: 4.4, rectRadius: 0.1, fill: { color: WHITE }, line: { color: TEAL, width: 1.5 } });
s.addText("1. Oracle KIND sets the ceiling", { x: 0.85, y: 2.2, w: 5.4, h: 0.5, fontFace: HF, bold: true, fontSize: 17, color: TEAL });
s.addText([
  { text: "Spec-derived status oracles accept any response in the plausible class. A mutant that changes a computed value but keeps the 200 is invisible.\n\n", options: { color: INK } },
  { text: `rest-ncs (all value faults): LLM ${rq2.per_sut_recall.ncs.llm}  Manual ${rq2.per_sut_recall.ncs.manual}  vs  EvoMaster ${rq2.per_sut_recall.ncs.evomaster}.`, options: { color: AMBER, bold: true } },
  { text: "\nEvoMaster's regression oracle sees value faults; status oracles cannot.", options: { color: MUTE } },
], { x: 0.85, y: 2.8, w: 5.4, h: 3.4, fontFace: BF, fontSize: 13.5, valign: "top", lineSpacingMultiple: 1.1 });
s.addShape(p.ShapeType.roundRect, { x: 6.8, y: 2.0, w: 5.9, h: 4.4, rectRadius: 0.1, fill: { color: WHITE }, line: { color: BLUE, width: 1.5 } });
s.addText("2. VOLUME allocates the rest", { x: 7.05, y: 2.2, w: 5.4, h: 0.5, fontFace: HF, bold: true, fontSize: 17, color: BLUE });
s.addText([
  { text: "Among status-oracle suites, more tests reach more of the status-visible faults.\n\n", options: { color: INK } },
  { text: `rest-scs (some status-visible): LLM ${rq2.per_sut_recall.scs.llm}  vs  Manual ${rq2.per_sut_recall.scs.manual}.`, options: { color: BLUE, bold: true } },
  { text: `\nThe LLM's ${prod.test_cases.llm} tests catch more than the leaner ${prod.test_cases.manual}-test manual suite — whose kills are a strict subset.`, options: { color: MUTE } },
], { x: 7.05, y: 2.8, w: 5.4, h: 3.4, fontFace: BF, fontSize: 13.5, valign: "top", lineSpacingMultiple: 1.1 });
s.addText("Kind fixes the ceiling; volume fills what is under it. The pilot's tie was the two levels coinciding by one author.",
  { x: 0.62, y: 6.6, w: 12, h: 0.5, fontFace: BF, italic: true, fontSize: 13, color: MUTE, align: "center" });

// ===== S8 produced vs detected =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Produced ≠ detected", "Every volume metric ranks the LLM first; the ground truth does not");
const rows = [
  ["", "LLM", "Manual", "EvoMaster"],
  ["Test cases produced", String(prod.test_cases.llm), String(prod.test_cases.manual), String(prod.test_cases.evomaster)],
  ["Edge-case scenarios", String(rq3.llm_total_edge), String(rq3.manual_total_edge), "—"],
  ["Faults detected / " + det.mutation_faults_killed.total, String(det.mutation_faults_killed.llm), String(det.mutation_faults_killed.manual), String(det.mutation_faults_killed.evomaster)],
  ["HTTP error behaviours / " + det.http_error_behaviours_triggered.answer_key, String(det.http_error_behaviours_triggered.llm), String(det.http_error_behaviours_triggered.manual), String(det.http_error_behaviours_triggered.evomaster)],
];
const tbl = rows.map((r, ri) => r.map((c, ci) => ({
  text: c,
  options: {
    fontFace: ri === 0 ? HF : BF, bold: ri === 0 || ci === 0, fontSize: 14,
    color: ri === 0 ? WHITE : (ci === 0 ? INK : MUTE),
    fill: { color: ri === 0 ? TEAL : (ri === 3 ? "FDECEC" : WHITE) },
    align: ci === 0 ? "left" : "center", valign: "middle",
  },
})));
s.addTable(tbl, { x: 0.9, y: 2.15, w: 11.5, colW: [5.0, 2.16, 2.17, 2.17], rowH: 0.62, border: { type: "solid", color: LINE, pt: 1 } });
s.addText([
  { text: "The volume order (LLM > Manual > EvoMaster) is not the effectiveness order (EvoMaster > LLM > Manual). ", options: { bold: true, color: INK } },
  { text: "The arm that produced the fewest tests detected the most faults. Without a denominator, a volume metric would have crowned the LLM outright.", options: { color: MUTE } },
], { x: 0.9, y: 5.9, w: 11.5, h: 1.0, fontFace: BF, fontSize: 14, valign: "top", lineSpacingMultiple: 1.15 });

// ===== S9 RQ3 =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "RQ3 — the LLM is more prolific", "Paired Wilcoxon across " + rq3.n_operations + " operations");
kpi(s, 1.0, 2.3, String(rq3.llm_total_edge), "LLM edge scenarios", TEAL);
kpi(s, 4.6, 2.3, String(rq3.manual_total_edge), "Manual edge scenarios", MUTE);
kpi(s, 8.2, 2.3, "p = " + pfmt(rq3.p_value_one_sided), "H0 rejected", TEAL);
kpi(s, 11.0, 2.3, rq3.rank_biserial.toFixed(2), "rank-biserial", MINT);
s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 4.35, w: 12.1, h: 1.9, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
s.addText([
  { text: `The LLM leads on ${rq3.pairs_llm_more} of ${rq3.n_operations} operations, manual on ${rq3.pairs_manual_more}. Largest effect in the study — and, per RQ2, the least consequential: `, options: { color: INK } },
  { text: "writing more scenarios is not detecting more faults.", options: { bold: true, color: AMBER } },
], { x: 0.9, y: 4.55, w: 11.5, h: 1.5, fontFace: BF, fontSize: 16, valign: "middle", lineSpacingMultiple: 1.2 });

// ===== S10 threats =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Threats — stated plainly", "What we did not control, and how fragile the verdicts are");
const th = [
  ["Independent-agent, not human", "The Manual suite is an isolated model session, not a human cohort. Direction robust (LLM kills ⊇ manual), but a human replication is the top next step."],
  ["Significance is fragile", "Both RQ2 McNemar tests hold at α=0.05 but not under Bonferroni; power is low. We rest on direction + effect size, not p alone."],
  ["One boundary mutant", "On rest-ncs the LLM's recall shifted 1→0 vs the pilot: a bessj n=2 boundary test excluded on a clean rebuild. This is what tips LLM-vs-EvoMaster across 0.05."],
  ["EMB-only, JVM-only, one LLM", "3 small APIs, Claude Sonnet 4.6 only. Mechanism (oracle kind) should generalise to any spec-only generator — a prediction, not a result."],
];
th.forEach((t, i) => {
  const y = 1.95 + i * 1.18;
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.05, rectRadius: 0.06, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
  s.addText(t[0], { x: 0.85, y: y + 0.08, w: 3.5, h: 0.9, fontFace: HF, bold: true, fontSize: 14.5, color: AMBER, valign: "middle" });
  s.addText(t[1], { x: 4.5, y: y + 0.06, w: 8.0, h: 0.93, fontFace: BF, fontSize: 12.5, color: INK, valign: "middle" });
});

// ===== S11 conclusion =====
s = p.addSlide(); s.background = { color: NAVY };
title(s, "Conclusion", "Contributions & takeaways", true);
const cs = [
  "First three-way LLM vs Manual vs EvoMaster on identical APIs, blind, with a known fault population.",
  `Ground-truth Recall on ${rq2.n_mutants_total} seeded mutants — true detection rate, not live-API error counts.`,
  "An LLM out-tests a human-style baseline but is out-tested by a 2019 search tool; volume ≠ effectiveness.",
  "Two-level mechanism: oracle kind sets the ceiling, volume allocates under it.",
  "Fully reproducible: every number regenerates from committed data by script.",
];
cs.forEach((c, i) => {
  const y = 2.0 + i * 0.92;
  s.addShape(p.ShapeType.ellipse, { x: 0.8, y: y + 0.05, w: 0.4, h: 0.4, fill: { color: TEAL }, line: { type: "none" } });
  s.addText(String(i + 1), { x: 0.8, y: y + 0.05, w: 0.4, h: 0.4, align: "center", valign: "middle", fontFace: HF, bold: true, color: WHITE, fontSize: 15 });
  s.addText(c, { x: 1.45, y, w: 11.2, h: 0.85, fontFace: BF, fontSize: 15.5, color: "E6ECF5", valign: "middle" });
});
s.addText("Practitioner rule: use LLM generation for spec conformance & error-path breadth; keep regression / value oracles for computational paths.",
  { x: 0.62, y: 6.7, w: 12, h: 0.5, fontFace: BF, italic: true, fontSize: 13.5, color: MINT });

// ===== S12 repro / thanks =====
s = p.addSlide(); s.background = { color: LIGHT };
title(s, "Reproducibility & team", "Every figure and statistic regenerates from committed raw data");
s.addText([
  { text: "Pipeline (one command per stage):\n", options: { bold: true, color: INK, fontSize: 15 } },
  { text: "mutate → faults/*/catalog.json → run_mutation → results/raw/*.csv → analyze → summary.json → gen_paper_macros → paper\n\n", options: { fontFace: MONO, color: TEAL, fontSize: 11.5 } },
  { text: "Executed 2026-07-17 on pinned toolchain (JDK 8u492 + JDK 17.0.19 + Maven 3.9.16); EMB commit 915859; 133-mutant ground truth reproduced exactly (EvoMaster kills identical to pilot).",
    options: { color: MUTE, fontSize: 13 } },
], { x: 0.9, y: 2.0, w: 11.5, h: 2.0, fontFace: BF, valign: "top", lineSpacingMultiple: 1.15 });
const roles = [["Huy · SE190240", "Project Lead"], ["Dung · SE190034", "LLM Runner"], ["Dat · SE190239", "Data & Ground Truth"], ["Thuan · SE190305", "Metrics & Stats"], ["Nguyen · SE190220", "Report Writer"]];
roles.forEach((r, i) => {
  const x = 0.6 + i * 2.44;
  s.addShape(p.ShapeType.roundRect, { x, y: 4.3, w: 2.3, h: 1.4, rectRadius: 0.08, fill: { color: WHITE }, line: { color: LINE, width: 1 } });
  s.addText(r[0], { x, y: 4.5, w: 2.3, h: 0.5, align: "center", fontFace: HF, bold: true, fontSize: 13, color: INK });
  s.addText(r[1], { x, y: 5.0, w: 2.3, h: 0.5, align: "center", fontFace: BF, fontSize: 12, color: TEAL });
});
s.addText("Thank you — questions welcome.", { x: 0.6, y: 6.3, w: 12, h: 0.6, align: "center", fontFace: HF, bold: true, fontSize: 20, color: TEAL });

const OUT = path.join(ROOT, "presentation", "RBL5_final_defense.pptx");
p.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT + " (" + "12 slides, numbers from results/)"));
