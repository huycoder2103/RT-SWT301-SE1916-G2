# Nội dung thuyết trình — LLM cho Sinh Test REST API (SLR & Thiết kế thí nghiệm)

**Môn:** SWT301 (Software Testing) · **Topic:** SE1916 · **Nhóm 2**
**Thành viên:** Nguyễn Tiến Dũng — SE190034
**Bộ slide web:** `presentation/slides/index.html` (mở bằng trình duyệt, chạy offline)
**Bằng chứng:** 13 PDF gốc trong `presentation/papers/` · trích dẫn đã verify trong `presentation/citations-raw.json`

> **Cách dùng tài liệu này:** đây là kịch bản nói cho từng slide. Cột *Lời nói* là phần thuyết trình; *Trên slide* tóm tắt nội dung hiển thị; *Trích dẫn* là nguồn để trả lời khi bị hỏi. Tổng thời lượng gợi ý: **18–22 phút** trình bày + Q&A. Bản đầy đủ của mỗi note cũng nằm trong slide (nhấn phím **S**).

---

## Thông điệp xuyên suốt (học thuộc 1 câu)

> *"Test REST API tự động bị chặn ở ~52% code coverage và tool còn thua người (EvoMaster 41% vs 82%); LLM hứa hẹn vượt qua; em làm SLR sàng ~280→13 paper chất lượng cao, phát hiện 3 khoảng trống chưa ai lấp, và đề xuất thí nghiệm trên 3 EMB API có lỗi gieo sẵn để đóng cả 3."*

Mọi con số trong bài đều **truy vết được tới paper · trang · câu**. Đó là thứ khiến bài không thể bị bắt bẻ.

---

# PHẦN MỞ ĐẦU

### Slide 1 — Trang bìa
- **Trên slide:** Tên topic, thành viên, N=13 (2019–2026), QA 5.73/6, "trích dẫn verbatim có page/dòng".
- **Lời nói:** "Kính chào hội đồng, em là Nguyễn Tiến Dũng, SE190034. Em trình bày phần nghiên cứu cá nhân trong topic nhóm: *Dùng LLM sinh test case cho REST API*. Đây là một Systematic Literature Review — mỗi con số em nêu đều trích dẫn được tới tận trang trong PDF gốc, và em đã tải sẵn 13 PDF để hội đồng kiểm chứng. Mục tiêu: chỉ ra một khoảng trống mà 13 paper chất lượng cao đều bỏ ngỏ, rồi đề xuất thí nghiệm lấp nó."

### Slide 2 — Bản đồ bài thuyết trình
- **Trên slide:** 6 bước (Bối cảnh → SLR → 13 bằng chứng → GAP → RQ → Giả thuyết/Thí nghiệm) + Kết luận.
- **Lời nói:** "Cả bài là một chuỗi nhân–quả. Điểm khác biệt: mỗi bước đều có nguồn. Khi tới phần GAP, em không nói *em thấy thiếu* mà chỉ vào đúng cột trong ma trận để chứng minh nó thiếu."

---

# PHẦN 1 — BỐI CẢNH & NỀN TẢNG (slide 3–8)

### Slide 3 — Divider Phần 1
- **Lời nói:** "Phần 1 trả lời 4 câu: REST API là gì, test nó khó ở đâu, công cụ trước-LLM làm tới đâu, và vì sao LLM hứa hẹn."

### Slide 4 — REST API & OpenAPI là gì
- **Trên slide:** method (GET/POST/PUT/DELETE), status code (2xx/4xx/5xx), OpenAPI spec + ví dụ endpoint với `minimum:1` và `404`.
- **Lời nói:** "REST API là cách hai phần mềm nói chuyện qua HTTP. Mỗi tài nguyên có URL, thao tác bằng method, server trả status code. OpenAPI là file đặc tả — đầu vào chuẩn cho 11/13 paper. Chỉ vào ví dụ: dòng `minimum:1` và mã `404` chính là chỗ sinh edge case — gửi id=0 để buộc 4xx. Cả bài xoáy vào việc *ai sinh được edge case này*."

