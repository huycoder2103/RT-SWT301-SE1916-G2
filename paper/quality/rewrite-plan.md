# Kế hoạch viết lại paper bằng chữ của nhóm

**Tình trạng:** GPTZero chấm **AI 100%** (Model 4.7b, 1.614 từ quét được).
**Kết luận:** không sửa được bằng cách biên tập thêm. Phải viết lại thật.

---

## 1. Vì sao biên tập không cứu được

Detector đo **perplexity** — độ dễ đoán của mỗi từ khi đã biết các từ trước.
Văn LLM có perplexity thấp vì đó chính là hàm mục tiêu mô hình được huấn luyện.

Đợt sửa trước đã bỏ 60 em-dash, bỏ cấu trúc "not X but Y", bỏ khung
"Three observations / First / Second / Third", bỏ từ hoa mỹ. Đó đều là **dấu
hiệu bề mặt**. Câu thay thế vẫn do LLM viết → phân bố token bên dưới không đổi
→ điểm không đổi.

Nhờ LLM sửa văn để máy không nhận ra là văn LLM là việc tự mâu thuẫn.

**Đừng** tìm cách lách: chèn ký tự ẩn (zero-width space), thay chữ Latin bằng
chữ Cyrillic nhìn giống, cố tình viết sai ngữ pháp cho "giống người". Mấy cái đó
bị phát hiện dễ hơn, và nếu bị bắt thì tính chất nặng hơn nhiều so với việc khai
báo trung thực.

**Phần nghiên cứu không có vấn đề gì.** Mutant thật, số liệu thật, phần threats
trung thực. `notes.md` §F còn ghi cả những lần thất bại (F1, F7, F8) — thứ mà
một bài bịa sẽ không bao giờ có. Vấn đề chỉ nằm ở câu chữ.

---

## 2. Chia việc

Chia theo **ai đã thực sự làm phần đó** — viết về việc mình làm thì tự nhiên ra
giọng của mình, không phải cố diễn.

| Người | Vai trò | Phần viết | Số từ |
|---|---|---|---:|
| Huy | PL | `02_related` + `01_intro` | ~1220 |
| Dung | LR | `03_method` (§ arms, measurement, reproducibility) | ~600 |
| Dat | DG | `03_method` (§ subjects, fault seeding) | ~420 |
| Thuan | MS | `04_results` | ~1090 |
| Nguyen | RW | `05_discussion` + `07_conclusion` + `00_abstract` | ~1860 |
| Cả nhóm | — | `06_threats` — mỗi người viết threat của phần mình | ~1190 |

`08_declarations.tex` **không viết lại** — chỉ cần kiểm tra từng câu có đúng
sự thật không. Đây là phần khai báo dùng AI, sai một câu là hỏng.

---

## 3. Cách viết (quan trọng)

**Quy trình cho từng đoạn:**

1. Mở khung dữ kiện ở §4 bên dưới. **Đóng file `.tex` lại.** Không nhìn câu cũ.
2. Đọc dữ kiện, hiểu ý.
3. **Nói thành tiếng** như đang giải thích cho bạn cùng lớp.
4. Gõ lại đúng câu vừa nói.
5. Sửa ngữ pháp, **giữ nguyên nhịp câu của mình**.

**Vì sao bước 3 quan trọng:** câu nói ra miệng có nhịp không đều — lúc dài lúc
cụt, có chỗ ngập ngừng, có chỗ nhấn. LLM không sinh ra kiểu đó. Đây không phải
mẹo lách máy, mà đơn giản là cách người ta viết thật.

**Viết tiếng Việt trước rồi dịch cũng được** và thường ra văn rất khác LLM, vì
cấu trúc câu tiếng Việt kéo theo. Ngữ pháp hơi lệch chuẩn học thuật một chút
không sao — GV chấm nội dung, và văn hơi mộc còn hơn văn bị flag.

**Giữ nguyên, tuyệt đối không đụng:**

- Mọi macro `\RQII...`, `\PD...`, `\Ncs...` — đó là số liệu tự sinh. Viết
  `\RQIIrecallEvo{}` chứ **không** gõ `0.1353`. `check_paper.py` sẽ báo lỗi nếu
  gõ tay số vào phần kết quả.
