# Gap Statement — LLM for REST API Test Generation (SE1916)

**Member:** Nguyen Tien Dung — SE190034
**Derived only from:** `evidence-table.md` (N = 13 papers, 2019–2026). Paper numbers below (#1–#13) refer to that table.

---

## 1. Structured answers to the GAP questions

| # | Question | Answer (from the evidence table) | Evidence refs |
|---|----------|----------------------------------|---------------|
| 1 | Which LLMs/tools have been evaluated? | GPT family dominates: GPT-3.5 (#1, #6), GPT-3.5-turbo-1106 (#2), GPT-4-Turbo (#4), GPT-4o-mini (#8), GPT-4.1-mini (#9); one fine-tuned small model Llama3-8B (#7); one multi-LLM study where Claude 3.5 Sonnet wins (#5); DeepSeek V3 (#3). Non-LLM baselines: EvoMaster (#10), Morest (#12), DeepREST (#13), and 10 tools in the study (#11). | #1–#13 |
| 2 | Which use OpenAPI/Swagger as input? | The majority: #1, #2, #4, #5, #6, #7, #10, #11, #12, #13 read OpenAPI/Swagger directly; #3 *infers* the spec; #9 uses endpoint/spec definitions. So OpenAPI-as-input is the norm. | #1,#2,#4,#5,#6,#7,#9,#10,#11,#12,#13 |
| 3 | Which coverage metrics were measured? | Code coverage (line/branch/method): #5,#6,#7,#8,#11,#12,#13; status-code/route/operation coverage: #2,#3,#9. Best line coverage ≈ 71.78% (#8); cross-tool ceiling ≈ 52.76% line (#11). | #2,#3,#5,#6,#7,#8,#9,#11,#12,#13 |
| 4 | Which measure executable / pass rate? | #4 (57→80% valid scripts); #5 (Claude 3.5 Sonnet reported the best pass rate of 7 LLMs — exact figure pending full-text, see `evidence-table.md` †). Most others measure coverage rather than script executability. | #4, #5 |
| 5 | Which measure bug/fault detection on a real API? | Yes, but as **counts without ground truth**: 500-errors/crashes (#2 23, #6 42, #7 204, #8 49 crashes, #11 33.3 avg, #13 unique faults) and real bugs (#10 38, #12 44). | #2,#6,#7,#8,#10,#11,#12,#13 |
| 6 | Which limitations recur? | (a) LLM hallucination / oracle uncertainty (#2, #8); (b) evaluation on live APIs with **no ground-truth fault total** → only counts, no Recall (#6, #7, #11, #13); (c) generated coverage can stay **below manual** (#10: 41% vs 82%); (d) small/varied datasets, no edge-case-specific metric. | #2,#6,#7,#8,#10,#11,#13 |

---

## 2. Identified gaps

### GAP-1 (Comparison) — No study compares **LLM vs manual vs EvoMaster simultaneously** on the same APIs
**Evidence:** The "Compares vs manual?" column of the cross-comparison matrix is empty for every LLM paper (#1–#9). LLM tools are compared against *automated* baselines only — AutoRestTest (#6) and LlamaRestTest (#7) beat EvoMaster (42 vs 20 errors; 204 vs 130 faults), and the study (#11) ranks 10 tools — but **none of them adds a human/manual test suite to the same comparison**. The only manual-vs-tool comparison in the entire corpus is EvoMaster (#10), which is **not** an LLM and predates them, and it found generated coverage *below* manual (41% vs 82%). 
**Gap:** there is no head-to-head **LLM vs manual test design vs EvoMaster** evaluation on one common set of APIs.

### GAP-2 (Dataset / ground truth) — No study uses a **pre-seeded-fault** dataset, so fault-detection Recall is never computed
**Evidence:** Fault detection is reported as raw counts on live systems — 38 bugs (#10), 44 bugs (#12), 42 500-errors (#6), 204 faults (#7), 49 crashes (#8) — but because the **total number of faults present is unknown**, no paper reports **Recall** (faults found ÷ faults present) or precise Precision. The single partial exception is RestTSLLM (#5), which reports a **mutation score** (40.8%) — i.e. Recall against *automatically-generated syntactic mutants* — but on 6 self-built APIs, with no LLM-vs-manual-vs-EvoMaster comparison, and using auto-mutants rather than realistic seeded faults. EMB (#11) provides shared *APIs* but not seeded-fault ground truth.
**Gap:** there is no quantitative, ground-truth measurement (on a shared pre-seeded-fault benchmark) of how many *known* faults LLM-generated tests catch relative to manual and EvoMaster.

### GAP-3 (Metric) — Coverage + 500-error counting dominate; **edge-case / error-code coverage and endpoint-type miss analysis are absent**
**Evidence:** Papers measure aggregate coverage (#5,#6,#7,#8,#11,#12,#13) and crash counts (#6,#8,#11,#13). Only #2 explicitly separates 2xx vs 4xx status-code coverage, and only #3 reports 5xx triggering — but **none** measures a dedicated **edge-case scenario count per endpoint** (4xx/5xx + boundary conditions produced by intentionally violating OpenAPI constraints), and **none** breaks coverage down by **endpoint type** (CRUD vs authentication vs error-handling) to show *which* endpoints are missed. A subtlety the experiment must respect: *operation/endpoint* coverage **can already exceed 90%** (RESTifAI 128/134 ≈ 95.5%, #9; RESTSpecIT ~88.6% avg route discovery, #3), whereas *code* coverage stays at ~52% line across classic tools (#11) and ~72% line at best (#8). So the ≥90% **endpoint** target is *attainable in principle* but has **never been verified on EMB APIs with pre-seeded faults, nor decomposed by endpoint type**.
**Gap:** there is no metric capturing edge-case/error-code generation quality per endpoint, no endpoint-type miss profile (CRUD/auth/error-handling), and no verification of the ≥90% endpoint-coverage target on a pre-seeded-fault benchmark.

---

## 3. Consolidated GAP statement

> Although 2019–2026 research has successfully applied advanced LLMs — predominantly the OpenAI/GPT ecosystem (GPT-3.5 in #1/#6, GPT-4-Turbo in #4, GPT-4o-mini in #8) plus a fine-tuned Llama3-8B (#7) and Claude 3.5 Sonnet (#5) — to generate REST API tests from OpenAPI specifications, reaching up to **71.78% line coverage** (#8) and out-performing automated baselines such as EvoMaster on 500-error detection (#6: 42 vs 20; #7: 204 vs 130), the reviewed studies share three unresolved limitations: **(1)** none compares **LLM-generated tests against both manual test design *and* EvoMaster on the same APIs** (the only manual comparison, #10, is a non-LLM tool that scored *below* manual); **(2)** they evaluate fault detection almost entirely by **counting** server errors on live APIs with **no shared pre-seeded-fault ground truth** (the lone partial exception, #5, reports a mutation score on auto-generated mutants), so **fault-detection Recall is never quantified across LLM, manual and EvoMaster**; and **(3)** they report aggregate coverage and 500-error counts but provide **no edge-case/error-code scenario metric per endpoint** and **no breakdown of which endpoint types (CRUD / authentication / error-handling) are missed**.
>
> **→ GAP:** the field lacks a controlled evaluation that, on locally deployed EvoMaster-Benchmark APIs instrumented with **pre-seeded faults**, measures **(i)** LLM endpoint coverage against the **≥90%** target with an endpoint-type miss analysis, **(ii)** ground-truth fault-detection counts for **LLM vs manual vs EvoMaster**, and **(iii)** edge-case scenario counts (4xx/5xx + boundary) per endpoint for LLM vs manual.
>
> **→ Contribution:** an LLM-based API test generator (tool + GitHub repo) plus an evaluation report on **3 EMB APIs with pre-seeded faulty versions**, directly answering RQ1 (coverage + misses), RQ2 (LLM vs manual vs EvoMaster fault detection), and RQ3 (edge-case scenarios), thereby closing GAP-1, GAP-2, GAP-3.

**Papers cited for the GAP:** #6, #7, #8, #10, #11, #13 (primary), supported by #1–#5, #9, #12.