### Slide 5 — Vì sao sinh test REST API khó
- **Trên slide:** 3 thách thức (không gian input vô hạn · phụ thuộc & trạng thái · bài toán oracle) + ô **2 loại coverage**.
- **Lời nói:** "Ba thách thức khiến đây là bài toán nghiên cứu mở. Quan trọng nhất — **nói chậm** — có hai loại độ phủ: (a) *endpoint coverage* = % endpoint đã gọi; (b) *code coverage* = % dòng/nhánh code chạy. Loại (a) có thể rất cao, loại (b) thấp hơn nhiều. Đây là chìa khoá của RQ1."

### Slide 6 — 4 trường phái trước LLM
- **Trên slide:** EvoMaster (search-based), Morest (model-based), RESTler (fuzzing), DeepREST (RL). Trần ~52% line; EvoMaster thua tay 41% vs 82%.
- **Lời nói:** "Trước LLM có 4 trường phái. Dù thông minh, chúng bị chặn ở ~52% line coverage, và EvoMaster còn sinh test phủ *thấp hơn người viết tay* — 41% so với 82%. Đó là lằn ranh LLM hứa hẹn vượt qua."
- **Trích dẫn:** trần 52.76% → No-Time-to-Rest **#11 p.5**; 41% vs 82% → EvoMaster **#10 p.11**.

### Slide 7 — Vì sao LLM hứa hẹn
- **Trên slide:** 4 năng lực (đọc NL · sinh giá trị thật · suy luận dependency · sinh script chạy được) + cái giá (hallucination, cost, oracle).
- **Lời nói:** "LLM làm được 4 việc tool cũ không: đọc mô tả tiếng người, sinh giá trị giống thật, suy luận phụ thuộc, sinh script chạy được. Nhưng có giá: ảo giác, chi phí, oracle vẫn không chắc. Nên câu hỏi không phải *LLM có dùng được không* mà *hiệu quả tới mức nào, so với người và EvoMaster, trên thước đo có ground truth*."

### Slide 8 — Câu hỏi nghiên cứu ban đầu
- **Trên slide:** RQ thô (≥90% coverage, ≥2 bug) + 2 điểm mơ hồ (LLM nào? baseline & ngưỡng từ đâu?).
- **Lời nói:** "Đây là RQ ban đầu. Nó có 2 điểm mơ hồ: *LLM nào* và *baseline/ngưỡng từ đâu*. Vì vậy không thể nhảy thẳng vào làm — phải khảo sát có hệ thống. Đó là lý do tồn tại của SLR ở Phần 2. Em không tự đặt ngưỡng rồi đi chứng minh — em tinh chỉnh RQ dựa trên bằng chứng."

---

# PHẦN 2 — PHƯƠNG PHÁP SLR (slide 9–16)

### Slide 9 — Divider Phần 2
- **Lời nói:** "Phần 2 chứng minh tính hệ thống & tái lập: bất kỳ ai chạy lại quy trình cũng ra cùng 13 paper."

### Slide 10 — SLR là gì + 6 bước
- **Lời nói:** "SLR (chuẩn Kitchenham) là khảo sát tài liệu minh bạch, tái lập, kiểm toán được — đối lập với đọc vu vơ. 6 bước: PICO → search string → sàng IC/EC → đánh giá chất lượng → trích xuất → tổng hợp GAP. Nếu chỉ Google vài bài, khoảng trống tìm được có thể chỉ do bỏ sót. SLR đảm bảo gap là thật."

### Slide 11 — PICO & 2 search strings
- **Lời nói:** "PICO là khung câu hỏi. 2 search string suy ra trực tiếp từ PICO: String 1 bắt paper LLM, String 2 chủ động kéo về baseline kinh điển — vì C trong PICO là *so với EvoMaster*."
- **Trích dẫn:** search-log.md §1.

### Slide 12 — 6 database + bộ lọc
- **Lời nói:** "6 nguồn: Google Scholar (recall rộng), arXiv (preprint sớm), IEEE/ACM/Springer (bản peer-reviewed), Semantic Scholar (đối chiếu). Lọc: English (IC1), ≥2018 (IC2), phải có PDF hợp pháp (EC2). Mọi record có URL + DOI để tái kiểm."

