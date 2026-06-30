# LLM generation transcript — rest-ncs

| Field | Value |
|-------|-------|
| LLM under test | **Claude Sonnet 4.6** (`claude-sonnet-4-6`), Agent `model=sonnet` |
| Sub-agent id | `a95f3c55220c883ae` |
| Date | 2026-06-12 |
| Prompt | frozen template `experiment/llm/prompt_template.md` (v1) + inlined OpenAPI spec |
| Input spec | `experiment/specs/rest-ncs.openapi.json` (sha256 prefix `0b24da08e2715149`) |
| **Blindness evidence** | **`tool_uses = 0`** — the sub-agent issued NO tool calls, so it did NOT read the SUT source, the web, or any file. Its only input was the spec text. → blind to source + blind to seeded faults. |
| Output | `experiment/harness/src/test/java/llm/NcsLlmTests.java` (verbatim model output) |
| Size | 73 `@Test` methods across all 6 operations |
| Usage | subagent_tokens=25241, duration=78.5s |

The generator used `anyOf(...)` status assertions for boundary/undocumented cases — correct black-box
behaviour for a spec that documents only 200/401/403/404 while the implementation actually returns 400
on out-of-range numeric inputs (the spec≠impl gap that RQ3 targets).
