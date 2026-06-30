[Records từ database searching (N = 200)]   ← Tổng từ search-log.md (String A = 100, String B = 100 trên CORE.ac.uk)
↓
[Sau khi xóa duplicate (N = 179)]            ← = dòng trong 01_all_records.csv
↓
┌─────────────────────────────────────────┐
│  Screened title + abstract (N = 179)    │
│  └── Excluded (N = 132):                │
│       IC1=5 (Không phải tiếng Anh),     │
│       IC2=61 (Xuất bản trước 2018),     │
│       EC4=59 (Lạc đề: UI, Mobile, IoT), │
│       EC5=6 (Không liên quan Test Gen), │
│       IC5=1 (Dạng Survey)               │
└─────────────────────────────────────────┘
↓ 47 papers pass                           ← = INCLUDE + Unsure trong 02_after_screening_v1.csv
┌─────────────────────────────────────────┐
│  Full-text assessed (N = 47)            │
│  └── Excluded (N = 27):                 │
│       EC3=27 (Chưa đi sâu vào LLM/      │
│               không phải baseline tool) │
└─────────────────────────────────────────┘
↓
[Final included (N = 20)]                  ← = Include trong 03_final_included.csv