### Slide 13 — Inclusion Criteria (IC1–IC5)
- **Lời nói:** "5 tiêu chí đưa vào, phải thoả cả 5. Điểm tinh tế là **IC4**: cố ý giữ baseline non-LLM, vì câu hỏi so LLM *với* EvoMaster — nếu loại hết thì không có gì để so."

### Slide 14 — Exclusion Criteria (EC1–EC5)
- **Lời nói:** "5 tiêu chí loại. EC4 *ngược hướng* hay nhầm: ví dụ paper 'RestGPT — kết nối LLM với REST API' bị loại vì dùng API *phục vụ* LLM, ngược với đề tài. Đừng nhầm với RESTGPT in hoa là paper #1 — chi tiết cho thấy em đọc kỹ."

### Slide 15 — Sơ đồ PRISMA
- **Trên slide:** phễu ~280 → 30 → (−7) → 23 → (−10) → 13, mỗi exclusion có mã IC/EC.
- **Lời nói:** "Đây là xương sống Phần 2. ~280 thô → 30 sau khử trùng → loại 7 (vòng abstract, EC4/EC5) → 23 → loại 10 (vòng full-text) → 13. Mỗi lần loại có mã IC/EC nên ai cũng kiểm lại được, và phép đối soát số học khớp 100%."
- **Trích dẫn:** prisma-flow.md. ~280 = ước lượng Google Scholar, có query Q1/Q2 tái lập + arXiv cross-check 26.

### Slide 16 — Đánh giá chất lượng (Kitchenham)
- **Trên slide:** QA1–6, TB 5.73/6, min 5.0, 13/13 vượt ngưỡng.
- **Lời nói:** "Không chỉ *liên quan* mà còn *đáng tin*. Trung bình 5.73/6. Điểm phòng thủ then chốt: những paper *không* so với thủ công và *chỉ đếm* lỗi đều là paper **chất lượng cao**. Nên gap là lỗ hổng thiết kế trong nghiên cứu mạnh, không phải do paper yếu."

---

# PHẦN 3 — 13 BẰNG CHỨNG (slide 17–33)

> **Cách trình bày mỗi paper:** trái = số liệu; phải = câu trích nguyên văn + chip trích dẫn (paper · trang) + ô WHY (lý do tại sao). Chỉ nhấn 1–2 con số đắt nhất mỗi paper. **104 trích dẫn đã verify, 102/104 khớp tuyệt đối.**

### Slide 17 — Divider Phần 3
### Slide 18 — Tổng quan 13 paper
- **Lời nói:** "Bảng tổng quan. Hai quan sát đẻ ra GAP: (1) họ GPT áp đảo 6/9 paper LLM, chỉ #5 có Claude và nó thắng; (2) cột *so với thủ công* sẽ trống ở mọi paper LLM."

### Slide 19 — #1 RESTGPT (GPT-3.5)
- **Số liệu:** 97% precision trích luật (NLP2REST 79%); 72.68% input hợp lệ vs ARTE 16.93% (+329%).
- **WHY:** LLM hiểu ngữ nghĩa mô tả NL (sort_order → ASC/DESC) mà NLP từ-khoá bỏ sót.
- **Trích dẫn:** "precision of 97% surpasses … NLP2REST … 79%" — **#1 arXiv:2312.00894 p.4**; "ARTE 16.93%, RESTGPT 72.68%" **p.4 Table 2**.

### Slide 20 — #2 KAT (GPT-3.5-turbo-1106, t=0)
- **Số liệu:** +15.7% overall, +18.1% 2xx, +8.4% 4xx vs RestTestGen; +24 mã ẩn; 94 vs 119 FP.
- **WHY:** GPT dựng ODG bắc cầu khi tên không khớp (output `id` ↔ input `flightId`); heuristic so-tên bó tay.
- **Trích dẫn:** "15.7% increase in overall … 18.1% … 2xx … 8.4% … 4xx" — **#2 arXiv:2407.10227 p.8**; "+24 status codes" **p.10**.

