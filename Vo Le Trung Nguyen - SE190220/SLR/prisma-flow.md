# PRISMA Flow Diagram — LLM REST API Test Generation

[Records từ Open Alex searching (N = 263)]
↓
[Sau khi xóa duplicate (N = 206)]
↓
┌─────────────────────────────────────────┐
│ Screened title + abstract (N = 206)
│ └── Excluded (N = 174): 
    EC3 - Dataset/software, not research paper (1), EC3 - Replication package/dataset (2), 
    EC4 - 5G network (1), EC4 - Blockchain (1), EC4 - CPS anomaly detection (1), EC4 - Cloud emulators (1), EC4 - Code benchmarking (1), EC4 - Code generation (8), EC4 - DevOps general (1), EC4 - Fuzz driver generation for libraries (1), EC4 - GUI/mobile testing (5), EC4 - General survey, not REST API focused (9), EC4 - Low-code platforms (1), EC4 - Metamorphic testing general (2), EC4 - Network protocol fuzzing (1), EC4 - No REST API testing context (103), EC4 - Payload/fuzzer identification (1), EC4 - Requirements engineering (1), EC4 - SQA framework (1), EC4 - SQA general (1), EC4 - Security/pen testing (2), EC4 - Test oracle general (1), EC4 - Unit testing, not REST API (10), EC4 - Vibe coding review (2), 
    EC5 - Test flakiness (2), 
    IC1 - Non-English (3), 
    IC4 - No LLM involvement (10), 
    IC5 - Survey/review without empirical (1)
└─────────────────────────────────────────┘
↓ 32 papers pass
┌─────────────────────────────────────────┐
│ Full-text assessed (N = 32)
│ └── Excluded (N = 4): IC4 - LLM not actually used for REST API testing (4)
└─────────────────────────────────────────┘
↓
[Final included (N = 28)]

## Kiểm tra nhất quán
Rows trong 01 CSV = 206 ✓
Count(v1_decision = EXCLUDE) = 174 ✓
Count(v1 = INCLUDE + Unsure) = 32 ✓
Count(v2_decision = Include) = 28 ✓
