# LLM generation transcript — rest-scs

| Field | Value |
|-------|-------|
| LLM under test | **Claude Sonnet 4.6** (`claude-sonnet-4-6`), Agent `model=sonnet` |
| Sub-agent id | `a5105fe0f6994eeac` |
| Date | 2026-06-12 |
| Prompt | frozen template `experiment/llm/prompt_template.md` (v1), spec read from file |
| Input spec | `experiment/specs/rest-scs.openapi.json` (sha256 prefix `8f28a9fbea6567df`) |
| **Blindness evidence** | **`tool_uses = 1`** — exactly one Read call, on the spec file. No source-code read, no web. → blind to source + faults. |
| Output | `experiment/harness/src/test/java/llm/ScsLlmTests.java` (verbatim model output) |
| Size | ~90 `@Test` across 12 operations |
| Usage | subagent_tokens=30987, duration=111s |