- `\cite{...}`, `\ref{...}`, `\label{...}`
- Cấu trúc bảng và figure

**Sau khi viết xong mỗi section:**

```bash
python scripts/check_paper.py
python scripts/ai_style_check.py
```

Script thứ hai không phải detector — nó chỉ chỉ ra chỗ nhịp văn còn đều quá.

---

## 4. Khung dữ kiện

Dưới đây là **nội dung** từng section, dạng gạch đầu dòng. Không có câu văn nào
để chép. Viết câu của mình từ đây.

### 01_intro — Huy

- REST API chiếm phần lớn lưu lượng giữa các thành phần phần mềm; test tốn kém, phần lớn vẫn thủ công
- LLM đọc OpenAPI spec sinh test được → có giá trị thương mại → nhiều nghiên cứu ra nhanh
- Dẫn 4 kết quả tiêu biểu: RESTGPT 97% precision rút luật · AutoRestTest 42 lỗi server vs EvoMaster 20 · LlamaRestTest 204 vs 130 · RESTifAI 95.5% operation coverage
- **Luận điểm chính:** mấy con số đó đếm *cái tìm được trên hệ thống sống*, không phải *tỉ lệ trên tổng số có thể tìm*
- Không có mẫu số thì "42 vs 20" không phân biệt được 42/50 với 42/500
- Với người phải quyết định có tin công cụ hay không, mẫu số thiếu chính là toàn bộ câu hỏi
- **GAP-C:** chỉ 1 bài từng so với manual — EvoMaster 2019, và nó *thua* manual (41% vs 82% statement coverage). Bài đó có trước LLM. Chưa ai đặt LLM + manual + tool trưởng thành lên cùng API
- **GAP-D:** fault detection luôn báo dạng đếm 500-error trên API sống. Không có benchmark gieo lỗi sẵn → không tính được Recall
- **GAP-M:** metric thiên về coverage. Chỉ KAT tách 2xx/4xx, chỉ RESTSpecIT báo 5xx. Không ai có metric edge-case theo endpoint
- Cách nhóm lấp: gieo lỗi bằng mutation vào 3 API EMB → mẫu số cố định `\RQIIn` → chạy cả 3 arm trên mọi mutant
- Thêm error-surface baseline: quét source liệt kê mọi chỗ có thể trả non-2xx
- **Kết quả chia làm hai hướng ngược nhau:** metric mà giới nghiên cứu ưa dùng thì LLM thắng (`\RQIcoveragePct`%, `\RQIIItotalLlm` scenario vs `\RQIIItotalManual`); ground truth thì EvoMaster `\RQIIrecallEvo` > LLM `\RQIIrecallLlm` > manual `\RQIIrecallManual`
- Giải thích: oracle *kind* đặt trần; trong cùng loại oracle, *volume* quyết định phần còn lại
- 5 đóng góp: so sánh 3 chiều đầu tiên · benchmark gieo lỗi `\RQIIn` mutant · metric edge-case + error-surface baseline · cơ chế 2 tầng · pipeline tái lập được

### 02_related — Huy

- Nền bằng chứng: SLR 5 thành viên, gộp và khử trùng lặp còn 59 bài (2018–2026), tiêu chí đăng ký trước, PRISMA từng người
- Bảng 10 bài tiêu biểu — **giữ nguyên bảng**, chỉ viết lại câu dẫn
- **Mẫu 1 — GPT thống trị:** gần như mọi bài LLM dùng model OpenAI; open-source chỉ lác đác. Nhóm dùng Claude Sonnet 4.6 → thêm điểm dữ liệu ngoài họ GPT (GAP-T)
- **Mẫu 2 — metric = coverage + đếm lỗi:** chất lượng ngữ nghĩa/edge-case hiếm khi tách riêng. Chỉ KAT tách 2xx/4xx, chỉ RESTSpecIT báo 5xx. Không ai đếm edge case theo endpoint → không có mốc để đánh giá độ rộng của negative testing
- **Mẫu 3 — baseline toàn tự động:** LLM tool so với EvoMaster/Morest rồi báo thắng về số lỗi server. Không bài LLM nào có manual arm. So sánh manual duy nhất là của chính EvoMaster (41% vs 82%), và không bài LLM nào xem lại nó dù lĩnh vực đã chuyển sang nói chuyện "ngang người"
- **Mẫu 4 — fault detection không có mẫu số:** mọi con số ở cột phải của bảng là đếm trên API sống. Đây là vấn đề phương pháp nặng nhất, vì đếm lỗi và Recall có thể xếp hạng *ngược nhau* — một suite dập mạnh một endpoint có thể log rất nhiều 500 mà bỏ sót phần lớn tập lỗi. Mutation testing là chuẩn ở mảng khác (PIT, Offutt); vắng ở đây khiến các claim so sánh không kiểm chứng được
- Bảng gap map — **giữ nguyên**