### Slide 21 — #3 RESTSpecIT (DeepSeek/GPT, masking)
- **Số liệu:** route 88.6% (DeepSeek), param 89.25%, $0.004/run, 5xx ở 4 API. **Lưu ý: đây là route discovery, KHÁC code coverage.**
- **WHY:** "prompt masking" che một phần request → hỏi LLM điền → response 2xx → tách thành route/param → bồi vào OAS. Vừa suy ra spec vừa test.
- **Trích dẫn:** "DeepSeek … (88.62%) … GPT-4.1 (81.16%) … GPT-3.5 (79.84%)" — **#3 arXiv:2402.05102 p.14**; param 89.25% **p.16**; 5xx **p.22**.

### Slide 22 — #4 APITestGenie (GPT-4-Turbo, RAG)
- **Số liệu:** 57.3% script hợp lệ 1 lần → 80% trong 3 lần; 126s, €0.37/script; 12 defect; 19 hallucination.
- **WHY:** retry cộng dồn xác suất; 30.7% lỗi do hallucination (import sai, bịa response) = rủi ro LLM.
- **Trích dẫn:** "57.3% with one attempt to 80% with three attempts" — **#4 arXiv:2409.03838 p.4**; Table 2 (12/19) **p.5**.

### Slide 23 — #5 RestTSLLM (Claude 3.5 thắng) ★
- **Số liệu:** Claude 3.5 Sonnet — 100% success (230 test, 0 fail), 71.7% branch, 40.8% mutation. Tốt nhất trong 7 LLM.
- **★ ĐIỂM CHÍNH TRỰC:** evidence-table từng đánh dấu † (3 số chưa verify được). Bài này **tải PDF gốc và tìm thấy chúng nguyên vẹn ở Table 3, trang 9** → gỡ được nghi ngờ.
- **WHY:** TSL (Test Specification Language) làm tầng trung gian — Prompt 1 đổi OpenAPI→TSL, Prompt 2 đổi TSL→xUnit. Chia để trị → chất lượng cao hơn.
- **Trích dẫn:** "Claude 3.5 Sonnet 70,9% 100% 71,7% 40,8%" — **#5 arXiv:2509.05540 p.9 Table 3**; "outperformed all other models" **p.1 abstract**.

### Slide 24 — #6 AutoRestTest (GPT-3.5 + MARL + SPDG)
- **Số liệu:** 58.3% method/line, 32.1% branch; 42 lỗi 500 vs EvoMaster 20; **ablation: bỏ LLM → coverage rớt 10.9–12.8%.**
- **WHY (đắt nhất corpus):** ablation chứng minh nhân–quả — chính LLM tạo ra cải thiện, không phải MARL/SPDG đơn thuần.
- **Trích dẫn:** "42 500 … Errors … EvoMaster and MoRest 20 … RESTler 14" — **#6 arXiv:2411.07098 p.9**; ablation **p.10**.

### Slide 25 — #7 LlamaRestTest (Llama3-8B fine-tuned)
- **Số liệu:** 204 fault vs EvoMaster 130; 72.44% input hợp lệ vs RESTGPT 68.82%; IPD 12/17 vs RESTGPT 9.
- **WHY:** model nhỏ fine-tune trên 1.8M ví dụ → đánh bại GPT; quantize 8-bit (48.9s→36.9s/rule) → test nhiều hơn trong 1h.
- **Trích dẫn:** "204 faults in 10 runs … 74 more than EvoMaster (130)" — **#7 arXiv:2501.08598 p.11**; 72.44% vs 68.82% **p.12**.

### Slide 26 — #8 LogiAgent (GPT-4o-mini, 3 agent)
- **Số liệu:** 71.78% line (cao nhất nhóm LLM); 234 lỗi logic (139 bug + 95 enh) ở 66.19% accuracy; 33.81% FP; 49 crash.
- **WHY:** Response Validator dùng LLM làm *oracle ngữ nghĩa* — bắt lỗi trả 200 nhưng sai (vượt khỏi đếm 5xx). Nhưng 33.81% FP do hallucination = oracle chưa giải triệt để.
- **Trích dẫn:** "234 (66.19%) … 139 … 95 … 115 (33.81%) false positives" — **#8 arXiv:2503.15079 p.8**; coverage **p.9**; (49 crash = tổng Table 3 p.9 — *xem slide chính trực*).

