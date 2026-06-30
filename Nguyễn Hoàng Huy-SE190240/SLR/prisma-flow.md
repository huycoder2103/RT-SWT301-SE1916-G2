# PRISMA Flow Diagram — LLM for REST API Test Generation

---

```
[Records từ Google Scholar searching (N = 189)]
    String A: 100 papers (10 trang đầu)
    String B: 89 papers (toàn bộ)
            ↓
[Sau khi xóa duplicate (N = 138)]              
    Số bị loại trùng: 51
            ↓
┌─────────────────────────────────────────────────┐
│  Screened title + abstract (N = 138)            │
│  └── Excluded (N = 108):                        │
│        EC4 (out of domain)          = 39        │
│        EC6 (not about generation)   = 25        │
│        EC7 (thesis/non-peer-review) = 18        │
│        IC5 (survey/no experiment)   = 12        │
│        EC5 (out of phase)           =  5        │
│        EC3 (short/book/poster)      =  5        │
│        IC4 (no LLM used)            =  2        │
│        EC1 (duplicate)              =  2        │
└─────────────────────────────────────────────────┘
            ↓
    22 INCLUDE + 8 Unsure = 30 papers pass
            ↓
┌─────────────────────────────────────────────────┐
│  Full-text assessed (N = 30)                    │
│  └── Excluded (N = 17):                         │
│        EC1 (duplicate/superseded)   =  1        │
│        IC5 (redundant approach,     = 16        │
│             covered by other                    │
│             included papers)                    │
└─────────────────────────────────────────────────┘
            ↓
[Final included in evidence table (N = 13)]       
```

---