### 03_method — Dat (subjects, fault seeding)

- RQ/metric/ngưỡng/kiểm định chốt trong proposal tuần 5, đóng băng khi GV duyệt, **trước khi thấy dữ liệu full run**. Kết quả RQ2 mâu thuẫn với giả thuyết đã nêu
- **RQ1:** coverage ≥90%? H₀: μ ≤ 0.90. Ngưỡng 90% lấy từ literature (sàn 88.6% route discovery, trần 95.5% operation coverage). Test: Wilcoxon 1 mẫu, một phía
- **RQ2:** LLM bắt bao nhiêu lỗi gieo sẵn so với manual và EvoMaster? H₁: hơn cả hai. Test: Friedman + post-hoc Wilcoxon-Holm + McNemar gộp. Effect size: Cliff's δ
- **RQ3:** LLM sinh nhiều scenario 4xx/5xx và biên hơn manual? Test: Wilcoxon bắt cặp một phía. Effect size: rank-biserial
- α = `\alphaRaw` mỗi RQ (đăng ký trước), thêm ngưỡng Bonferroni `\alphaBonf` như cách đọc chặt hơn
- **Subjects:** 3 service từ EMB (LGPL-3.0) — `rest-ncs` `\RQINcsTotal` op, `rest-scs` `\RQIScsTotal`, `features-service` `\RQIFeaturesTotal`, tổng `\RQIopsTotal`. Mỗi cái deploy thành fat jar JDK 8 độc lập; harness và EvoMaster chạy JDK 17, chỉ giao tiếp qua HTTP
- **Fault seeding:** họ toán tử PIT/Offutt — relational replacement, arithmetic replacement, negate/boundary conditional. Áp vào controller và core-logic (nơi lỗi quan sát được qua HTTP contract). Mỗi mutation đổi 1 token, áp riêng lẻ, compile thành jar riêng; cái nào không compile thì bỏ; restore source trước khi làm cái tiếp
- Ra `\RQIIn` mutant compile được: ncs 70, scs 59, features 4. Catalog ghi file/dòng/toán tử
- Ground truth dẫn từ code chứ không phải người gán nhãn → không có chỉ số inter-annotator agreement
- `features-service` mất cân bằng (4 vs 70 và 59) là **đặc tính có thật** của code ít phép tính, không phải chọn mẫu lệch. Báo cáo như giới hạn generalization, không vá sau

### 03_method — Dung (arms, measurement, reproducibility)