### Slide 27 — #9 RESTifAI (GPT-4.1-mini)
- **Số liệu:** 128/134 operations OhSome (≈95.5%) vs AutoRestTest 33; −37% token (32,370 vs 51,188); 60.87% failure = bug thật.
- **WHY:** dùng LLM chọn lọc — dựng happy-path rồi *suy ra* negative case từ chính chuỗi đó → ít prompt → 37% rẻ hơn.
- **★ Quan trọng GAP-3:** 95.5% operation coverage chứng minh ngưỡng ≥90% endpoint là KHẢ THI. Nên RQ1 không hỏi "có đạt không" mà "có đạt trên EMB lỗi-gieo-sẵn không + loại endpoint nào bị bỏ".
- **Trích dẫn:** "128 out of 134 … vs … 33 … AutoRestTest" — **#9 arXiv:2512.08706 p.3**; 60.87% **p.4**.

### Slide 28 — 4 baseline kinh điển (#10–#13)
- **Lời nói:** "Theo IC4, giữ tool non-LLM làm mốc. Hai cái quan trọng nhất: EvoMaster (#10) — đối thủ + so test tay; No-Time-to-Rest (#11) — EMB + trần 52%. Hai cái này đẻ ra thiết kế thí nghiệm."

### Slide 29 — #10 EvoMaster (paper then chốt) ★
- **Số liệu:** 38 bug thật; nhưng gen 41% < tay 82%, 18% vs 47%, 20% vs 43%.
- **WHY:** GA không vượt được ràng buộc string/DB/external; dev viết tay có tri thức miền nên thoả thẳng.
- **★ Ý nghĩa GAP:** đây là tool DUY NHẤT so với test tay — và thua. Câu hỏi 2026: LLM có lật ngược được không? Nhưng chưa ai đặt LLM/người/EvoMaster cùng bàn cân → GAP-1.
- **Trích dẫn:** "18% and 41% statement coverage … lower than … existing test cases" — **#10 arXiv:1901.01538 p.11**; "38 real faults" **p.1**.

### Slide 30 — #11 No Time to Rest Yet (trần 52% + EMB) ★
- **Số liệu:** EvoMaster-WB tốt nhất 52.76% line; không tool nào > 53%; 20 service = EMB; tương quan coverage↔500 = 0.7881.
- **WHY:** 2 nút thắt — sinh giá trị tham số hợp lệ kém + phát hiện dependency yếu. Đúng 2 chỗ LLM mạnh.
- **Trích dẫn:** "EvoMasterWB … less than 53% line … 37% branch … 53% method" — **#11 arXiv:2204.08348 p.5–6**; "20 web services" **p.4**; 0.7881 **p.8**.

### Slide 31 — #12 Morest (model-based RPG)
- **Số liệu:** +26–103% coverage; 44 bug (13 mới, 2 ở Bitbucket).
- **WHY:** RPG có cạnh property-equivalence nối 2 schema khác tên (Order.petId ↔ Pet.id) → dựng chuỗi gọi sâu mà đồ thị tĩnh không tạo nổi.
- **Trích dẫn:** "152.66%-232.45% more … 26.16%-103.24% … 40.64%-215.94% … bugs" — **#12 arXiv:2204.12148 p.1**.

### Slide 32 — #13 DeepREST (deep RL)
- **Số liệu:** +17–77% branch; +25–67% fault; Wilcoxon p<0.05.
- **WHY:** học ràng buộc ẩn (thứ tự + giá trị) ngoài OpenAPI. **Dùng Wilcoxon + 10 lần chạy + α=0.05 — đúng khuôn mẫu Phần 6 của em.**
- **Trích dẫn:** "branch coverage … spans from 17% … to 77%" — **#13 arXiv:2408.08594 p.8**; Wilcoxon α=0.05 **p.8**.

