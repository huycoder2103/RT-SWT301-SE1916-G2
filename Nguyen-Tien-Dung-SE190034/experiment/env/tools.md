# Toolchain snapshot (pinned versions for reproducibility)

Captured 2026-06-12 on the experiment machine (Windows 11, x64).

| Component | Version / detail |
|-----------|------------------|
| OS | Windows 11 (build 26200), x64 |
| JDK (SUTs) | Eclipse Temurin **1.8.0_492** (`C:\Users\dungm\tools\jdk8\jdk8u492-b09`) |
| JDK (EvoMaster + harness) | Eclipse Temurin **17.0.19** |
| Maven | Apache Maven **3.9.16** |
| EvoMaster | **6.0.0** (GitHub release jar) |
| REST-assured | **5.4.0** (harness) |
| JUnit Jupiter | **5.10.2** (harness) |
| Hamcrest | **2.2** (harness) |
| maven-surefire-plugin | **3.2.5** |
| Python | **3.14.5** |
| scipy / statsmodels / pandas / numpy / matplotlib | 1.17.1 / 0.14.6 / 3.0.3 / 2.4.5 / 3.10.9 |
| EMB (SUT source) | EMResearch/EMB `jdk_8_maven`, parent `org.evomaster:evomaster-benchmark:4.3.0` (LGPL-3.0) |

## LLM under test
- **Claude Sonnet 4.6** (`claude-sonnet-4-6`), invoked as isolated sub-agents (clean context),
  spec-only input, frozen prompt `llm/prompt_template.md`. Per-SUT transcripts + blindness evidence
  (tool-use = 0/1) in `llm/transcripts/`.

## SUT ports
- rest-ncs → 8080 · features-service → 8081 · rest-scs → 8083 (each a standalone Spring-Boot fat jar).

## Process split
- SUTs build & run on **JDK 8**; EvoMaster 6.0.0 and the REST-assured harness run on **JDK 17**
  (EvoMaster's classes are compiled for class-file v61 = Java 17). They communicate over HTTP only.