- Cả 3 suite viết **trước** khi gieo lỗi, mù với catalog → không arm nào nhắm được mutant đã biết
- **LLM:** Claude Sonnet 4.6, temperature 0, top_p 1, max_tokens 4096, seed cố định. Input **chỉ** OpenAPI spec (black-box, không thấy source). Prompt đóng băng verbatim. Output: REST-assured JUnit 5
- **Manual:** suite EP/BVA từ cùng spec, mù với lỗi. **Do một phiên model riêng biệt, cách ly viết — không phải nhóm người.** Đây là threat về construct validity, gọi là "independently authored" chứ không phải "human"
- **EvoMaster 6.0.0:** black-box mode, seed 42, 3 lần lặp
- **Coverage:** số operation có ít nhất 1 test chạm ÷ tổng operation, tính từ spec + log request đã chạy
- **Fault Recall:** killed ÷ `\RQIIn`. Kill khi có ít nhất 1 test *pass trên bản gốc* mà *fail trên mutant*. Test vốn fail trên bản gốc bị loại (oracle không hợp lệ) → ghi `n_oracle` riêng từng arm
- **Edge-case count:** số scenario negative/boundary/error-code riêng biệt mỗi endpoint, parse từ tag `// SCENARIO type=`
- **Error-surface baseline:** analyser tĩnh liệt kê mọi vị trí source có thể trả non-2xx, phân loại declared / framework / potential
- **Error-behaviour key:** mẫu số `\PDerrKey` là **hợp của 3 arm**, không phải tổng độc lập. Arm nào đạt `\PDerrKey`/`\PDerrKey` chỉ chứng minh tập quan sát của nó bao hàm các arm khác, **không** chứng minh phủ hết bề mặt lỗi
- **Produced vs detected:** mọi request replay qua logging proxy, ghi status thật. Báo riêng cái *sinh ra* và cái *phát hiện được* — vì hai thứ này xếp hạng ngược nhau
- **Reproducibility:** chuỗi mutate.py → catalog → run_mutation → raw csv → analyze.py → summary.json → gen_paper_macros.py → paper. Mọi số là macro. `analyze.py` tái tạo `summary.json` byte-identical. Notebook Restart & Run All không lỗi. Một số nguyên cố định (số mutant từng SUT, số liệu pilot) viết chữ

### 04_results — Thuan

- **RQ1:** LLM chạm `\RQIopsCovered`/`\RQIopsTotal` operation = `\RQIcoveragePct`%, đều trên cả 3 subject. Wilcoxon: W=`\RQIwilcoxonW`, p=`\RQIpvalue`, rank-biserial=`\RQIrankBiserial`. H₀ bị bác ở α=`\alphaRaw` và cả Bonferroni
- Miss profile theo loại endpoint: rỗng. Kết quả thật nhưng yếu — chỉ chứng minh LLM *tới được* mọi operation, không nói nó test tốt
- **RQ2 — so sánh chính đã đăng ký trước.** Recall: EvoMaster `\RQIIrecallEvo`, LLM `\RQIIrecallLlm`, manual `\RQIIrecallManual`. Tuyệt đối: `\PDkilledEvo` / `\PDkilledLlm` / `\PDkilledManual` trên `\PDkilledTotal`. **H₁ (LLM giỏi nhất) bị bác**
- Friedman: χ²=`\RQIIfriedmanChi`, p=`\RQIIfriedmanP`, không bác bỏ
- Post-hoc Wilcoxon-Holm (đã đăng ký trước) cũng **không** bác bỏ: p_Holm = `\RQIIholmLEp` và `\RQIIholmLMp`. Báo cáo vì đã đăng ký, nhưng n=3 subject nên họ kiểm định này thiếu lực → proposal đã chỉ định McNemar gộp (N=`\RQIIn`) làm phân tích chính
- **LLM vs EvoMaster:** b=`\RQIImcnemarLEb`, c=`\RQIImcnemarLEc`, p=`\RQIImcnemarLEp`, Cliff's δ=`\RQIIcliffLE`. Power xấp xỉ `\RQIImcnemarLEpower`. Sát ngưỡng α, nhạy với 1 mutant biên
- **LLM vs manual:** b=`\RQIImcnemarLMb`, c=`\RQIImcnemarLMc` → **tập kill của manual nằm trọn trong tập của LLM**. p=`\RQIImcnemarLMp`, δ=`\RQIIcliffLM`
- Bảng RQ2 — giữ nguyên. Đọc bảng: trên `rest-ncs` cả hai arm status-oracle đều `\RQIINcsLlm` trong khi EvoMaster `\RQIINcsEvo`; trên `rest-scs` LLM dẫn (`\RQIIScsLlm` vs manual `\RQIIScsManual`, EvoMaster `\RQIIScsEvo`); `features-service` hòa. **Thứ hạng đi theo đặc tính lỗi của từng subject**
- **RQ3:** LLM `\RQIIItotalLlm` scenario vs manual `\RQIIItotalManual` trên `\RQIIIn` operation (median `\RQIIImedianLlm` vs `\RQIIImedianManual`). W=`\RQIIIwilcoxonW`, p=`\RQIIIpvalue`, rank-biserial=`\RQIIIrankBiserial`. Qua cả Bonferroni. Không do outlier: LLM hơn ở `\RQIIIpairsLlm`/`\RQIIIn` operation, manual hơn ở `\RQIIIpairsManual`, hòa `\RQIIIpairsTie`. Hiệu ứng lớn nhất nghiên cứu, và ít hệ quả nhất
- **Produced vs detected** — bảng giữ nguyên. LLM viết `\PDtestsLlm` test vs EvoMaster `\PDtestsEvo` (=`\PDvolumeRatioLlmEvo`×), EvoMaster phát hiện `\PDkillRatioEvoLlm`× số lỗi của LLM
- LLM dẫn về error behaviour (`\PDerrTriggeredLlm` vs `\PDerrTriggeredManual` và `\PDerrTriggeredEvo`), `\PDcrashLlm` phản hồi 5xx gồm 1 crash thật. **Nhưng key là hợp của 3 arm** → chỉ chứng minh bao hàm, không phải phủ bề mặt lỗi
- Nếu chỉ báo metric mà literature dùng thì LLM đứng nhất mọi bảng. Ground truth đồng ý về manual nhưng **lật ngược** phán quyết với EvoMaster: arm sinh ít test nhất lại phát hiện nhiều lỗi nhất
- Hai caveat: coverage và scenario count chỉ định nghĩa cho LLM và manual (EvoMaster không sinh scenario annotation, và nhóm không đo per-operation coverage cho nó) → **không metric nào xếp hạng đủ cả 3 arm**. So sánh với EvoMaster rốt cuộc dựa trên test volume và 5xx tally — đúng loại proxy mà bài này phê phán