### Slide 33 — Hai loại coverage (chốt setup GAP) ★
- **Lời nói (nói chậm):** "Slide bản lề. Ngăn câu phản biện 'đã đạt 90% coverage rồi'. Có 2 loại: endpoint coverage (loại A) đã ≥90% — RESTifAI 95.5%; code coverage (loại B) vẫn ~52–72%. RQ1 đo *endpoint* coverage NHƯNG thêm 2 điều chưa ai làm: kiểm trên EMB lỗi-gieo-sẵn + bóc tách theo loại endpoint."

---

# PHẦN 4 — KHOẢNG TRỐNG (slide 34–39)

### Slide 34 — Divider Phần 4
### Slide 35 — Ma trận so sánh chéo (GAP hiện hình) ★★
- **Lời nói (đắt nhất bài):** "Đừng đọc từng ô — chỉ vào 2 cột phải. *So với thủ công*: chỉ #10 Yes (và thua). *Recall trên lỗi gieo sẵn*: đỏ hết, chỉ #5 gần đúng bằng mutation score. Cả 13 paper, không bài nào đặt LLM/người/EvoMaster cùng bàn cân có ground truth. Khoảng trống hiện ra thành cột trống, không phải ý kiến của em."
- **Trích dẫn:** evidence-table.md mục C.

### Slide 36 — GAP-1 (Comparison)
- **Lời nói:** "LLM so với tool thì có (và thắng 42 vs 20, 204 vs 130); tool so với người thì có 1 (EvoMaster, và thua). Nhưng tam giác LLM–người–EvoMaster chưa khép. Nếu LLM chỉ hơn tool mà chưa chắc hơn người, lời hứa 'thay thế test tay' chưa được kiểm chứng. RQ2 khép tam giác này."

### Slide 37 — GAP-2 (Ground truth / Recall)
- **Lời nói:** "Fault chỉ là số đếm trên hệ thống sống — 38, 44, 42, 204, 49… Vì tổng số lỗi là ẩn số → không ai tính được Recall. Ví von: nói tôi bắt 42 con cá là vô nghĩa nếu không biết hồ có bao nhiêu con. Chỉ khi gieo lỗi biết trước mới tính được Recall. RQ2 đóng gap này."

### Slide 38 — GAP-3 (Metric / edge-case)
- **Lời nói:** "Chỉ #2 tách 2xx/4xx, chỉ #3 báo 5xx. Không ai đo số kịch bản edge-case/endpoint, cũng không ai bóc tách theo loại endpoint. Coverage tổng 'che' việc API bỏ sót đúng các endpoint nhạy cảm (auth, error-handling). RQ1 + RQ3 đóng gap này."

### Slide 39 — Tuyên bố GAP hợp nhất + đóng góp
- **Lời nói:** "3 gap không rời rạc — chúng hợp thành MỘT thiết kế thí nghiệm: EMB + lỗi gieo sẵn + 3 generator. Đóng góp: tool + GitHub repo + báo cáo đánh giá trên 3 EMB API có bản lỗi gieo sẵn, trả lời RQ1/RQ2/RQ3."
- **Trích dẫn:** gap-statement.md §3.

---

# PHẦN 5 — TỪ GAP TỚI RQ (slide 40–43)

### Slide 40 — Divider Phần 5
### Slide 41 — Nhật ký tinh chỉnh (4 thay đổi)
- **Lời nói (câu phòng thủ vàng):** "Em không tự đặt ngưỡng rồi đi chứng minh. 4 thay đổi so với RQ ban đầu đều có cột *nguồn* chỉ về paper: thêm EvoMaster (baseline phổ biến nhất), dataset EMB + gieo lỗi, chọn GPT (thống trị literature), metric edge-case. Mỗi tinh chỉnh truy vết về evidence table."

### Slide 42 — PICO thí nghiệm
- **Lời nói:** "PICO khớp 1-1 với 3 gap: C ba chiều ↔ GAP-1; P có lỗi gieo sẵn ↔ GAP-2; O3 + bóc loại endpoint ↔ GAP-3."

