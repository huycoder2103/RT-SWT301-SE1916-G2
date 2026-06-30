# Outcome-Based Error Profile — Triggered vs. Missed (Gap-M extension)

**Member:** Nguyen Tien Dung (SE190034) · **Gap:** GAP-M (Metric) · **Date:** 2026-06-13

## 1. Why this exists

The RQ3 metric in the pilot counts **edge-case/error *scenarios authored*** per endpoint
(LLM 217 vs Manual 141, Wilcoxon p≈6e-7). That measures test **intent** — how many negative /
boundary / error-code tests a suite *writes*. It does **not** prove the suite actually *reaches*
the API's real error behaviour, nor does it say *which* behaviour each suite **misses**.

This document adds the **outcome** half of GAP-M: for every request each arm issues, we record the
**real HTTP status the SUT returns**, then per endpoint we report **how many 4xx/5xx each arm
triggered, on which input, and which error behaviours it missed**. This is exactly the question
“does the suite catch the error, which boundary, and what is missing?” — answered with live evidence.

## 2. Method (faithful, non-invasive)

1. Each SUT runs live (ncs:8080, features:8081, scs:8083; pristine `original.jar`, JDK 8).
2. A logging forward-proxy (`scripts/logproxy.py`) sits between the JUnit suite and the SUT and
   records `(arm, method, path, status)` for **every request the suite issues at runtime** — this
   captures dynamic/created-resource paths that static source parsing cannot.
3. `scripts/run_capture.sh` runs all 9 suites (3 SUTs × {llm, manual, evomaster}) through the proxy
   via Maven/JDK 17 → `results/raw/traffic.csv` (**785 real requests**).
4. `scripts/error_profile.py` maps each path to its OpenAPI operation, tallies 2xx/4xx/5xx per
   `(arm, endpoint)`, and computes triggered-vs-missed against the **answer key**.

**Answer key** = the union of every distinct `(endpoint, status≥400)` behaviour elicited by **any**
arm (LLM ∪ Manual ∪ EvoMaster). An arm **triggers** a behaviour if it produced that status on that
endpoint; it **misses** behaviours in the answer key it never produced. Requests to malformed /
undocumented paths (wrong arity, garbage) return 4xx but map to no documented operation; they are
reported in a separate **UNKNOWN** bucket and excluded from the answer key.

Captured status distribution: `200×318, 201×237, 204×43, 400×81, 404×31, 405×4, 406×1, 500×70`.

## 3. Headline result

| Arm | Triggered (documented error behaviours) | Missed |
|-----|----------------------------------------:|-------:|
| **LLM (Claude Sonnet 4.6)** | **31 / 31  (100%)** | **0** |
| Manual (human black-box)     | 22 / 31  (71%) | 9 |
| EvoMaster 6.0.0              | 18 / 31  (58%) | 13 |

Per SUT (answer-key size in parentheses):

| SUT | key | LLM | Manual | EvoMaster |
|-----|----:|----:|-------:|----------:|
| ncs (numeric)  | 6  | 6 | 6 | 5 |
| scs (string)   | 5  | 5 | **3** | 0 |
| features (CRUD)| 20 | 20 | **13** | 13 |

**The LLM suite reached every error behaviour any tool found; the human suite missed 9 and
EvoMaster 13.**

## 4. What the human suite missed (and the LLM caught)

| SUT | Endpoint | Missed status | Triggering input (LLM) |
|-----|----------|--------------:|------------------------|
| features | addRequiresConstraintToProduct | **500** | `POST /products/nonExistentProd_ARCP_N/constraints/requires` (constraint on a non-existent product **crashes the server**) |
| features | getAllProducts | 405 + 406 | `POST /products` (method) · `GET /products` with `Accept: text/plain` |
| features | getConfigurationActivedFeatures | 405 | `POST` to a GET-only path |
| features | getConfigurationsForProduct | 405 | `POST` to a GET-only path |
| features | getFeaturesForProduct | 405 | `POST` to a GET-only path |
| features | deleteFeatureOfProduct | 400 | `DELETE …/features/feat%00null` (null byte) |
| scs | fileSuffixUsingGET | 400 | `GET /api/filesuffix/home%2Fuser/file.txt` (encoded slash) |
| scs | ordered4UsingGET | 400 | `GET /api/ordered4/a%00b/c/d/e` (null byte) |

The most consequential is the **500 server crash** on `addRequiresConstraintToProduct`: a real
robustness bug that the human suite never provoked. The 405/406 family shows the LLM probing
HTTP-method and content-negotiation errors that the human partition-based suite skipped.

## 5. The three questions, answered with evidence

- **“How many 4xx/5xx are caught?”** → the per-endpoint `2xx/4xx/5xx` counts in
  `results/raw/error_profile.csv` (e.g. ncs `bessj` LLM = 5/6/0).
- **“Which boundary?”** → the exact triggering request (table above), e.g. `bessj/1/3.0 → 400`
  (n<2), `remainder/99999/2 → 400` (|a|>10000), `ordered4/a%00b → 400` (null byte).
- **“What is missing?”** → `results/raw/error_missed.csv` per `(endpoint, arm)`: LLM misses 0,
  Manual misses the 9 above, EvoMaster misses 13.

## 6. Threats to validity / honest limits

- **Answer key is a union, not exhaustive ground truth.** A behaviour that *all three* arms miss is
  invisible. Mitigation: three diverse oracles, including search-based EvoMaster. This bounds the
  claim to “relative to the strongest available reference,” not “absolute completeness.”
- **`features-service` is stateful** and the three arms ran sequentially against one instance, so
  2xx counts may carry cross-arm state. The **error behaviours the human missed are
  state-independent** (method-not-allowed, content-negotiation, crash on a non-existent resource),
  so the headline contrast is robust to this.
- **5 LLM ncs tests were unsendable** (`!@#/$%^` produced malformed URIs RestAssured rejected before
  any request) — counted as not-sent, not as passes. A minor LLM test-quality issue, disclosed.
- **EvoMaster looks weak here (58%)** because we replay its *fixed regression suite* via the proxy,
  which does not re-exercise its search engine. This measures *error-status diversity*, a different
  facet from RQ2 mutation recall (where EvoMaster’s value-oracle wins). The two results are
  complementary, not contradictory.

## 7. Reproduce

```bash
# 1) start the 3 SUTs (JDK 8) on 8080/8081/8083
# 2) capture real traffic through the proxy (JDK 17 + Maven):
bash experiment/scripts/run_capture.sh
# 3) build the profile + report:
python experiment/scripts/error_profile.py
# outputs: results/raw/{traffic.csv, error_profile.csv, error_missed.csv}
```
