# Dataset gốc — EvoMaster Benchmark (EMB)

**Nguồn:** https://github.com/EMResearch/EMB (EMResearch organization, public repo)

**License:** LGPL v3 — cho phép dùng nghiên cứu, không cần xin phép

**3 REST APIs được dùng (N = 35 operations):**

| SUT | Operations | Loại API |
|---|---|---|
| `rest-ncs` | 6 | Numerical computation services |
| `rest-scs` | 11 | String computation services |
| `features-service` | 18 | Feature management |

Counts được verify dựa trên `EMB/statistics/table_emb.md` trong upstream repo.

**Build & deploy:**
- JDK 8 cho SUTs (Maven fat-jar)
- JDK 17 cho experiment harness + EvoMaster 6.0.0
- Local deploy (CPU, không cần GPU)

**Mutation ground truth:**
- Operators: standard PIT/Offutt families — relational, arithmetic, negate-boundary
- Áp dụng lên: controller + core-logic classes
- Chỉ giữ mutants compile được
- Catalog: `data/faults/<sut>/catalog.json` (sau khi migrate)
- **Pilot N = 133 mutants** (ncs 70, scs 59, features 4)

---

## Cấu trúc cột raw output (verified từ pilot)

### `<sut>_kills.csv` — kill matrix per mutant per arm
| Cột | Ý nghĩa |
|---|---|
| `mutant_id` | ID mutant (vd `m001`, `m002`, ...) |
| `arm` | `llm` / `manual` / `evomaster` |
| `killed` | 0 / 1 — arm có kill được mutant này không |
| `n_oracle` | tổng số oracle (test assertion) arm này có cho SUT |
| `n_now_failing_oracle` | số oracle fail trên mutant (kill iff > 0 sau khi pass trên gốc) |

### `<sut>_recall.json` — aggregate Recall per arm
```json
{
  "llm":       { "killed": N, "total": M, "recall": K/M },
  "manual":    { "killed": N, "total": M, "recall": K/M },
  "evomaster": { "killed": N, "total": M, "recall": K/M }
}
```

### `traffic.csv` — log mọi HTTP request từ logging proxy
| Cột | Ý nghĩa |
|---|---|
| `tag` | `<sut>:<arm>` (vd `ncs:llm`) |
| `method` | HTTP method (GET/POST/PUT/DELETE) |
| `path` | endpoint path đã được gọi |
| `status` | real HTTP status từ SUT |

### `scenarios.csv` — parse từ `// SCENARIO type=` tags trong JUnit code
| Cột | Ý nghĩa |
|---|---|
| `sut` | tên SUT (ncs / scs / features) |
| `arm` | `llm` / `manual` |
| `op` | operation name |
| `type` | loại scenario (`boundary` / `errorcode` / ...) |
| `count` | số lần xuất hiện |

### `coverage.csv` — endpoint coverage per arm per SUT
| Cột | Ý nghĩa |
|---|---|
| `sut` | tên SUT |
| `arm` | `llm` / `manual` |
| `ops_covered` | số operation có ≥ 1 test |
| `ops_total` | tổng số operation |
| `coverage_pct` | %  coverage |

### `error_profile.csv` — phân bố HTTP status per op per arm
| Cột | Ý nghĩa |
|---|---|
| `sut` | tên SUT |
| `arm` | `llm` / `manual` / `evomaster` |
| `op` | operation name |
| `n_2xx`, `n_4xx`, `n_5xx` | số response từng class |

### `error_missed.csv` — triggered vs missed error behaviour per op
| Cột | Ý nghĩa |
|---|---|
| `sut`, `op` | identifier endpoint |
| `answer_key_codes` | error code đáng lẽ phải trigger (từ error-surface-baseline) |
| `arm` | `llm` / `manual` / `evomaster` |
| `triggered` | mã đã trigger (vd `404`) hoặc `-` |
| `missed` | mã bị miss (vd `404`) hoặc `-` |

---

**Ngày clone:** 
**EMB upstream commit hash:** 

**Ghi chú:** Tool-independent code-derived error-surface baseline được sinh bởi `scripts/error_surface.py` — output `results/error-surface-baseline.json` — đây là "what can fail" map per endpoint (declared / framework / potential 4xx/5xx).
