# Final Gap Statement (Group) — LLM for REST API Test Generation

**Team:** SWT301_SU26_Group2
**Evidence base:** `evidence-table-merged.md` — N = 59 unique papers (2018–2026) merged from 5 members (85 inclusions, 30.6% overlap).
Paper numbers (#) below refer to the merged table.

---

## 1. From five individual gaps to the group gap

Each member identified gaps; they cluster into four group-level gaps. The **strongest, best-evidenced** one (selected per the template) is **GAP-C + GAP-D combined**, because it is supported by the most members *and* by the highest-quality (peer-reviewed, primary-verified) papers.

| Member | Their headline gap | Clusters into |
|--------|--------------------|---------------|
| DUNG | No LLM-vs-manual-vs-EvoMaster comparison; no pre-seeded faults | GAP-C, GAP-D |
| HUY | No non-OpenAI model benchmarked; no edge-case metric; no pre-seeded business-logic faults | GAP-T, GAP-M, GAP-D |
| DAT | LLM + stateful-fuzzing not combined; token-efficiency unmeasured | GAP-T, GAP-M |
| THUAN | Commercial-LLM dependence; only structural coverage; small datasets | GAP-T, GAP-M, GAP-D |
| NGUYEN | No shared benchmark; coverage-biased metrics; open-source LLMs under-studied | GAP-D, GAP-M, GAP-T |

---

## 2. Group gaps (each tied to specific evidence columns)

### GAP-C (Comparison) — no head-to-head **LLM vs manual vs EvoMaster** on one set of APIs
**Evidence:** Across all 59 papers, the "compares vs manual?" condition is met by **exactly one** study — EvoMaster (#16), which is *not* an LLM and found generated coverage **below** manual (41% vs 82%). LLM tools are compared only against *automated* baselines: AutoRestTest (#7) and LlamaRestTest (#3) beat EvoMaster on 500-errors (42 vs 20; 204 vs 130), and the empirical study (#11) ranks 10 tools — but **none** puts LLM, manual, and EvoMaster on the same APIs. (Members: DUNG primary; DAT widens to RESTler/ARAT-RL.)

### GAP-D (Dataset / ground truth) — no shared **pre-seeded-fault** benchmark → Recall never computed
**Evidence:** Fault detection is reported as raw counts on live systems — 38 bugs (#16), 44 (#17), 42 500-errors (#7), 204 faults (#3), 49 crashes (#9), 38 cloud vulns (#20). Because the *total* fault count is unknown, **no paper reports Recall**. The closest is RestTSLLM's mutation score (#8) on auto-mutants over 6 self-built APIs — not a shared benchmark. NGUYEN's review confirms papers use 2–19 inconsistent services with "no shared benchmark"; RESTestBench (#15) is a first 3-service attempt without pre-seeded business-logic faults. (Members: DUNG, HUY, THUAN, NGUYEN.)

### GAP-M (Metric) — coverage dominates; **edge-case / error-code / business-logic** quality under-measured
**Evidence:** Code coverage (line/branch/method) or operation coverage appears in the large majority; only KAT (#1) separates 2xx/4xx and only RESTSpecIT (#2) reports 5xx triggering. No paper measures an **edge-case scenario count per endpoint** (4xx/5xx + boundary from intentional OpenAPI-constraint violations), nor a **per-endpoint-type miss profile** (CRUD/auth/error-handling). LogiAgent (#9) tries logical bugs but at only 66.19% oracle accuracy. (Members: all five; HUY edge-cases, DAT token-efficiency, THUAN/NGUYEN semantic/mutation.)

### GAP-T (Technology) — non-OpenAI / open-source LLMs barely benchmarked on shared data
**Evidence:** GPT dominates (#1,#5,#6,#7,#12…). Non-OpenAI appears only sporadically and never head-to-head on one benchmark: Claude/DeepSeek/Qwen in RestTSLLM (#8), DeepSeek in RESTSpecIT (#2) and MASTEST (#21), Claude Opus/GPT-5.2 in #46, and one fine-tuned open-source model LlamaRestTest (#3). (Members: HUY Gemini, THUAN LLaMA-3+RAG, NGUYEN open-source survey.)

---

## 3. Consolidated group GAP statement

> Across 59 studies (2018–2026), the team finds that LLMs — overwhelmingly the GPT family — generate REST API tests from OpenAPI specifications with strong results (RESTGPT 97% rule precision #5; AutoRestTest 42 500-errors vs EvoMaster 20 #7; LlamaRestTest 204 faults vs 130 #3; operation coverage up to ~95% in RESTifAI #10). Yet **three gaps persist in otherwise high-quality work**: **(1)** no study compares **LLM-generated tests against both manual test design and EvoMaster on the same APIs** — the only manual comparison, EvoMaster (#16), is a non-LLM tool that scored *below* manual; **(2)** fault detection is measured by **counting** server errors on live systems with **no shared pre-seeded-fault benchmark**, so **ground-truth Recall is never computed across LLM, manual and EvoMaster**; **(3)** evaluation is **coverage-biased** — there is no per-endpoint **edge-case / error-code** metric and no breakdown of which endpoint types (CRUD / authentication / error-handling) are missed.
>
> **→ Group GAP:** the field lacks a controlled study that, on locally deployed **EMB APIs with pre-seeded faults**, measures (i) LLM endpoint coverage against the **≥90%** target with an endpoint-type miss analysis, (ii) ground-truth fault-detection counts for **LLM vs manual vs EvoMaster**, and (iii) edge-case scenario counts (4xx/5xx + boundary) per endpoint.
>
> **→ Group contribution:** an LLM-based API test generator (tool + GitHub repo) and an evaluation report on **3 EMB APIs with pre-seeded faulty versions**, answering RQ1 (coverage + misses), RQ2 (LLM vs manual vs EvoMaster fault detection), and RQ3 (edge-case scenarios) — directly closing GAP-C, GAP-D and GAP-M, with GAP-T (Gemini / open-source) as an optional ablation.

**Papers cited for the group GAP:** #1, #2, #3, #5, #7, #9, #10, #11, #16, #17 (primary-verified), supported by #8, #12, #15, #20, #21, #46 and the breadth of the 59-paper merge.