### 05_discussion — Nguyen

- **Nghịch lý:** LLM sinh `\PDvolumeRatioLlmEvo`× volume của EvoMaster, phủ mọi operation, `\RQIIItotalLlm` scenario, mà kill chưa tới một nửa số lỗi
- **Giải thích nằm ở loại assertion mỗi arm viết**
- Spec mô tả *status code* → test sinh từ spec chỉ assert status code, cùng lắm là shape của body → "response nằm trong lớp hợp lý cho request này". Manual EP/BVA từ cùng spec viết cùng loại. Cả hai là **spec-derived status oracle**
- Mutant làm gì: đổi toán tử quan hệ/số học trong routine số → đổi *giá trị tính được*. Endpoint vẫn trả 200 với con số sai → status oracle pass → lỗi sống sót
- EvoMaster: black-box mode ghi lại response thật của hệ gốc, sinh assertion ghim giá trị đó → **regression oracle**, fail khi bất kỳ giá trị nào đổi
- → Ba arm chưa bao giờ đo cùng một thứ. LLM/manual trả lời "API có phản hồi đúng lớp tài liệu ghi không"; EvoMaster trả lời "API có còn tính ra đúng như trước không". Tập lỗi của nhóm gần như toàn value fault → hỏi câu thứ hai. **EvoMaster thắng là bằng chứng regression oracle mạnh hơn status oracle trên value fault, không phải search-based giỏi hơn LLM**
- **Bằng chứng 1 — pattern theo subject khớp dự đoán:** EvoMaster dẫn trên `rest-ncs` (`\RQIINcsEvo` vs `\RQIINcsLlm`), nơi controller là routine số học; LLM dẫn trên `rest-scs` (`\RQIIScsLlm` vs `\RQIIScsEvo`), nơi nhiều mutant lật *lớp* response
- **Chi tiết ncs (phần cô yêu cầu bổ sung):** cả `\NcsEvoKills` mutant EvoMaster kill được đều nằm trong 1 file `\NcsEvoKillFile.java`. `\NcsEvoKillsArith` cái đổi toán tử số học, `\NcsEvoKillsRel` cái đổi so sánh số. Mọi cái đều giữ request hợp lệ và status 200, chỉ đổi con số trả về
- **Volume không giải thích được, mà còn ngược lại:** trên ncs, LLM có `\NcsOracleLlm` test hợp lệ, manual `\NcsOracleManual`, EvoMaster `\NcsOracleEvo`. EvoMaster kill `\NcsEvoKills` với bộ test **nhỏ nhất**, hai bộ lớn hơn kill 0
- **Bằng chứng 2 — LLM thắng chỗ oracle của nó đủ:** trên bề mặt lỗi có tài liệu, LLM sinh nhiều behaviour nhất và có 1 crash 500 thật. (Nhắc lại: key là arm-derived)
- **Bằng chứng 3 — cơ chế 2 tầng:** pilot thấy LLM và manual kill *y hệt* nhau, nhưng suite manual chung tác giả với LLM nên không diễn giải được. Viết lại độc lập tách được hai hiệu ứng: trên ncs (toàn value fault) manual độc lập vẫn `\RQIINcsManual` giống LLM — trần do oracle kind; trên scs (có mutant status-visible) hai suite tách hẳn, LLM `\RQIIScsLlm` vs manual `\RQIIScsManual`, manual ⊂ LLM
- **Cho practitioner:** LLM cho *độ rộng*, không cho *độ sâu*. Nó sẽ chạm mọi operation và dò bề mặt lỗi mạnh hơn người lẫn search tool. Nó **sẽ không** nhận ra routine tính giá trả sai tổng, vì spec không nói tổng đúng là bao nhiêu. Dùng LLM cho spec conformance và error-path breadth; đừng để nó thay regression oracle / property-based assertion / expected value trên đường tính toán. EvoMaster tìm ra `\RQIImcnemarLEc` lỗi LLM bỏ sót hoàn toàn
- **Cho lĩnh vực:** mọi metric literature dùng xếp LLM nhất, ground truth xếp nhì. Khi AutoRestTest báo 42 vs 20, hay LlamaRestTest 204 vs 130 — số đó thật, nhưng đo *bề mặt lỗi bị dập mạnh đến đâu*, không phải *bắt được bao nhiêu phần tập lỗi*. RQ3 của chính nhóm cũng dính caveat này
- **Cho thiết kế benchmark:** cần benchmark gieo lỗi sẵn, vì không có mẫu số thì hai thứ tự trên không phân biệt được. Nên phân tầng tập lỗi theo **oracle-observability** (status-visible vs value-only) — trục đó một mình đủ đảo thứ hạng. Benchmark toàn value fault sẽ ưu ái regression-oracle tool; toàn status fault sẽ ưu ái LLM
- **Recall tuyệt đối thấp là thông tin, không phải lỗi setup:** cao nhất EvoMaster `\PDkilledEvo`/`\PDkilledTotal` (`\RQIIrecallEvoPct`%). Có thể chỉnh cao lên bằng cách gieo lỗi dễ hơn, nhóm chọn không làm. Mutant nằm trong core logic chỉ chạm được qua HTTP contract, nhiều cái tương đương ở biên: giá trị hỏng không bao giờ nổi lên response field, hoặc chỉ nổi với input không arm nào sinh. White-box tool có feedback coverage sẽ cao hơn