### Slide 43 — Main RQ + RQ1/RQ2/RQ3
- **Main RQ:** "LLM sinh test từ OpenAPI hiệu quả tới mức nào, so với thủ công và EvoMaster, trên bản API có lỗi gieo sẵn?"
- **Lời nói:** "3 RQ không trùng: RQ1 đo *phủ* (+loại bị bỏ), RQ2 đo *bắt lỗi có ground truth* 3 chiều, RQ3 đo *chất lượng edge-case*. Cùng nhau đóng cả 3 gap."

---

# PHẦN 6 — GIẢ THUYẾT & THÍ NGHIỆM (slide 44–48)

### Slide 44 — Divider Phần 6
### Slide 45 — RQ1: H0/H1 + Wilcoxon một mẫu
- **H0:** coverage ≤ 90%. **H1:** > 90%. **Test:** Wilcoxon signed-rank một mẫu (phi tham số, mẫu nhỏ).
- **Lời nói:** "Ngưỡng 90% có nguồn — target môn + #9 chứng minh khả thi; điểm mới = kiểm trên EMB lỗi-gieo-sẵn + bóc loại endpoint."

### Slide 46 — RQ2: LLM vs Thủ công vs EvoMaster + Friedman (gap chính)
- **H0:** LLM ≤ max(others). **H1:** LLM > cả hai. **Test:** Friedman + post-hoc Wilcoxon (Holm) + McNemar per-fault.
- **Lời nói:** "Đây là phép so ĐẦU TIÊN đặt LLM/người/EvoMaster trên cùng bộ lỗi-gieo-sẵn → đóng GAP-1 + GAP-2. Friedman vì 3 nhóm phụ thuộc, phi tham số. Chỉ 3 API → thành thật về power thấp, nên bổ sung McNemar per-fault + effect size."

### Slide 47 — RQ3: LLM vs Thủ công + Wilcoxon ghép cặp
- **H0:** edge-case/endpoint LLM ≤ tay. **H1:** > tay. **Test:** Wilcoxon signed-rank ghép cặp qua endpoint.
- **Lời nói:** "Mỗi endpoint là một đơn vị so sánh tự nhiên → ghép cặp kiểm soát biến nhiễu. Không paper nào đo metric này → đóng GAP-3."

### Slide 48 — Thiết kế thí nghiệm + đóng góp
- **Lời nói:** "Một bàn cân (3 API EMB + lỗi gieo sẵn), 3 generator (LLM/tay/EvoMaster), đo O1/O2/O3, α=0.05. Đóng góp: tool+repo + báo cáo + phép so 3 chiều đầu tiên + hồ sơ endpoint miss. Dùng đúng EMB + EvoMaster mà literature đã chuẩn hoá → kết quả so sánh được."

---

# KẾT LUẬN (slide 49–52)

### Slide 49 — Divider Kết luận
### Slide 50 — Tóm tắt chuỗi nhân–quả
- **Lời nói (luyện trôi 30s):** "Vì test tự động bị chặn ~52% và thua người; và LLM hứa hẹn vượt qua; nên em làm SLR sàng ~280→13; phát hiện 3 gap; do đó đề xuất thí nghiệm 3 EMB API có lỗi gieo sẵn. Mỗi mệnh đề đều có số liệu + trích dẫn tới trang phía sau."

### Slide 51 — Tính chính trực (chủ động khai báo) ★
- **Lời nói (ghi điểm cao):** "Em chủ động báo 3 chỗ chưa hoàn hảo trong 104 trích dẫn: (1) gỡ được dấu † của #5; (2) 2 chỗ lệch trang nhỏ — EvoMaster 'only manual comparison' nằm ở Conclusion p.11–12 chứ không p.9; LogiAgent '49 crash' là tổng Table 3 chứ không một câu; (3) RESTGPT 'limitation' paper nêu ở Future Work. Chính sự khai báo này khiến hội đồng tin 101 trích dẫn còn lại."

