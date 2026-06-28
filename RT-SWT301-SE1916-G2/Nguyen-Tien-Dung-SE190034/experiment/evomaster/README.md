# EvoMaster arm (Comparator C2)

## How the suites were generated

EvoMaster **6.0.0** in **black-box** mode, one run per SUT:

```
java -jar evomaster.jar --blackBox true \
  --bbSwaggerUrl <spec-url> --bbTargetUrl <base-url> \
  --outputFormat JAVA_JUNIT_5 --outputFolder raw/<sut> \
  --maxTime 120s --ratePerMinute 1200
```

Raw, unmodified EvoMaster output (incl. its HTML report + `report.json`) is kept under
`raw/<sut>/`. EvoMaster's own coverage report:

| SUT | EvoMaster endpoints 2xx | Tests saved | Potential faults flagged |
|-----|------------------------:|------------:|-------------------------:|
| ncs | 6/6 (100%) | 30 | 0 |
| scs | 11/11 (100%) | 27 | 1 |
| features | 14/18 (78%) | 30 | 18 |

(EvoMaster ran on JDK 17; the SUTs on JDK 8 — separate processes.)

## Adaptation into the common harness

`scripts/adapt_evomaster.py` performs a **mechanical, faithful** transform of each generated file
into `harness/src/test/java/evomaster/<Sut>Evo<Kind>Tests.java`:

1. prepend `package evomaster;`
2. rename the public class `EvoMaster_<kind>_Test` → `<Sut>Evo<Kind>Tests`
3. replace the hardcoded `baseUrlOfSut = "http://localhost:<port>"` with
   `System.getProperty("baseURI", "http://localhost:<port>")` so the same suite can be pointed at
   each mutant during RQ2.

**The request payloads and the assertions are left byte-for-byte unchanged.** This matters: EvoMaster
records *exact response values* as regression oracles (e.g. `body("'resultAsInt'", numberMatches(289))`),
which is a stronger oracle than the spec-derived status assertions of the LLM/Manual arms — a
methodological difference we report rather than normalise away.

## Why the `org.evomaster.*` shim classes exist

EvoMaster's generated tests statically import a few helper types
(`NumberMatcher`, `StringMatcher`, `SubStringMatcher`, `EMTestUtils`, `SutHandler`). Rather than put
EvoMaster's 88 MB shaded fat-jar on the harness classpath (which would clash with our pinned
REST-assured / Hamcrest), we provide **faithful, minimal re-implementations** under the same package
names in `harness/src/test/java/org/evomaster/...`:

| Shim | Methods actually used by the suites | Behaviour |
|------|--------------------------------------|-----------|
| `NumberMatcher` | `numberMatches(...)` (24×) | Hamcrest matcher: JSON number equals the recorded value (NaN-aware, 1e-9 rel. eps) |
| `EMTestUtils` | `resolveLocation(...)` (16×), `isValidURIorEmpty(...)` (10×) | resolve a Location header (or fall back to recorded URL); lenient URI validity |
| `StringMatcher`, `SubStringMatcher` | none (only imported) | empty, behaviour-neutral |
| `SutHandler` | none (only imported) | empty marker interface |

Only `numberMatches`, `resolveLocation`, `isValidURIorEmpty` are ever called (verified by grepping the
generated sources); their semantics are reproduced exactly, so the EvoMaster regression oracle is
preserved. This keeps the arm faithful while letting it run in the uniform harness.
