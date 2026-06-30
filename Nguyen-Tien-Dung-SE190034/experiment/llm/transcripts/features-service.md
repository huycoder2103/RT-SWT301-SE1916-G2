# LLM generation transcript — features-service

| Field | Value |
|-------|-------|
| LLM under test | **Claude Sonnet 4.6** (`claude-sonnet-4-6`), Agent `model=sonnet` |
| Date | 2026-06-12 |
| Prompt | frozen template `experiment/llm/prompt_template.md` (v1), spec read from file |
| Input spec | `experiment/specs/features-service.openapi.json` (sha256 prefix `d5536f06a9d84630`) |
| **Blindness** | Sub-agent instructed to Read ONLY the spec file (no source, no web). Output contains no implementation-specific constants (pure black-box assertions / error-class `anyOf`). |
| Output | `experiment/harness/src/test/java/llm/FeaturesLlmTests.java` (verbatim model output, extracted from the persisted sub-agent result) |
| Size | **100 `@Test`** across the 18 operations (incl. POST/PUT/DELETE with JSON bodies) |

Raw sub-agent result persisted at the session tool-results path; the `.java` is a byte-for-byte copy of the model's output.