### 06_threats — cả nhóm

Mỗi người viết threat thuộc phần mình. Danh sách đầy đủ:

**Construct validity**
- Manual arm là *independent-agent*, không phải *independent-human*. Proposal ghi human cohort, không huy động được. Viết bởi phiên model riêng, cách ly, spec-only, mù với output LLM và catalog lỗi. Giải quyết được confound same-author của pilot (b=`\RQIImcnemarLMb`, c=`\RQIImcnemarLMc`). Còn lại chưa kiểm soát: khoảng cách giữa agent độc lập và người thật — người có thể có trực giác nghiệp vụ mà agent viết-từ-spec không có. Hướng kết luận không đổi vì manual ⊂ LLM
- Ý nghĩa thống kê LLM-vs-EvoMaster phụ thuộc 1 mutant biên. Re-run tái tạo *chính xác* kill của EvoMaster (12 mutant trên ncs) và kill scs của LLM, nhưng ncs của LLM rớt từ 1/70 xuống `\RQIINcsLlm`: 1 test `bessj` tại biên n=2 pass trên build pilot, fail trên build sạch → bị loại khỏi oracle. Bessel tại biên nhạy về số học; đây là giới hạn tái lập, không phải lỗi pipeline (EvoMaster khớp 100% loại trừ lỗi build). Hệ quả: b từ 5 → `\RQIImcnemarLEb`, đẩy p qua ngưỡng α. **Hướng robust, ngưỡng thì không**
- Mẫu số error-behaviour là arm-derived nên trần không mang thông tin. `\PDerrKey` là hợp của 3 arm → arm mạnh nhất đạt `\PDerrKey`/`\PDerrKey` by construction. Không so được với baseline tĩnh (đếm vị trí source, không phải behaviour quan sát). Muốn có error-surface Recall thật phải chấm mọi arm với bản liệt kê tĩnh — nhóm chưa làm, và đây là khoảng trống đo lường rõ nhất của bài
- Oracle strength khác nhau giữa các arm **theo thiết kế**. Không phải biến gây nhiễu bị bỏ sót — nó chính là biến độc lập. Nhưng nghĩa là RQ2 không so "kỹ thuật sinh test" với oracle strength giữ cố định
- Mutation kill là proxy cho lỗi thật. Coverage cũng là proxy cho chất lượng test