### Slide 52 — Q&A: câu hỏi khó & trả lời sẵn ★
| Hỏi | Trả lời |
|---|---|
| "90% coverage rồi, gap đâu?" | Đó là *endpoint* coverage (#9 95.5%); *code* vẫn ~52–72%. RQ1 thêm EMB lỗi-gieo-sẵn + bóc loại endpoint. |
| "Chỉ 3 API đủ không?" | Threat đã nêu; bù bằng McNemar per-fault + effect size; #10 dùng 3, #12 dùng 6 — đúng tầm. |
| "Sao chọn GPT?" | GPT thống trị (#1,2,4,6); decision-log #3; #5 cho thấy Claude cũng mạnh → mở rộng được. |
| "Lấy gì chắc LLM có ích?" | Ablation #6: bỏ LLM → coverage rớt 10.9–12.8% (p.10). |
| "Mutation #5 = ground truth rồi?" | Mutant tự sinh, 6 API tự dựng, không so người/EvoMaster — khác lỗi-gieo-sẵn dùng chung. |
| "Số liệu SLR tin được?" | 104 trích dẫn verify tới trang, 13 PDF tải sẵn; 2 lệch trang + 1 not-present đã khai báo. |

---

# PHỤ LỤC (slide 53–58)
- **53** Divider · **54** Evidence table đầy đủ · **55–56** Chỉ mục trích dẫn (page/line, ✓ verify) · **57** Lý do chọn kiểm định + thuật ngữ · **58** Tài liệu tham khảo + cách chạy deck.
- **Cách dùng:** không trình bày tuần tự — nhảy tới khi hội đồng hỏi (gõ số slide + Enter, hoặc **O** xem lưới).

### Slide 59 — Cảm ơn
- **Lời nói:** "Cảm ơn hội đồng. Mọi con số em nói đều mở được tới trang trong PDF — mời hội đồng kiểm chứng. Em sẵn sàng cho câu hỏi."

---

## Bảng tổng hợp 13 paper (tra nhanh)

| # | Tool | LLM/approach | Kết quả chính | arXiv | Trang trích dẫn |
|---|------|--------------|---------------|-------|------------------|
| 1 | RESTGPT | GPT-3.5 few-shot | 97% precision; 72.68% input (+329%) | 2312.00894 | p.4 |
| 2 | KAT | GPT-3.5-turbo-1106 t=0 | +15.7% status-code; +24 mã ẩn | 2407.10227 | p.8, p.10 |
| 3 | RESTSpecIT | DeepSeek/GPT masking | 88.6% route; 89.25% param; $0.004 | 2402.05102 | p.14, p.16, p.22 |
| 4 | APITestGenie | GPT-4-Turbo RAG | 57.3%→80% script; 12 defect | 2409.03838 | p.4, p.5 |
| 5 | RestTSLLM | 7 LLM, Claude thắng | 71.7% branch; 40.8% mutation; 100% | 2509.05540 | p.9 Table 3 |
| 6 | AutoRestTest | GPT-3.5+MARL+SPDG | 58.3% line; 42 lỗi 500; ablation −10.9% | 2411.07098 | p.9, p.10 |
| 7 | LlamaRestTest | Llama3-8B fine-tune | 204 fault; 72.44% input | 2501.08598 | p.11, p.12 |
| 8 | LogiAgent | GPT-4o-mini 3 agent | 71.78% line; 234 lỗi logic; 33.81% FP | 2503.15079 | p.8, p.9 |
| 9 | RESTifAI | GPT-4.1-mini | 128/134 op; −37% token; 60.87%=bug | 2512.08706 | p.3, p.4 |
| 10 | EvoMaster | search-based MIO | 38 bug; gen 41% < tay 82% | 1901.01538 | p.1, p.11 |
| 11 | No Time to Rest | study 10 tool | 52.76% line (trần); EMB 20 svc | 2204.08348 | p.4, p.5, p.8 |
| 12 | Morest | model-based RPG | +26–103% cov; 44 bug (13 mới) | 2204.12148 | p.1 |
| 13 | DeepREST | deep RL + curiosity | +17–77% branch; Wilcoxon p<0.05 | 2408.08594 | p.8 |
