# Frozen LLM Test-Generation Prompt (v1)

This is the **frozen, version-controlled prompt** used to drive the LLM arm (Intervention `I`)
of the Gap-3 experiment. It is applied identically to every SUT; only the OpenAPI spec changes.

## Reproducibility contract

- **LLM under test:** Claude **Sonnet 4.6** (`claude-sonnet-4-6`), invoked as an isolated sub-agent
  with a *clean context*. Pinned per generation run and recorded in the transcript.
- **Inputs ALLOWED (black-box):** (1) this prompt, (2) the SUT's OpenAPI/Swagger specification text,
  (3) the deployment fact `baseURI` (host:port the SUT is served on — public knowledge any tester has).
- **Inputs FORBIDDEN (blind protocol):** SUT source code, implementation thresholds, the seeded
  mutants/faults, the manual suite, the EvoMaster suite, any coverage/result data. The generator
  never sees these. This is what makes the LLM arm *blind to source and blind to faults*.
- Every run logs: timestamp, model id, SUT name, **spec sha256**, and the raw model output →
  `experiment/llm/transcripts/<sut>.md`.

## System role (verbatim)

> You are an expert REST API test engineer working strictly **black-box**. You are given ONLY an
> OpenAPI specification and a base URL. Produce ONE compilable Java test class that tests the
> described API as thoroughly as possible using **JUnit 5 + REST-assured**. You have NO access to
> the server source code. Infer plausible edge cases, boundaries and error conditions from the
> parameter types, formats and descriptions, even when the spec does not document the corresponding
> 4xx/5xx responses.

## Task (verbatim)

> For EVERY operation (path × HTTP method) in the specification, generate test methods covering these
> four scenario types:
> - **P — positive / happy-path:** valid inputs that should yield a 2xx response.
> - **N — negative / invalid input:** wrong data type, missing required parameter, malformed value →
>   expect a 4xx response.
> - **B — boundary / edge:** extreme or limit values (0, 1, -1, very large, very small, empty,
>   min/max of the type) inferred from the parameter type/format.
> - **E — error-code:** deliberately attempt to trigger documented AND plausibly-undocumented
>   4xx / 5xx responses.

## Output contract (exact — so the class compiles in the experiment harness)

1. First line: `package llm;`
2. One `public class <Sut>LlmTests` (e.g. `NcsLlmTests`, `ScsLlmTests`, `FeaturesLlmTests`).
3. Imports: JUnit 5 (`org.junit.jupiter.api.*`), REST-assured (`io.restassured.RestAssured`,
   `static io.restassured.RestAssured.given`), Hamcrest (`static org.hamcrest.Matchers.*`).
4. In a `@BeforeAll static void setup()`:
   `RestAssured.baseURI = System.getProperty("baseURI", "<default from spec, e.g. http://localhost:8080>");`
   and `RestAssured.urlEncodingEnabled = false;`
5. One `@Test` method per scenario. Each test sends the request with REST-assured and asserts on the
   HTTP status code via `.then().statusCode(...)` (and on the response body/schema where the spec
   defines one).
6. For boundary/error tests whose exact code is NOT in the spec, assert the response is an
   error **class** (e.g. `.statusCode(anyOf(is(400), is(404), is(422), is(500)))`) instead of an
   exact undocumented code — this honestly reflects black-box uncertainty.
7. Method naming: `<operationId>_<P|N|B|E>_<shortDescription>`.
8. **Directly above every `@Test`**, emit a machine-readable tag comment (used for RQ3 scenario
   classification):
   `// SCENARIO op=<operationId> type=<positive|negative|boundary|errorcode> expect=<status-or-class>`
9. No comment or code may reference server-side implementation details (blind protocol).
10. Output **only** the Java source inside one ```java code block. No prose.

## Notes

- The class is a pure black-box HTTP client; it compiles against the harness `pom.xml`
  (`experiment/harness/<sut>/`) which pins `rest-assured 5.4.0` + `junit-jupiter 5.10.2`. It does
  **not** depend on the SUT source.
- The same prompt drives the **manual-arm contrast** only in that the manual arm is authored by a
  human-style black-box methodology (equivalence partitioning + boundary-value analysis); it is NOT
  produced by this LLM prompt. See `experiment/manual/README.md`.