**Internal validity**
- Không loại equivalent mutant (bài toán không giải được tổng quát). Một phần trong `\RQIIn` mutant có thể không arm black-box nào kill được → kéo Recall cả 3 arm xuống đều. Yếu con số tuyệt đối, không ảnh hưởng so sánh
- LLM không tất định. Temperature 0 + seed cố định, output đóng băng trong repo, nhưng sampling không bit-reproducible qua các lần provider cập nhật model. Suite đã commit nên phân tích tái lập được kể cả khi sinh lại thì không
- Mutation chỉ trong controller và core-logic. Lỗi ở tầng config/persistence/serialisation nằm ngoài tập lỗi và ngoài kết luận

**External validity**
- 3 API JVM, `\RQIopsTotal` operation, service EMB nhỏ. Kết luận là "EMB-only, JVM-only". Không suy ra API production lớn, luồng có xác thực, hay stack ngoài JVM. `user-management` (MySQL) bị loại vì chi phí setup → endpoint xác thực thiếu đại diện
- `features-service` mất cân bằng: 4 mutant vs 70 và 59. Cả 3 arm hòa (`\RQIIFeaturesLlm`) nên đóng góp gần như không gì vào so sánh gộp. Giữ lại vì bỏ một subject sau khi thấy kết quả là chọn theo outcome
- 1 model, 1 cấu hình. Không suy ra họ GPT (đang thống trị literature), model open-source, hay chiến lược agentic nhiều lượt. Vì cơ chế là oracle kind chứ không phải năng lực model, dự đoán kết quả định tính giữ nguyên cho mọi bộ sinh spec-only — nhưng **chưa test**

**Conclusion validity**
- Friedman thiếu lực **theo thiết kế**: n=3 subject không phát hiện được hiệu ứng thực tế. Vì thế proposal chỉ định trước McNemar gộp làm phân tích chính, **không phải** đôn lên sau khi omnibus fail
- Kiểm định pairwise RQ2 có ý nghĩa nhưng mong manh: cả hai p=`\RQIImcnemarLEp` / `\RQIImcnemarLMp` qua α=`\alphaRaw` nhưng **không** qua Bonferroni `\alphaBonf`; power `\RQIImcnemarLEpower` và `\RQIImcnemarLMpower` đều dưới mức đủ. Đặt kết luận trên *hướng và effect size*, không trên p-value. Không nâng "significant ở α" thành "đã xác lập chắc chắn". Con số power tự nó là xấp xỉ (statsmodels không có routine power McNemar chính xác → thay bằng phép tính 2 tỉ lệ độc lập, đã khai trong `summary.json`)
- Multiplicity: 3 họ RQ. Holm trong post-hoc RQ2, Bonferroni chéo họ. RQ1 và RQ3 qua thoải mái; pairwise RQ2 qua ngưỡng thô nhưng không qua Bonferroni

### 07_conclusion — Nguyen

