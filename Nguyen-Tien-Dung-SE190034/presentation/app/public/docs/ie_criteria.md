# Inclusion and Exclusion Criteria (IE Criteria)

**Topic:** LLM for REST API Test Generation (SE1916)
**Member:** Nguyen Tien Dung — SE190034
**Group status:** Officially confirmed (approved by all members)

---

## 1. Inclusion Criteria (IC)
A study is retained only if it satisfies **all** of the inclusion criteria below:

*   **IC1 (Language):** The study must be written entirely in English.
*   **IC2 (Timeline):** The study must be published from 2018 onward (2018 – present).
*   **IC3 (Context Scope):** The study must be directly related to REST API / Web API testing, OpenAPI/Swagger, or automated API test-generation solutions.
*   **IC4 (Technology):** The study must either use a Large Language Model (LLM) **or** build a baseline test-generation system that is clearly relevant enough to serve as a comparison point for the research gap (GAP) — e.g. EvoMaster, RESTler, RestTestGen, Morest.
*   **IC5 (Empirical Evidence):** The study must report empirical results with concrete numbers and evaluation metrics (e.g. coverage, precision, recall, pass rate, fault/bug detection, etc.). Pure surveys or opinion pieces with no original experiment are not selected.

---

## 2. Exclusion Criteria (EC)
A study is excluded immediately if it violates **even one** of the criteria below at the screening stage:

*   **EC1 (Duplicate):** The study is a full content/title duplicate of another study already in the list (used as a backstop when automatic de-duplication misses something), **or** it is an older/superseded version of another study that is being retained.
*   **EC2 (Access Limit):** No legal full-text PDF can be found, or the full text cannot be accessed/downloaded.
*   **EC3 (Format & Length):** The paper is a poster, extended abstract, presentation slide deck, or is too short (< 4 pages).
*   **EC4 (Out of Domain):** The study discusses only GUI testing, unit testing, or mobile-app testing; **or** it uses REST APIs in the reverse direction (APIs as *tools for* LLMs, or LLM-based generation of the OpenAPI specification itself) — i.e. it is not about generating tests *for* a REST API / Web API.
*   **EC5 (Out of Phase):** The study focuses only on the test-execution phase, system monitoring, or test-code maintenance (test maintenance / test naming / test oracle); it does not address generating test scenarios or test code (test generation).

---

## 3. How to apply the criteria codes in the CSV files

*   **Title/Abstract screening round (`02_after_screening_v1.csv`):** Quickly read the title and abstract. If a clear scope violation is found under codes such as `EC4` or `EC5`, set `v1_decision` to `EXCLUDE` and record the corresponding code in `v1_reason`. If the paper looks potentially relevant but is uncertain, mark it `Unsure` and leave the reason blank. If it satisfies all IC, mark it `INCLUDE`.
*   **Full-text round (`03_final_included.csv`):** Read the full text of every `INCLUDE` and `Unsure` paper. Carefully check the empirical condition (`IC5`) and the length/format (`EC3`, `EC2`). A paper that fully passes is recorded as `Include` (column `final_include = YES`) with the reason that it meets all of `IC1–IC5`. A paper excluded at this round is usually one that overlaps in approach with a stronger retained paper (`EC1`) or lacks sufficiently clear empirical numbers (`IC5`).

> **Note on baselines (IC4):** Because the research question of this topic compares LLMs against **manual test design** and **EvoMaster**, the group deliberately retains the classic non-LLM baseline tools (EvoMaster, RESTler, RestTestGen, Morest, QuickREST, DeepREST) as quantitative reference points for the research gap, consistent with IC4.
