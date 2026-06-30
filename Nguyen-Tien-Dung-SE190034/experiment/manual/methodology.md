# Manual test-design methodology (Comparator arm C1)

The **Manual** arm is the human-style comparator. To keep it (a) blind to source, (b) reproducible,
and (c) consistent across the 3 SUTs, each manual suite is authored by an isolated sub-agent that is
instructed to act as an **experienced manual QA engineer doing black-box test design from the API
documentation only**, applying a conventional, textbook manual methodology — explicitly **NOT** the
LLM arm's systematic per-operation generation prompt.

## Methodology the manual author follows

1. **Equivalence Partitioning (EP):** for each parameter, split the input domain into valid and
   invalid equivalence classes; pick ONE representative per class (this is what distinguishes manual
   design from exhaustive generation — coverage by representatives, not enumeration).
2. **Boundary Value Analysis (BVA):** for ordered/numeric domains, test the boundary and just
   inside/outside it.
3. **Error guessing:** a few tests from experience (e.g. wrong type, missing segment, empty value).
4. **CRUD lifecycle (for resource APIs such as features-service):** create → read → update → delete →
   read-after-delete, plus read/update/delete of a non-existent id.
5. Assert on HTTP status; for undocumented error codes, assert an error **class** (`anyOf`).

## Input / blindness

- Input: ONLY the committed OpenAPI spec for that SUT. No source code, no web, no other files
  (verified via the sub-agent tool log — one Read of the spec file).
- Output: a JUnit 5 + REST-assured class `<Sut>ManualTests` in package `manual`, same harness format
  as the other arms, each `@Test` carrying a `// SCENARIO op=.. type=.. expect=..` tag so RQ3 can
  count edge-case scenarios on the same footing as the LLM arm.

## Threat to validity (disclosed, not hidden)

Both the LLM arm and this Manual arm are ultimately produced by Claude (different models / roles /
methodologies). This is a **construct-validity threat**: a cohort of independent human testers would
strengthen the "LLM vs human" external validity. We mitigate by (i) a distinct, documented manual
methodology, (ii) blindness to source for both arms, (iii) cross-referencing — where an EMB SUT ships
real human tests (e.g. user-management) those corroborate the manual style. A human-tester replication
is named as future work. The RQ2 result (mutation-kill recall) does not depend on the manual arm being
human; RQ3 is therefore framed as a **methodology** comparison (systematic LLM generation vs structured
manual EP/BVA design).