- Đã chạy so sánh mà literature chưa có: LLM + manual EP/BVA + EvoMaster, cùng 3 API, đối chiếu tập lỗi **đã biết** `\RQIIn` thay vì đếm lỗi trên hệ thống sống
- Trả lời câu hỏi tiêu đề: LLM **thắng** baseline kiểu người, **thua** công cụ
- Metric volume: `\RQIcoveragePct`% coverage, `\RQIIItotalLlm` vs `\RQIIItotalManual` scenario, `\PDtestsLlm` vs `\PDtestsEvo` test case
- Ground truth: EvoMaster `\RQIIrecallEvo` > LLM `\RQIIrecallLlm` > manual `\RQIIrecallManual`. LLM out-detect manual (`\RQIImcnemarLMp`, kill là superset thật sự), bị EvoMaster out-detect (`\RQIImcnemarLEp`). Cả hai qua ngưỡng thô, không qua Bonferroni → đọc theo hướng
- Không phải chuyện năng lực model: bộ sinh đọc spec thì viết assertion về status code, và lỗi đổi giá trị mà giữ status là vô hình với mọi assertion loại đó, viết bao nhiêu cũng vậy
- Bằng chứng: thứ hạng đi theo đặc tính lỗi — ncs cả hai status-oracle arm `\RQIINcsLlm` trong khi EvoMaster `\RQIINcsEvo`; scs LLM dẫn mọi arm
- Oracle kind đặt trần; trong cùng kind, volume quyết định phần bắt được
- 3 hệ quả: (practitioner) LLM bổ sung chứ không thay oracle giá trị — thắng suite kiểu người mà vẫn sót `\RQIImcnemarLEc` lỗi EvoMaster bắt được · (lĩnh vực) metric xếp LLM trên và metric xếp LLM dưới bất đồng trên cùng một code, nên các claim so sánh hiện có không đo cái mà cách diễn đạt của chúng ám chỉ · (benchmark) phân tầng tập lỗi theo oracle-observability
- Giới hạn còn lại lớn nhất: manual baseline là phiên agent cách ly, không phải nhóm người. Tái lập với người thật trên đúng `\RQIIn` mutant là bước giá trị nhất, pipeline chạy được ngay
- Nghiên cứu tiếp theo: so sánh có kiểm soát oracle (cố định loại assertion, chỉ đổi bộ sinh) · tập lỗi phân tầng theo oracle-observability · ablation GAP-T qua các họ model

### 00_abstract — Nguyen (viết **cuối cùng**)

Viết sau khi đã xong hết. Trần LNCS: **150 từ**. Cấu trúc:

1. Bối cảnh + 3 khoảng trống từ 59 bài (1–2 câu)
2. Nhóm làm gì: 3 arm mù, 3 API EMB, `\RQIopsTotal` operation, gieo `\RQIIn` lỗi để cố định mẫu số
3. Kết quả: LLM thắng metric volume; ground truth EvoMaster > LLM > manual
4. Giải thích: oracle kind — status oracle không thấy lỗi đổi giá trị mà giữ status
5. Hệ quả: scenario count gây hiểu nhầm nếu không kèm Recall

Đếm từ trước khi commit — vượt 150 là sai chuẩn LNCS.

---

## 5. Sau khi viết xong

```bash
python scripts/gen_paper_macros.py    # nếu có chạy lại thí nghiệm
python scripts/check_paper.py         # phải PASS
python scripts/ai_style_check.py      # xem nhịp văn
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Kiểm tra: body vẫn trong trang 1–15, 0 overfull hbox, abstract ≤150 từ.

Rồi quét lại GPTZero. **Kỳ vọng thực tế:** điểm sẽ tụt đáng kể vì text thật sự
do người viết, nhưng đừng kỳ vọng 0%. Detector có false positive với văn học
thuật của người viết không phải bản ngữ. Nếu vẫn còn cao ở một section nào đó,
đó là section chưa được viết lại thật sự.

**Và giữ nguyên `08_declarations.tex`.** Nó khai rằng nhóm có dùng LLM hỗ trợ.
Điều đó vẫn đúng và vẫn phải khai — kể cả sau khi viết lại toàn bộ, vì bản nháp
đầu do LLM sinh. Khai trung thực là thứ bảo vệ nhóm, không phải điểm số detector.
