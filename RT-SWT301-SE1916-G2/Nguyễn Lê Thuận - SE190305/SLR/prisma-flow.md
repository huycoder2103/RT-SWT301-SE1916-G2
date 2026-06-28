# PRISMA Flow Diagram — LLM for REST API Test Generation

[Records identified from database searching (N = 170)]
↓
[Records after duplicates removed (N = 166)]
↓
┌─────────────────────────────────────────┐
│  Screened title + abstract (N = 166)    │
│  └── Excluded (N = 155):                │
│       - EC: IC2 (Timeline): 79          │
│       - EC4 (Out of Domain): 61         │
│       - EC6 (Generation Focus): 4       │
│       - EC7 (Publication Type): 11      │
└─────────────────────────────────────────┘
↓ 11 papers pass
┌─────────────────────────────────────────┐
│  Full-text assessed (N = 11)            │
│  └── Excluded (N = 0)                   │
└─────────────────────────────────────────┘
↓
[Final included (N = 11)]

---

## Consistency Check

- Rows in `01_all_records.csv`: 166 (Matches N after dedup)
- Count(v1_decision = EXCLUDE): 155 (Matches Excluded V1)
- Count(v1_decision = INCLUDE): 11 (Matches Full-text assessed)
- Count(v2_decision = Include): 11 (Matches Final included)
