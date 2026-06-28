// =============================================================================
// Curriculum: Zero -> Hero. Dạy người CHƯA đọc paper/SLR cũng thuyết trình được.
// teach block types: p | analogy | terms | numbers | why | say | slide | warn
// quiz types: mcq | tf | cloze | flip | order
// Mọi nội dung bám sát deck (../presentation) + 104 trích dẫn đã verify.
// =============================================================================

export const HERO_LINE =
  "Vì test API tự động bị chặn ở ~52% code coverage và còn thua người (EvoMaster 41% vs 82%); LLM hứa hẹn vượt qua; nên em làm SLR sàng ~280→13 paper chất lượng cao; phát hiện 3 khoảng trống; do đó đề xuất thí nghiệm trên 3 API EMB có lỗi gieo sẵn để đóng cả 3.";

export const course = [
  // ===================================================================== M0
  {
    id: 'm0', icon: '🚀', color: 'teal',
    title: 'Khởi động',
    subtitle: 'Bài này nói về cái gì? (cho người chưa biết gì)',
    lessons: [
      {
        id: 'm0l1', title: 'Bức tranh lớn trong 60 giây', mins: 3, slides: [1, 2],
        teach: [
          { t: 'p', md: 'Cả bài thuyết trình trả lời **một câu hỏi**: *"AI (cụ thể là LLM như ChatGPT) có viết test cho REST API giỏi không — so với con người và so với công cụ tự động cũ?"*' },
          { t: 'analogy', title: 'Hình dung như một nhà hàng', md: 'Một **REST API** giống nhà hàng nhận order qua ô cửa. **Kiểm thử (test)** = thử đặt đủ kiểu order (đúng và cố tình sai) để xem nhà hàng phản ứng có đúng không. Câu hỏi của bài: *để AI viết các order thử đó, có tốt hơn người và máy cũ không?*' },
          { t: 'p', md: 'Để trả lời nghiêm túc (không phán bừa), tác giả đọc **13 công trình khoa học** theo một quy trình chuẩn gọi là **SLR**, tìm ra **3 chỗ chưa ai làm**, rồi đề xuất một **thí nghiệm** để làm chỗ đó.' },
          { t: 'numbers', items: [{ v: '13', l: 'paper được đọc (2019–2026)' }, { v: '3', l: 'khoảng trống (GAP) tìm ra' }, { v: '104', l: 'trích dẫn đã kiểm tới từng trang' }] },
          { t: 'say', md: 'Mở đầu trên sân khấu: *"Em trình bày nghiên cứu về việc dùng LLM sinh test cho REST API. Đây là một tổng quan có hệ thống trên 13 công trình, từ đó em chỉ ra một khoảng trống và đề xuất thí nghiệm lấp nó. Mọi con số em nêu đều dẫn được tới trang trong paper gốc."*' },
          { t: 'slide', n: [1, 2] },
        ],
        quiz: [
          { t: 'mcq', q: 'Mục tiêu cuối cùng của cả bài thuyết trình là gì?', options: ['Khoe LLM mạnh thế nào', 'Chỉ ra một khoảng trống nghiên cứu và đề xuất thí nghiệm lấp nó', 'Dạy cách lập trình REST API', 'Giới thiệu ChatGPT'], correct: 1, explain: 'Bài là một SLR → tìm GAP → đề xuất thí nghiệm. Không phải tung hô LLM.' },
          { t: 'flip', front: 'SLR là viết tắt của gì?', back: 'Systematic Literature Review — tổng quan tài liệu có hệ thống, minh bạch, ai làm lại cũng ra cùng kết quả.' },
          { t: 'tf', q: 'Tác giả chỉ đọc vài bài báo tìm được rồi kết luận.', answer: false, explain: 'Sai — quy trình SLR quét có hệ thống ~280 kết quả, sàng lọc minh bạch còn 13.' },
        ],
      },
      {
        id: 'm0l2', title: 'Bạn sẽ thuyết trình theo đường nào', mins: 3, slides: [2],
        teach: [
          { t: 'p', md: 'Toàn bộ bài đi theo **một đường thẳng nhân–quả**. Nhớ 6 chặng này là bạn không bao giờ lạc:' },
          { t: 'terms', items: [
            ['1. Bối cảnh', 'API là gì, test nó khó ở đâu, vì sao cần LLM'],
            ['2. Phương pháp SLR', 'cách quét & sàng lọc 280→13 paper'],
            ['3. Bằng chứng', '13 paper với số liệu cụ thể'],
            ['4. GAP', '3 khoảng trống chưa ai làm'],
            ['5. Câu hỏi NC', 'biến GAP thành câu hỏi đo được'],
            ['6. Giả thuyết & Thí nghiệm', 'cách kiểm chứng'],
          ] },
          { t: 'why', md: 'Vì sao đi đúng thứ tự này? Vì **mỗi chặng là LÝ DO cho chặng sau**. Không có bối cảnh thì không hiểu vì sao cần LLM; không có bằng chứng thì GAP chỉ là cảm tính.' },
          { t: 'say', md: '*"Bài gồm 6 phần, đi từ bối cảnh đến thí nghiệm. Điểm khác biệt: mỗi bước đều có nguồn — khi tới phần khoảng trống, em sẽ chỉ vào đúng cột trong bảng để chứng minh, không nói cảm tính."*' },
        ],
        quiz: [
          { t: 'order', prompt: 'Sắp đúng thứ tự 6 chặng của bài:', items: ['Bối cảnh', 'Phương pháp SLR', 'Bằng chứng (13 paper)', 'GAP', 'Câu hỏi nghiên cứu', 'Giả thuyết & Thí nghiệm'] },
          { t: 'mcq', q: 'Vì sao phải có "Bằng chứng" TRƯỚC "GAP"?', options: ['Cho dài bài', 'Để GAP dựa trên dữ liệu thật chứ không phải cảm tính', 'Vì hội đồng yêu cầu', 'Không quan trọng thứ tự'], correct: 1, explain: 'GAP phải được chứng minh bằng bằng chứng (bảng so sánh), nếu không nó chỉ là "tôi thấy thiếu".' },
        ],
      },
      {
        id: 'm0l3', title: 'Mẹo thuyết trình tự tin (kể cả khi run)', mins: 4, slides: [],
        teach: [
          { t: 'p', md: 'Bạn **không cần** thuộc lòng từng chữ. Bạn cần nắm **ý chính + 1–2 con số đắt** mỗi slide, rồi nói bằng lời của mình.' },
          { t: 'terms', items: [
            ['Quy tắc 1 con số', 'Mỗi slide chỉ cần nhấn 1–2 số quan trọng nhất, đừng đọc hết bảng'],
            ['Dừng có chủ đích', 'Sau một con số mạnh (vd "41% vs 82%"), dừng 1 giây cho ngấm'],
            ['Nối nhân–quả', 'Dùng từ "vì / nên / do đó" để nối các slide'],
            ['Nếu bị hỏi khó', 'Quay về: "mọi khẳng định của em đều có nguồn, em mở appendix chỉ trang"'],
          ] },
          { t: 'warn', md: 'Đừng đọc slide chữ-cho-chữ. Hội đồng đọc nhanh hơn bạn nói. Bạn ở đó để **giải thích & kết nối**, không phải đọc.' },
          { t: 'say', md: 'Câu "cứu nguy" vạn năng khi quên: *"Để em tóm lại ý chính của phần này…"* rồi nói 1 câu cốt lõi của slide.' },
        ],
        quiz: [
          { t: 'tf', q: 'Nên đọc nguyên văn từng dòng chữ trên slide.', answer: false, explain: 'Không — nhấn ý chính + số đắt, nói bằng lời mình. Đọc chữ-cho-chữ làm hội đồng chán.' },
          { t: 'mcq', q: 'Khi bị hỏi một câu khó bất ngờ, chiến lược an toàn nhất?', options: ['Im lặng', 'Bịa một con số', 'Quay về nguyên tắc "mọi khẳng định đều có nguồn, em mở appendix chỉ trang"', 'Đổi chủ đề'], correct: 2, explain: 'Tựa vào tính truy vết được — đó là điểm mạnh của bài.' },
        ],
      },
    ],
  },

  // ===================================================================== M1
  {
    id: 'm1', icon: '🧱', color: 'teal',
    title: 'Nền tảng',
    subtitle: 'API · Test · LLM — hiểu để giải thích được',
    lessons: [
      {
        id: 'm1l1', title: 'REST API & status code (siêu dễ)', mins: 5, slides: [4],
        teach: [
          { t: 'analogy', title: 'Nhà hàng qua ô cửa', md: '**Client** (bạn) gửi **request** (phiếu order) tới một **endpoint** (ô cửa cho từng món) bằng một **method**: `GET` = xem, `POST` = tạo, `PUT/PATCH` = sửa, `DELETE` = xoá. **Server** (bếp) trả **response** kèm **status code**.' },
          { t: 'terms', items: [
            ['2xx', 'Thành công ("món của bạn đây")'],
            ['4xx', 'Lỗi phía bạn ("order sai rồi" — thiếu thông tin, không có quyền)'],
            ['5xx', 'Lỗi phía server ("bếp cháy" — crash)'],
          ] },
          { t: 'p', md: 'Điểm mấu chốt cho cả bài: một bộ test **tốt** không chỉ gửi order đúng (mong 2xx), mà còn **cố tình gửi order sai** để xem có nhận đúng 4xx không. Đó gọi là **edge case** (ca biên).' },
          { t: 'say', md: '*"REST API là cách hai phần mềm nói chuyện qua HTTP. Server trả mã trạng thái: 2xx là ổn, 4xx là client sai, 5xx là server lỗi. Test giỏi phải cố tình tạo lỗi để xem API có báo đúng không."*' },
          { t: 'slide', n: [4] },
        ],
        quiz: [
          { t: 'mcq', q: 'Gửi request với dữ liệu sai (vd thiếu trường bắt buộc), API NÊN trả mã nào?', options: ['200 (2xx)', '404/400 (4xx)', '500 (5xx)', 'Không trả gì'], correct: 1, explain: '4xx = lỗi phía client. Test edge case chính là kiểm tra API có trả đúng 4xx không.' },
          { t: 'cloze', before: 'Mã ', answer: '5xx', after: ' nghĩa là server bị lỗi/crash — thường là dấu hiệu một bug thật.', options: ['2xx', '4xx', '5xx'] },
          { t: 'flip', front: 'Method để TẠO một tài nguyên mới?', back: 'POST (GET = đọc, PUT/PATCH = sửa, DELETE = xoá).' },
        ],
      },
      {
        id: 'm1l2', title: 'OpenAPI spec là gì', mins: 4, slides: [4],
        teach: [
          { t: 'analogy', title: 'Quyển menu chi tiết', md: '**OpenAPI (Swagger)** là một file mô tả toàn bộ "menu" của API: có những endpoint nào, mỗi cái nhận tham số gì, kiểu dữ liệu, ràng buộc (vd `id phải ≥ 1`), và mô tả bằng **tiếng người**.' },
          { t: 'p', md: 'Đây là **đầu vào chuẩn** cho hầu hết công cụ sinh test — 11/13 paper đọc trực tiếp OpenAPI. Ghi nhớ: nó vừa có phần máy đọc được (kiểu, ràng buộc), vừa có phần **mô tả ngôn ngữ tự nhiên** — phần này là chỗ LLM toả sáng (bài sau).' },
          { t: 'say', md: '*"OpenAPI là bản đặc tả mô tả mọi endpoint, tham số và ràng buộc của API — đầu vào chuẩn cho công cụ sinh test. Nó có cả mô tả bằng tiếng người, và đó chính là chỗ LLM khai thác được."*' },
        ],
        quiz: [
          { t: 'mcq', q: 'OpenAPI/Swagger dùng để làm gì?', options: ['Chạy server', 'Mô tả (đặc tả) API: endpoint, tham số, ràng buộc', 'Lưu dữ liệu người dùng', 'Vẽ giao diện'], correct: 1, explain: 'Nó là "menu" đặc tả — đầu vào để sinh test.' },
          { t: 'tf', q: 'OpenAPI chỉ chứa thông tin máy đọc được, không có mô tả tiếng người.', answer: false, explain: 'Sai — nó CÓ phần mô tả ngôn ngữ tự nhiên, và đó là chỗ LLM khai thác.' },
        ],
      },
      {
        id: 'm1l3', title: 'Vì sao test API khó + HAI loại coverage', mins: 6, slides: [5, 33], key: true,
        teach: [
          { t: 'p', md: 'Ba thách thức khiến đây là **bài toán nghiên cứu** chứ không phải "viết vài test là xong":' },
          { t: 'terms', items: [
            ['1. Input vô hạn', 'Phải sinh giá trị THỰC TẾ (email đúng định dạng) thì request mới qua được tầng kiểm tra'],
            ['2. Phụ thuộc & trạng thái', 'Phải POST tạo trước rồi mới GET được — thứ tự lời gọi quan trọng'],
            ['3. Bài toán Oracle', 'Làm sao biết kết quả ĐÚNG? Spec (menu) có thể khác code (bếp) thật'],
          ] },
          { t: 'warn', title: 'CỰC KỲ QUAN TRỌNG — học kỹ chỗ này', md: 'Có **HAI loại "độ phủ" (coverage)** — đừng nhầm:\n\n• **Endpoint coverage** = đã gọi bao nhiêu % endpoint (món trong menu). **Có thể rất cao (>90%).**\n• **Code coverage** = đã chạm bao nhiêu % dòng code bên trong (ngóc ngách bếp). **Thường thấp hơn nhiều (~52%).**' },
          { t: 'analogy', title: 'Vì sao phân biệt?', md: 'Thử hết các món trong menu (endpoint cao) **không** có nghĩa bạn đã chạm mọi quy trình trong bếp (code thấp). Đây là chìa khoá để trả lời câu phản biện *"đã đạt 90% coverage rồi, gap đâu?"*.' },
          { t: 'say', md: '*"Có hai loại coverage. Endpoint coverage — đã gọi bao nhiêu phần trăm endpoint — có thể trên 90%. Nhưng code coverage — bao nhiêu phần trăm dòng code chạy — vẫn chỉ ~52%. Câu hỏi nghiên cứu của bài đo endpoint coverage nhưng thêm điều chưa ai làm: kiểm trên dữ liệu có lỗi gieo sẵn và bóc tách loại endpoint nào bị bỏ sót."*' },
          { t: 'slide', n: [5, 33] },
        ],
        quiz: [
          { t: 'mcq', q: 'Hội đồng hỏi: "Đã có tool đạt >90% coverage, vậy gap ở đâu?" — trả lời đúng nhất?', options: ['Thừa nhận hết gap', 'Đó là ENDPOINT coverage; CODE coverage vẫn chỉ ~52%, và chưa ai kiểm trên lỗi gieo sẵn + bóc loại endpoint', 'Nói tool đó sai', 'Im lặng'], correct: 1, explain: 'Phân biệt 2 loại coverage là câu trả lời "vàng" — endpoint cao không có nghĩa code cao.' },
          { t: 'flip', front: '"Bài toán Oracle" trong test API nghĩa là gì?', back: 'Khó biết kết quả trả về có ĐÚNG không, vì đặc tả (spec) có thể khác code thật. Nhiều tool chỉ coi 5xx là lỗi → bỏ sót lỗi logic trả 200 nhưng sai.' },
          { t: 'tf', q: 'Endpoint coverage cao đồng nghĩa code coverage cũng cao.', answer: false, explain: 'Sai hoàn toàn — đây là cái bẫy. Endpoint có thể >90% trong khi code chỉ ~52%.' },
        ],
      },
      {
        id: 'm1l4', title: 'Công cụ TRƯỚC LLM (chỉ cần biết tên)', mins: 4, slides: [6, 28],
        teach: [
          { t: 'p', md: 'Trước khi có LLM, người ta đã có 4 trường phái sinh test tự động. Bạn **chỉ cần nhớ tên + 1 câu** mỗi cái:' },
          { t: 'terms', items: [
            ['EvoMaster (2019)', 'Thuật toán di truyền (tiến hoá). Là baseline được dùng nhiều nhất — và là đối thủ trong thí nghiệm'],
            ['Morest (2022)', 'Dựng đồ thị quan hệ của API rồi cập nhật theo phản hồi'],
            ['RESTler (2019)', 'Fuzzing có trạng thái — bắn chuỗi request để dò lỗi 5xx'],
            ['DeepREST (2024)', 'Học tăng cường sâu (deep RL) — học cả ràng buộc ẩn ngoài spec'],
          ] },
          { t: 'numbers', items: [{ v: '~52%', l: 'line coverage — TRẦN của các tool này' }, { v: '41% vs 82%', l: 'EvoMaster (gen) THUA test người viết tay' }] },
          { t: 'why', md: 'Vì sao trần thấp & thua người? Vì giải thuật không vượt được **ràng buộc chuỗi, truy vấn DB, dịch vụ ngoài**. Con người có **tri thức miền** nên thoả thẳng. → Đây chính là chỗ LLM (đọc được tiếng người) hứa hẹn vượt qua.' },
          { t: 'say', md: '*"Trước LLM có các công cụ như EvoMaster, Morest, RESTler. Dù thông minh, chúng bị chặn ở khoảng 52% code coverage, và EvoMaster còn sinh test phủ thấp hơn người viết tay — 41% so với 82%. Đó là lằn ranh mà LLM hứa hẹn vượt qua."*' },
          { t: 'slide', n: [6, 28] },
        ],
        quiz: [
          { t: 'mcq', q: 'Con số "41% vs 82%" (EvoMaster) nói lên điều gì?', options: ['EvoMaster mạnh hơn người', 'Test do tool sinh phủ THẤP hơn test người viết tay', 'Coverage tăng theo năm', 'LLM đạt 82%'], correct: 1, explain: 'Đây là bằng chứng then chốt: tool tự động (2019) còn thua người → câu hỏi 2026 là LLM có lật ngược được không.' },
          { t: 'flip', front: 'Baseline (đối thủ tự động) nào được tái dùng nhiều nhất và là đối thủ trong thí nghiệm?', back: 'EvoMaster (search-based, 2019).' },
          { t: 'order', prompt: 'Xếp các tool theo năm ra đời (cũ → mới):', items: ['EvoMaster / RESTler (2019)', 'Morest (2022)', 'DeepREST (2024)'] },
        ],
      },
      {
        id: 'm1l5', title: 'Vì sao LLM hứa hẹn + câu hỏi ban đầu', mins: 5, slides: [7, 8],
        teach: [
          { t: 'p', md: 'LLM (như GPT) làm được **4 việc** mà công cụ máy móc cũ không làm được:' },
          { t: 'terms', items: [
            ['Đọc mô tả tiếng người', 'Hiểu câu "id phải là mã quốc gia hợp lệ" → sinh đúng giá trị'],
            ['Sinh giá trị giống thật', 'Email, ngày tháng hợp lệ → vượt tầng 4xx để chạm code sâu'],
            ['Suy luận phụ thuộc', 'Biết phải tạo trước rồi mới truy vấn'],
            ['Sinh script chạy được', 'Ra luôn code test (xUnit/Postman) + ca âm (negative)'],
          ] },
          { t: 'warn', md: 'Nhưng LLM có giá: **ảo giác (hallucination)**, **chi phí**, oracle vẫn không chắc. → Nên câu hỏi không phải "LLM dùng được không" mà **"hiệu quả tới mức nào, so với người và EvoMaster, trên thước đo có sự thật nền?"**' },
          { t: 'p', md: '**Câu hỏi ban đầu** (RQ thô) có 2 điểm mơ hồ: *(1) LLM nào?* và *(2) baseline & ngưỡng 90% từ đâu?* → chính 2 điểm mơ hồ này là **lý do phải làm SLR** (Phần 2).' },
          { t: 'say', md: '*"LLM hứa hẹn vì đọc được mô tả tiếng người, sinh giá trị thực tế, suy luận phụ thuộc, và sinh script chạy được. Nhưng nó có rủi ro ảo giác. Câu hỏi ban đầu của em còn mơ hồ ở chỗ chọn LLM nào và ngưỡng từ đâu — nên em làm SLR để tinh chỉnh nó dựa trên bằng chứng."*' },
          { t: 'slide', n: [7, 8] },
        ],
        quiz: [
          { t: 'mcq', q: 'Năng lực nào của LLM giúp nó hơn tool cũ rõ nhất?', options: ['Chạy nhanh hơn', 'Đọc & hiểu mô tả ngôn ngữ tự nhiên trong spec', 'Tốn ít điện', 'Không cần internet'], correct: 1, explain: 'Hiểu tiếng người là thứ tool dựa-luật không làm được — nền tảng cho mọi ưu thế khác.' },
          { t: 'tf', q: 'Bài thuyết trình tung hô LLM là giải pháp hoàn hảo.', answer: false, explain: 'Sai — bài thừa nhận LLM có ảo giác/chi phí, và đặt câu hỏi CÓ KIỂM SOÁT, không tung hô.' },
          { t: 'cloze', before: 'Câu hỏi ban đầu mơ hồ ở 2 điểm: chọn ', answer: 'LLM nào', after: ' và ngưỡng/baseline lấy từ đâu — đó là lý do cần làm SLR.', options: ['LLM nào', 'ngôn ngữ nào', 'server nào'] },
        ],
      },
    ],
  },

  // ===================================================================== M2
  {
    id: 'm2', icon: '🔬', color: 'indigo',
    title: 'Phương pháp SLR',
    subtitle: 'Cách quét & sàng lọc 280 → 13 paper một cách minh bạch',
    lessons: [
      {
        id: 'm2l1', title: 'SLR là gì & vì sao bắt buộc', mins: 5, slides: [9, 10],
        teach: [
          { t: 'analogy', title: 'Không phải "đọc đại vài bài"', md: '**SLR (Systematic Literature Review)** = khảo sát tài liệu theo quy trình *minh bạch, tái lập, kiểm toán được* (chuẩn Kitchenham). Giống công thức nấu ăn: ai làm theo cũng ra cùng món.' },
          { t: 'p', md: 'Quy trình 6 bước: **(1)** Câu hỏi + PICO → **(2)** Search string + database → **(3)** Sàng lọc IC/EC → **(4)** Đánh giá chất lượng → **(5)** Trích xuất dữ liệu → **(6)** Tổng hợp → GAP.' },
          { t: 'why', md: 'Vì sao bắt buộc? Nếu chỉ "Google vài bài", khoảng trống tìm được có thể chỉ là **do bỏ sót**. SLR đảm bảo gap là **thật**, vì đã sàng ~280 kết quả theo tiêu chí công khai.' },
          { t: 'say', md: '*"SLR là tổng quan tài liệu có hệ thống và tái lập được — bất kỳ ai chạy lại quy trình này cũng ra cùng 13 paper. Nhờ vậy khoảng trống em tìm ra là thật, không phải do em bỏ sót bài nào."*' },
          { t: 'slide', n: [9, 10] },
        ],
        quiz: [
          { t: 'mcq', q: 'Điểm khác biệt cốt lõi của SLR so với "đọc vài bài rồi kết luận"?', options: ['Đọc nhiều hơn', 'Quy trình minh bạch, tái lập được, ai làm lại cũng ra cùng kết quả', 'Dùng AI', 'Nhanh hơn'], correct: 1, explain: 'Tính tái lập + minh bạch là thứ làm GAP đáng tin.' },
          { t: 'order', prompt: 'Sắp đúng thứ tự quy trình SLR:', items: ['Câu hỏi + PICO', 'Search string + database', 'Sàng lọc IC/EC', 'Đánh giá chất lượng', 'Trích xuất dữ liệu', 'Tổng hợp → GAP'] },
        ],
      },
      {
        id: 'm2l2', title: 'PICO & chuỗi tìm kiếm', mins: 4, slides: [11, 12],
        teach: [
          { t: 'p', md: '**PICO** là khung 4 phần của một câu hỏi nghiên cứu — search string suy ra trực tiếp từ nó:' },
          { t: 'terms', items: [
            ['P — Population', 'REST/Web API có OpenAPI'],
            ['I — Intervention', 'LLM / GPT sinh test'],
            ['C — Comparison', 'thủ công + EvoMaster'],
            ['O — Outcome', 'coverage · executable · fault detection'],
          ] },
          { t: 'why', md: 'Vì sao **2** search string? String 1 bắt paper LLM; String 2 **cố ý** kéo về các baseline kinh điển (EvoMaster, Morest…) — vì chữ C trong PICO là "so với EvoMaster". Có chủ đích, không lạc đề.' },
          { t: 'say', md: '*"Câu hỏi được khung theo PICO. Em dùng 2 chuỗi tìm kiếm: một bắt các paper LLM, một chủ động kéo về các baseline kinh điển để có mốc so sánh — vì PICO yêu cầu so với EvoMaster."*' },
          { t: 'slide', n: [11, 12] },
        ],
        quiz: [
          { t: 'flip', front: 'PICO gồm 4 chữ gì?', back: 'Population (đối tượng), Intervention (can thiệp), Comparison (so sánh), Outcome (kết quả).' },
          { t: 'mcq', q: 'Vì sao cần String 2 (kéo về baseline)?', options: ['Cho đủ số lượng', 'Vì chữ C trong PICO là so với EvoMaster — cần tìm chính các baseline đó', 'Ngẫu nhiên', 'Google bắt buộc'], correct: 1, explain: 'C = Comparison = thủ công + EvoMaster, nên phải chủ động tìm baseline.' },
        ],
      },
      {
        id: 'm2l3', title: 'Tiêu chí chọn (IC) & loại (EC)', mins: 5, slides: [13, 14],
        teach: [
          { t: 'p', md: '**IC (Inclusion)** = điều kiện ĐỂ GIỮ một paper (phải thoả TẤT CẢ). **EC (Exclusion)** = điều kiện để LOẠI (vi phạm 1 là loại).' },
          { t: 'terms', items: [
            ['IC2', 'Xuất bản từ 2018 trở đi'],
            ['IC4 (tinh tế)', 'Dùng LLM, HOẶC là baseline liên quan (giữ EvoMaster/Morest để so)'],
            ['IC5', 'Phải có số liệu thực nghiệm cụ thể'],
            ['EC4', 'Lạc miền: chỉ GUI/unit test, HOẶC dùng API "ngược hướng" (API làm tool cho LLM)'],
            ['EC5', 'Lạc pha: chỉ về thực thi/bảo trì test, không phải SINH test'],
          ] },
          { t: 'warn', md: '**Bẫy EC4:** paper "RestGPT — kết nối LLM với REST API" bị LOẠI vì nó dùng API *phục vụ* LLM (ngược hướng). Đừng nhầm với "RESTGPT" (in hoa) là paper #1 được GIỮ. Chi tiết này cho thấy tác giả đọc kỹ.' },
          { t: 'say', md: '*"Một paper được giữ phải thoả cả 5 tiêu chí chọn. Điểm tinh tế là IC4: em cố ý giữ các tool không-LLM như EvoMaster để làm mốc so sánh — vì câu hỏi so LLM với chính EvoMaster."*' },
          { t: 'slide', n: [13, 14] },
        ],
        quiz: [
          { t: 'mcq', q: 'Vì sao giữ lại các tool KHÔNG dùng LLM (EvoMaster, Morest)?', options: ['Cho đủ 13 bài', 'Vì IC4 — cần chúng làm mốc so sánh định lượng cho GAP', 'Vì chúng cũng dùng AI', 'Nhầm lẫn'], correct: 1, explain: 'IC4 có chủ đích giữ baseline để so — không phải lạc đề.' },
          { t: 'tf', q: 'Paper dùng REST API làm công cụ cho LLM (ngược hướng) thì được giữ.', answer: false, explain: 'Sai — bị loại theo EC4 (lạc miền, ngược hướng).' },
        ],
      },
      {
        id: 'm2l4', title: 'Phễu PRISMA: 280 → 13', mins: 5, slides: [15], key: true,
        teach: [
          { t: 'analogy', title: 'Cái phễu lọc', md: 'PRISMA là sơ đồ "cái phễu": đổ vào ~280 kết quả thô, lọc dần xuống 13. Mỗi lần loại đều **ghi rõ mã lý do (IC/EC)** nên ai cũng kiểm lại được.' },
          { t: 'numbers', items: [
            { v: '~280', l: 'kết quả thô (Google Scholar, 2 string)' },
            { v: '30', l: 'sau khử trùng lặp (20 LLM + 10 baseline)' },
            { v: '13', l: 'cuối cùng vào evidence table (9 LLM + 4 baseline)' },
          ] },
          { t: 'p', md: 'Chi tiết phễu: 280 → **30** (khử trùng) → loại **7** ở vòng tiêu đề/abstract → **23** → loại **10** ở vòng full-text → **13**. Phép cộng khớp 100% — đây là thứ hội đồng hay soi.' },
          { t: 'say', md: '*"Em quét khoảng 280 kết quả thô, khử trùng còn 30, loại 7 ở vòng đọc tiêu đề-tóm tắt, còn 23, rồi loại 10 ở vòng đọc toàn văn, cuối cùng 13 paper. Mỗi lần loại đều có mã IC/EC nên hoàn toàn kiểm lại được, và phép cộng khớp tuyệt đối."*' },
          { t: 'slide', n: [15] },
        ],
        quiz: [
          { t: 'order', prompt: 'Sắp đúng các mốc của phễu PRISMA (nhiều → ít):', items: ['~280 thô', '30 sau khử trùng', '23 vào full-text', '13 cuối cùng'] },
          { t: 'cloze', before: 'Sau cùng còn ', answer: '13', after: ' paper: 9 LLM + 4 baseline.', options: ['9', '13', '30'] },
          { t: 'mcq', q: 'Điều gì khiến phễu PRISMA "kiểm toán được"?', options: ['Số đẹp', 'Mỗi lần loại đều ghi mã lý do IC/EC + phép cộng khớp', 'Dùng phần mềm', 'Nhiều bước'], correct: 1, explain: 'Minh bạch từng bước loại + đối soát số học = ai cũng kiểm lại được.' },
        ],
      },
      {
        id: 'm2l5', title: 'Đánh giá chất lượng (5.73/6)', mins: 4, slides: [16],
        teach: [
          { t: 'p', md: 'Sau khi chọn, mỗi paper được **chấm điểm chất lượng** (6 tiêu chí kiểu Kitchenham: mục tiêu rõ? tái lập được? có baseline? có bàn giới hạn?...). Mỗi tiêu chí: Yes=1, Partly=0.5, No=0.' },
          { t: 'numbers', items: [{ v: '5.73', l: 'điểm trung bình / 6' }, { v: '5.0', l: 'thấp nhất (vẫn cao)' }, { v: '13/13', l: 'đều vượt ngưỡng' }] },
          { t: 'why', md: 'Vì sao quan trọng? Vì nó **củng cố GAP**: những paper *không* so với người và *chỉ đếm* lỗi đều là paper **chất lượng cao**. → GAP là lỗ hổng thiết kế trong nghiên cứu mạnh, **không phải** do paper yếu bỏ sót.' },
          { t: 'say', md: '*"Em không chỉ chọn paper liên quan mà còn chấm chất lượng — trung bình 5.73/6. Điều này quan trọng: vì gap nằm ngay trong các paper mạnh, nên nó là lỗ hổng thiết kế thật, không phải do paper yếu."*' },
          { t: 'slide', n: [16] },
        ],
        quiz: [
          { t: 'mcq', q: 'Đánh giá chất lượng (5.73/6) củng cố lập luận GAP như thế nào?', options: ['Cho bài dài hơn', 'Chứng minh gap nằm trong các paper MẠNH → là lỗ hổng thiết kế thật', 'Để loại bớt paper', 'Không liên quan'], correct: 1, explain: 'Gap trong nghiên cứu chất lượng cao = gap thật, không phải artifact của paper yếu.' },
          { t: 'tf', q: 'Các paper bỏ sót so-sánh-với-người là những paper chất lượng thấp.', answer: false, explain: 'Ngược lại — chúng chất lượng cao (5.0–6.0), nên gap càng đáng tin.' },
        ],
      },
    ],
  },

  // ===================================================================== M3
  {
    id: 'm3', icon: '📚', color: 'teal',
    title: '13 Bằng chứng',
    subtitle: 'Số liệu đắt + 1 lý do cho mỗi paper',
    lessons: [
      {
        id: 'm3l1', title: 'Bản đồ 13 paper + GPT thống trị', mins: 5, slides: [17, 18],
        teach: [
          { t: 'p', md: '13 paper = **9 LLM** (#1–#9) + **4 baseline** kinh điển (#10–#13). Bạn không cần thuộc hết — chỉ cần **2 quan sát** định hình GAP:' },
          { t: 'terms', items: [
            ['GPT thống trị', '6/9 paper LLM dùng họ GPT; chỉ #5 có Claude (và Claude thắng)'],
            ['Không ai so với người', 'Cột "so với thủ công" TRỐNG ở mọi paper LLM → đây là GAP-1'],
          ] },
          { t: 'say', md: '*"Có 13 paper: 9 dùng LLM, 4 là baseline. Hai quan sát quan trọng: một là họ GPT áp đảo — chỉ một paper thử Claude và Claude thắng; hai là chưa paper LLM nào so với test do người viết. Giữ hai ý này, lát em chứng minh bằng ma trận."*' },
          { t: 'slide', n: [17, 18] },
        ],
        quiz: [
          { t: 'mcq', q: 'Trong 13 paper, bao nhiêu dùng LLM?', options: ['4', '9', '13', '6'], correct: 1, explain: '9 LLM (#1–#9) + 4 baseline non-LLM (#10–#13).' },
          { t: 'tf', q: 'Đã có nhiều paper LLM so sánh trực tiếp với test do người viết tay.', answer: false, explain: 'Sai — KHÔNG paper LLM nào làm điều này. Đó là GAP-1.' },
        ],
      },
      {
        id: 'm3l2', title: 'Nhóm LLM (1): RESTGPT, KAT, RESTSpecIT, APITestGenie', mins: 6, slides: [19, 20, 21, 22],
        teach: [
          { t: 'numbers', items: [
            { v: '97%', l: '#1 RESTGPT — precision trích luật (vs 79%)' },
            { v: '+15.7%', l: '#2 KAT — tăng status-code coverage' },
            { v: '88.6%', l: '#3 RESTSpecIT — route discovery (KHÁC code cov!)' },
            { v: '57→80%', l: '#4 APITestGenie — script hợp lệ qua 3 lần thử' },
          ] },
          { t: 'terms', items: [
            ['#1 RESTGPT — vì sao 97%?', 'LLM hiểu mô tả tiếng người (sort_order → ASC/DESC) mà tool từ-khoá bỏ sót'],
            ['#2 KAT — vì sao tăng?', 'GPT dựng đồ thị phụ thuộc, bắc cầu khi tên không khớp (id ↔ flightId)'],
            ['#3 RESTSpecIT — đặc biệt', 'Không cần spec sẵn — vừa suy ra spec vừa test bằng "prompt masking"'],
            ['#4 APITestGenie — mặt trái', 'Sinh script chạy được, nhưng 19 ca ảo giác (hallucination)'],
          ] },
          { t: 'warn', md: '#3 đạt **88.6%** là **route discovery** (tìm endpoint), KHÔNG phải code coverage. Nhớ lại bài "2 loại coverage"!' },
          { t: 'say', md: '*"Bốn paper đầu cho thấy LLM mạnh ở: đọc mô tả (RESTGPT 97%), suy luận phụ thuộc (KAT +15.7%), tự suy ra spec (RESTSpecIT 88.6% route), và sinh script chạy được (APITestGenie 57→80%). Nhưng APITestGenie cũng lộ rủi ro ảo giác."*' },
          { t: 'slide', n: [19, 20, 21, 22] },
        ],
        quiz: [
          { t: 'mcq', q: '#1 RESTGPT đạt 97% precision nhờ đâu?', options: ['Chạy nhiều lần', 'LLM hiểu ngữ nghĩa mô tả tiếng người mà tool từ-khoá bỏ sót', 'Phần cứng mạnh', 'May mắn'], correct: 1, explain: 'Hiểu ngữ cảnh NL là ưu thế cốt lõi của LLM.' },
          { t: 'mcq', q: 'Con số 88.6% của RESTSpecIT là loại coverage nào?', options: ['Code coverage', 'Route/endpoint discovery (KHÁC code coverage)', 'Mutation score', 'Pass rate'], correct: 1, explain: 'Là độ phủ route — không nên nhầm với code coverage (vẫn thấp).' },
          { t: 'flip', front: 'Mặt trái của APITestGenie (#4) là gì?', back: '19 ca ảo giác (hallucination) — import sai, bịa cấu trúc response. Bằng chứng cho rủi ro của LLM.' },
        ],
      },
      {
        id: 'm3l3', title: 'Nhóm LLM (2): RestTSLLM, AutoRestTest, LlamaRestTest, LogiAgent, RESTifAI', mins: 7, slides: [23, 24, 25, 26, 27], key: true,
        teach: [
          { t: 'terms', items: [
            ['#5 RestTSLLM ⭐', 'So 7 LLM — Claude 3.5 thắng tuyệt đối (71.7% branch, 40.8% mutation, 100% success)'],
            ['#6 AutoRestTest', 'GPT + đa tác tử (MARL). Bằng chứng VÀNG: bỏ LLM → coverage rớt 10.9–12.8% (ablation)'],
            ['#7 LlamaRestTest', 'Model NHỎ fine-tune đánh bại GPT: 204 lỗi vs EvoMaster 130'],
            ['#8 LogiAgent', 'Dùng LLM làm "oracle logic" — bắt lỗi trả 200 nhưng sai. Nhưng 33.81% báo nhầm'],
            ['#9 RESTifAI', '128/134 endpoint, tiết kiệm 37% token'],
          ] },
          { t: 'numbers', items: [
            { v: '42 vs 20', l: '#6 AutoRestTest bắt lỗi 500 hơn EvoMaster' },
            { v: '204 vs 130', l: '#7 LlamaRestTest hơn EvoMaster' },
            { v: '−10.9%', l: '#6 ablation: bỏ LLM → coverage rớt (nhân–quả!)' },
          ] },
          { t: 'why', md: '**Ablation của #6 là vũ khí mạnh nhất**: nếu hội đồng hỏi "lấy gì chắc chính LLM tạo ra cải thiện?" → chỉ vào đây: bỏ LLM ra thì coverage rớt 10.9–12.8%.' },
          { t: 'say', md: '*"Nhóm này có nhiều điểm vàng: Claude thắng cả 7 LLM (#5); AutoRestTest chứng minh bằng ablation rằng chính LLM tạo ra cải thiện — bỏ nó ra coverage rớt 11–13%; LlamaRestTest cho thấy model nhỏ fine-tune cũng đánh bại GPT; LogiAgent dùng LLM làm oracle logic."*' },
          { t: 'slide', n: [23, 24, 25, 26, 27] },
        ],
        quiz: [
          { t: 'mcq', q: 'Hội đồng hỏi "lấy gì chắc chính LLM tạo ra cải thiện?" — bằng chứng mạnh nhất?', options: ['#1 RESTGPT 97%', '#6 AutoRestTest ablation: bỏ LLM → coverage rớt 10.9–12.8%', '#9 tiết kiệm token', '#3 route 88.6%'], correct: 1, explain: 'Ablation = thí nghiệm gỡ-bỏ-thành-phần → bằng chứng nhân–quả trực tiếp.' },
          { t: 'flip', front: 'Paper nào chứng minh model NHỎ fine-tune đánh bại GPT?', back: '#7 LlamaRestTest (Llama3-8B): 204 lỗi vs EvoMaster 130; 72.44% input hợp lệ vs RESTGPT 68.82%.' },
          { t: 'tf', q: 'Trong các paper, chỉ có GPT được thử — chưa ai thử Claude.', answer: false, explain: 'Sai — #5 RestTSLLM thử 7 LLM và Claude 3.5 thắng tuyệt đối.' },
        ],
      },
      {
        id: 'm3l4', title: 'Baselines: EvoMaster, No-Time-to-Rest, Morest, DeepREST', mins: 5, slides: [29, 30, 31, 32],
        teach: [
          { t: 'terms', items: [
            ['#10 EvoMaster ⭐', 'Tool DUY NHẤT so với test người — và THUA (41% vs 82%). Hạt giống GAP-1'],
            ['#11 No-Time-to-Rest ⭐', 'Study 10 tool/20 service → trần ~52% line + benchmark EMB (dùng cho thí nghiệm)'],
            ['#12 Morest', 'Model-based, 44 bug (13 mới, 2 ở Bitbucket)'],
            ['#13 DeepREST', 'Deep RL, +17–77% branch + dùng kiểm định Wilcoxon (mẫu cho Phần 6)'],
          ] },
          { t: 'why', md: 'Hai baseline #10 và #11 cho thí nghiệm 2 thứ cần: **EvoMaster** (đối thủ) và **EMB** (tập 20 API chuẩn) + **trần ~52%** để đặt kỳ vọng đúng.' },
          { t: 'say', md: '*"Bốn baseline cho mốc so sánh. Quan trọng nhất là EvoMaster — tool duy nhất so với test người và đã thua; và study No-Time-to-Rest cho ta benchmark EMB cùng con số trần 52% code coverage."*' },
          { t: 'slide', n: [29, 30, 31, 32] },
        ],
        quiz: [
          { t: 'mcq', q: 'Vì sao #10 EvoMaster là paper "then chốt"?', options: ['Mới nhất', 'Là tool DUY NHẤT so với test người viết tay (và thua) → hạt giống GAP-1', 'Dùng LLM', 'Nhiều bug nhất'], correct: 1, explain: 'Manual-vs-tool comparison duy nhất trong corpus → trực tiếp dẫn tới GAP-1.' },
          { t: 'flip', front: '#11 (No-Time-to-Rest) cho thí nghiệm 2 thứ gì?', back: 'Benchmark EMB (20 API chuẩn) + con số trần ~52% line coverage.' },
        ],
      },
    ],
  },

  // ===================================================================== M4
  {
    id: 'm4', icon: '🎯', color: 'red',
    title: 'Khoảng trống (GAP)',
    subtitle: 'Trái tim của bài — 3 chỗ chưa ai làm',
    lessons: [
      {
        id: 'm4l1', title: 'Ma trận so sánh = GAP hiện hình', mins: 5, slides: [35], key: true,
        teach: [
          { t: 'analogy', title: 'Ô trống trong bảng', md: 'Tác giả xếp 13 paper thành 1 bảng. Hai cột bên phải — *"so với thủ công?"* và *"đo Recall trên lỗi gieo sẵn?"* — **gần như trống/đỏ toàn bộ**. Khoảng trống không phải ý kiến; nó **hiện ra thành cột trống**.' },
          { t: 'p', md: 'Cột "so với thủ công" chỉ có **EvoMaster** (non-LLM) ghi Yes — và nó *thua* người. Cột "Recall trên lỗi gieo sẵn" trống toàn bộ (chỉ #5 có mutation score gần đúng).' },
          { t: 'say', md: '*"Đây là slide quan trọng nhất. Em không đọc từng ô — em chỉ vào hai cột phải: so với thủ công chỉ EvoMaster có và nó thua; còn đo Recall trên lỗi gieo sẵn thì trống toàn bộ. Cả 13 paper, không bài nào đặt LLM, người và EvoMaster lên cùng một cân có ground truth."*' },
          { t: 'slide', n: [35] },
        ],
        quiz: [
          { t: 'mcq', q: 'Ma trận so sánh chứng minh điều gì?', options: ['LLM luôn thắng', 'Không paper nào đặt LLM + người + EvoMaster lên cùng 1 cân có ground truth', '13 paper đều giống nhau', 'EvoMaster tốt nhất'], correct: 1, explain: 'Cột trống = chưa ai làm phép so 3 chiều có sự thật nền → đó là GAP.' },
          { t: 'tf', q: 'Khoảng trống là ý kiến chủ quan của tác giả.', answer: false, explain: 'Sai — nó hiện thành cột trống trong bảng, truy được về từng paper.' },
        ],
      },
      {
        id: 'm4l2', title: 'Ba khoảng trống (học thuộc 3 câu)', mins: 6, slides: [36, 37, 38], key: true,
        teach: [
          { t: 'terms', items: [
            ['GAP-1 (So sánh)', 'Chưa ai so LLM ↔ thủ công ↔ EvoMaster CÙNG LÚC trên cùng API'],
            ['GAP-2 (Sự thật nền)', 'Đếm lỗi mà KHÔNG biết tổng → không tính được Recall'],
            ['GAP-3 (Thước đo)', 'Thiếu metric edge-case & bóc tách LOẠI endpoint bị bỏ sót'],
          ] },
          { t: 'analogy', title: 'GAP-2 dễ nhớ nhất', md: 'Nói "tôi bắt được 42 con cá" là **vô nghĩa** nếu không biết hồ có 50 hay 500 con. Phải **giấu sẵn lỗi biết trước** (pre-seeded faults) mới tính được Recall = bắt được ÷ có thật.' },
          { t: 'why', md: 'Ba gap không rời rạc — chúng hợp thành **một thiết kế thí nghiệm**: dùng API có lỗi gieo sẵn (đóng GAP-2), so 3 chiều (đóng GAP-1), đếm edge-case theo loại endpoint (đóng GAP-3).' },
          { t: 'say', md: '*"Có ba khoảng trống: một, chưa ai so LLM với cả người và EvoMaster cùng lúc; hai, fault chỉ được đếm chứ không có sự thật nền nên không tính được Recall; ba, thiếu thước đo edge-case theo loại endpoint. Ba cái này hợp thành một thiết kế thí nghiệm duy nhất."*' },
          { t: 'slide', n: [36, 37, 38] },
        ],
        quiz: [
          { t: 'mcq', q: 'GAP-2 nói về điều gì?', options: ['Thiếu so sánh với người', 'Đếm lỗi mà không có ground truth → không tính được Recall', 'Coverage thấp', 'Thiếu LLM'], correct: 1, explain: 'Không biết tổng số lỗi thì "bắt 42 lỗi" vô nghĩa — cần lỗi gieo sẵn.' },
          { t: 'order', prompt: 'Ghép số GAP với chủ đề (kéo đúng thứ tự 1→2→3):', items: ['GAP-1: So sánh 3 chiều', 'GAP-2: Sự thật nền / Recall', 'GAP-3: Thước đo edge-case'] },
          { t: 'cloze', before: 'Để tính được Recall, thí nghiệm phải dùng API có ', answer: 'lỗi gieo sẵn', after: ' (pre-seeded faults) để biết tổng số lỗi.', options: ['lỗi gieo sẵn', 'nhiều endpoint', 'GPT-4'] },
        ],
      },
      {
        id: 'm4l3', title: 'Tuyên bố GAP hợp nhất', mins: 3, slides: [39],
        teach: [
          { t: 'p', md: 'Gói gọn: *"Dù LLM đã đạt tới 71.78% line coverage và vượt EvoMaster về phát hiện lỗi, các nghiên cứu vẫn (1) không so với cả người + EvoMaster, (2) không có ground truth để tính Recall, (3) thiếu metric edge-case theo loại endpoint."*' },
          { t: 'p', md: '**Đóng góp** của bài: một tool sinh test bằng LLM + báo cáo đánh giá trên **3 API EMB có lỗi gieo sẵn**, trả lời RQ1/RQ2/RQ3 → đóng cả 3 gap.' },
          { t: 'say', md: '*"Tóm lại, dù LLM đã rất mạnh, ba hạn chế vẫn còn. Đóng góp của em là một tool cộng một báo cáo đánh giá trên 3 API có lỗi gieo sẵn, trả lời ba câu hỏi nghiên cứu, khép cả ba khoảng trống."*' },
          { t: 'slide', n: [39] },
        ],
        quiz: [
          { t: 'mcq', q: 'Đóng góp chính của bài là gì?', options: ['Một LLM mới', 'Tool sinh test bằng LLM + báo cáo đánh giá trên 3 API EMB có lỗi gieo sẵn (đóng 3 gap)', 'Một benchmark mới', 'Một thư viện'], correct: 1, explain: 'Tool + đánh giá có kiểm soát trên lỗi gieo sẵn → khép GAP-1/2/3.' },
        ],
      },
    ],
  },

  // ===================================================================== M5
  {
    id: 'm5', icon: '🧪', color: 'indigo',
    title: 'Câu hỏi & Thí nghiệm',
    subtitle: 'Biến GAP thành câu hỏi đo được + cách kiểm chứng',
    lessons: [
      {
        id: 'm5l1', title: 'Từ RQ thô → RQ tinh chỉnh (4 thay đổi)', mins: 5, slides: [41, 42, 43],
        teach: [
          { t: 'p', md: 'Câu hỏi ban đầu (RQ thô) được **tinh chỉnh 4 lần**, mỗi thay đổi đều truy về evidence table — KHÔNG tự đặt:' },
          { t: 'terms', items: [
            ['1. Baseline', 'chỉ "thủ công" → THÊM EvoMaster (baseline phổ biến nhất)'],
            ['2. Dataset', '"REST API chung" → 3 API EMB + lỗi gieo sẵn'],
            ['3. LLM cụ thể', '"LLM" chung → GPT-4o/GPT-4-Turbo (vì GPT thống trị literature)'],
            ['4. Metric', '"≥2 bug" mơ hồ → số lỗi gieo sẵn bắt được + đếm edge-case'],
          ] },
          { t: 'say', md: '*"Em không tự đặt ngưỡng rồi đi chứng minh. Bốn thay đổi so với câu hỏi ban đầu đều có nguồn từ evidence table: thêm EvoMaster vì là baseline phổ biến nhất, dùng EMB + gieo lỗi, chọn GPT vì nó thống trị, và đổi metric mơ hồ thành đo được."*' },
          { t: 'slide', n: [41, 42, 43] },
        ],
        quiz: [
          { t: 'mcq', q: 'Vì sao thí nghiệm chọn GPT (chứ không model khác)?', options: ['GPT rẻ nhất', 'Vì họ GPT thống trị các paper LLM → đại diện SOTA, có nguồn từ evidence table', 'Ngẫu nhiên', 'GPT dễ dùng'], correct: 1, explain: 'Mọi tinh chỉnh truy về evidence table — không tự đặt.' },
          { t: 'tf', q: 'Tác giả tự đặt ngưỡng 90% rồi đi chứng minh.', answer: false, explain: 'Sai — ngưỡng & mọi lựa chọn đều truy về bằng chứng (decision log 4 thay đổi).' },
        ],
      },
      {
        id: 'm5l2', title: 'Main RQ + RQ1/RQ2/RQ3', mins: 5, slides: [43],
        teach: [
          { t: 'p', md: '**Main RQ:** *"LLM sinh test từ OpenAPI hiệu quả tới mức nào, so với thủ công và EvoMaster, trên API có lỗi gieo sẵn?"*' },
          { t: 'terms', items: [
            ['RQ1 (Coverage)', 'LLM có đạt endpoint coverage ≥90%? Loại endpoint nào hay bị bỏ? → đóng GAP-3'],
            ['RQ2 (Fault) ⭐', 'LLM bắt bao nhiêu lỗi gieo sẵn so với thủ công & EvoMaster? → đóng GAP-1+2'],
            ['RQ3 (Edge-case)', 'LLM sinh nhiều kịch bản 4xx/5xx + biên hơn thủ công không? → đóng GAP-3'],
          ] },
          { t: 'why', md: '3 RQ **không trùng nhau**: RQ1 đo *phủ*, RQ2 đo *bắt lỗi có ground truth*, RQ3 đo *chất lượng edge-case*. Cùng nhau đóng cả 3 gap.' },
          { t: 'say', md: '*"Câu hỏi chính chia thành ba: RQ1 đo độ phủ endpoint và loại nào bị bỏ; RQ2 — quan trọng nhất — so số lỗi gieo sẵn bắt được giữa LLM, người và EvoMaster; RQ3 đo số kịch bản edge-case. Mỗi câu đóng một đến hai khoảng trống."*' },
          { t: 'slide', n: [43] },
        ],
        quiz: [
          { t: 'mcq', q: 'RQ nào là "trái tim" (đóng cả GAP-1 và GAP-2)?', options: ['RQ1', 'RQ2 (so số lỗi gieo sẵn: LLM vs thủ công vs EvoMaster)', 'RQ3', 'Main RQ'], correct: 1, explain: 'RQ2 là phép so 3 chiều đầu tiên trên ground truth → đóng GAP-1 + GAP-2.' },
          { t: 'flip', front: 'RQ1 đo gì?', back: 'Endpoint coverage (có đạt ≥90%?) + bóc tách loại endpoint nào hay bị bỏ sót (CRUD/auth/error).' },
        ],
      },
      {
        id: 'm5l3', title: 'Giả thuyết H0/H1 + kiểm định (siêu đơn giản)', mins: 6, slides: [45, 46, 47], key: true,
        teach: [
          { t: 'analogy', title: 'H0 vs H1', md: '**H0 (giả thuyết không)** = điều ta muốn *bác bỏ* ("LLM KHÔNG hơn"). **H1 (giả thuyết đối)** = điều ta *kỳ vọng* ("LLM hơn"). Ta thu dữ liệu; nếu đủ mạnh để bác H0 (p < 0.05) thì kết luận H1.' },
          { t: 'terms', items: [
            ['p < 0.05', 'Xác suất kết quả là do may rủi < 5% → đủ tin để bác H0'],
            ['Wilcoxon', 'Kiểm định phi tham số (không cần dữ liệu phân phối chuẩn) — hợp mẫu nhỏ'],
            ['Friedman', 'So 3 nhóm liên hệ cùng lúc (LLM/người/EvoMaster trên cùng API) — dùng cho RQ2'],
          ] },
          { t: 'why', md: 'Vì sao chọn phi tham số (Wilcoxon/Friedman)? Vì mẫu **nhỏ (3 API)** và các nhóm **phụ thuộc** (đo trên cùng API). Tác giả còn thành thật bù bằng phân tích từng-lỗi (McNemar) vì power thấp.' },
          { t: 'say', md: '*"Mỗi câu hỏi có một cặp giả thuyết: H0 là điều em muốn bác bỏ, H1 là điều em kỳ vọng. Em dùng kiểm định Wilcoxon và Friedman — loại phi tham số, phù hợp mẫu nhỏ. Nếu p nhỏ hơn 0.05 thì khác biệt là thật, không phải may rủi."*' },
          { t: 'slide', n: [45, 46, 47] },
        ],
        quiz: [
          { t: 'mcq', q: '"p < 0.05" nghĩa là gì?', options: ['LLM tốt hơn 5%', 'Xác suất kết quả do may rủi < 5% → đủ tin để bác H0', 'Có 5 paper', 'Sai số 5cm'], correct: 1, explain: 'p-value nhỏ = khó xảy ra ngẫu nhiên → khác biệt có ý nghĩa thống kê.' },
          { t: 'flip', front: 'H0 (giả thuyết không) là gì?', back: 'Điều ta muốn BÁC BỎ — ví dụ "LLM không bắt nhiều lỗi hơn người/EvoMaster". H1 là điều kỳ vọng (LLM hơn).' },
          { t: 'mcq', q: 'Vì sao dùng kiểm định phi tham số (Wilcoxon/Friedman)?', options: ['Cho oai', 'Vì mẫu nhỏ (3 API) + nhóm phụ thuộc → không cần giả định phân phối chuẩn', 'Vì dễ tính', 'Vì máy tính bắt buộc'], correct: 1, explain: 'Mẫu nhỏ + nhóm liên hệ → phi tham số là lựa chọn đúng.' },
        ],
      },
      {
        id: 'm5l4', title: 'Thiết kế thí nghiệm + đóng góp', mins: 4, slides: [48],
        teach: [
          { t: 'p', md: 'Thiết kế = **một bàn cân, ba generator**: lấy 3 API từ EMB, gieo lỗi biết trước, rồi cho 3 bên sinh test: **LLM (GPT-4o) · Thủ công · EvoMaster**. Đo O1 (coverage) / O2 (lỗi bắt được) / O3 (edge-case), α=0.05.' },
          { t: 'numbers', items: [{ v: '3', l: 'API EMB có lỗi gieo sẵn' }, { v: '3', l: 'generator: LLM / người / EvoMaster' }, { v: '3', l: 'outcome đo: O1/O2/O3' }] },
          { t: 'say', md: '*"Thiết kế đơn giản: ba API từ benchmark EMB, gieo lỗi biết trước, rồi cho ba bên cùng sinh test — LLM, người, và EvoMaster — trên cùng một bàn cân. Đo độ phủ, số lỗi bắt được, và số kịch bản edge-case. Đây là phép so ba chiều đầu tiên trên ground truth chung."*' },
          { t: 'slide', n: [48] },
        ],
        quiz: [
          { t: 'mcq', q: 'Ba "generator" được so trong thí nghiệm là?', options: ['GPT, Claude, Gemini', 'LLM, Thủ công (người), EvoMaster', 'EvoMaster, Morest, RESTler', 'RQ1, RQ2, RQ3'], correct: 1, explain: 'Phép so 3 chiều LLM ↔ người ↔ EvoMaster — điểm mới của bài.' },
          { t: 'tf', q: 'Thí nghiệm dùng API có lỗi gieo sẵn để biết tổng số lỗi.', answer: true, explain: 'Đúng — nhờ vậy mới tính được Recall (đóng GAP-2).' },
        ],
      },
    ],
  },

  // ===================================================================== M6
  {
    id: 'm6', icon: '🏆', color: 'gold',
    title: 'Hero: Bảo vệ',
    subtitle: 'Chốt hạ + chống mọi câu hỏi bắt bẻ',
    lessons: [
      {
        id: 'm6l1', title: 'Chuỗi nhân–quả 5 câu (học thuộc)', mins: 4, slides: [50], key: true,
        teach: [
          { t: 'p', md: 'Đây là "linh hồn" cả bài — luyện nói trôi trong 30 giây:' },
          { t: 'say', md: '**(1) VÌ** test tự động bị chặn ~52% và còn thua người (41% vs 82%), **(2) VÀ** LLM hứa hẹn vượt qua (đọc NL, sinh giá trị thật, ablation chứng minh), **(3) NÊN** em làm SLR sàng ~280→13 paper chất lượng cao, **(4) PHÁT HIỆN** 3 gap (so sánh / ground truth / edge-case), **(5) DO ĐÓ** đề xuất thí nghiệm 3 API EMB có lỗi gieo sẵn — khép cả 3.' },
          { t: 'why', md: 'Mỗi mệnh đề "vì/nên" đều có **số + trích dẫn** phía sau. Đó là thứ khiến bài khó bắt bẻ: không bước nào là cảm tính.' },
          { t: 'slide', n: [50] },
        ],
        quiz: [
          { t: 'order', prompt: 'Sắp đúng 5 mắt xích của chuỗi nhân–quả:', items: ['VÌ test tự động ~52% & thua người', 'VÀ LLM hứa hẹn vượt qua', 'NÊN làm SLR 280→13', 'PHÁT HIỆN 3 gap', 'DO ĐÓ đề xuất thí nghiệm'] },
        ],
      },
      {
        id: 'm6l2', title: 'Tính chính trực (ghi điểm với hội đồng)', mins: 4, slides: [51], key: true,
        teach: [
          { t: 'p', md: 'Người yếu giấu điểm yếu; người mạnh **khai báo trước**. Bài chủ động báo 3 chỗ chưa hoàn hảo trong 104 trích dẫn:' },
          { t: 'terms', items: [
            ['Gỡ được dấu †', 'evidence-table từng nghi 3 số của RestTSLLM — đã tìm thấy ở Table 3 trang 9 → điểm CỘNG'],
            ['2 chỗ lệch trang nhỏ', 'EvoMaster "only manual" ở Conclusion p.11–12; LogiAgent "49 crash" là tổng bảng — câu vẫn thật'],
            ['1 claim future-work', 'RESTGPT "limitation" thực ra là mục Future Work — trình bày đúng như paper'],
          ] },
          { t: 'say', md: '*"Em chủ động báo ba chỗ chưa hoàn hảo trong 104 trích dẫn. Chính sự khai báo này khiến hội đồng tin được 101 trích dẫn còn lại — 102/104 đã khớp verbatim tuyệt đối với PDF gốc."*' },
          { t: 'slide', n: [51] },
        ],
        quiz: [
          { t: 'mcq', q: 'Vì sao chủ động khai báo điểm yếu lại GHI ĐIỂM?', options: ['Để bài ngắn hơn', 'Vì nó làm hội đồng TIN các phần còn lại — thể hiện sự trung thực & kỹ lưỡng', 'Vì bắt buộc', 'Để xin điểm'], correct: 1, explain: 'Trung thực có chọn lọc = đòn tâm lý mạnh, tăng độ tin cậy tổng thể.' },
          { t: 'tf', q: '"Gỡ được dấu †" của RestTSLLM là một điểm cộng cho bài.', answer: true, explain: 'Đúng — chứng tỏ tác giả không nhận bừa số liệu, đi kiểm tới cùng (tìm thấy ở Table 3 p.9).' },
        ],
      },
      {
        id: 'm6l3', title: 'Q&A: 6 câu hỏi khó + trả lời sẵn', mins: 6, slides: [52], key: true,
        teach: [
          { t: 'terms', items: [
            ['"90% coverage rồi, gap đâu?"', 'Đó là ENDPOINT cov; CODE cov vẫn ~52%; chưa ai kiểm trên lỗi gieo sẵn + bóc loại endpoint'],
            ['"Chỉ 3 API đủ không?"', 'Threat đã nêu; bù bằng McNemar per-fault + effect size; #10 dùng 3, #12 dùng 6 — đúng tầm'],
            ['"Sao chọn GPT?"', 'GPT thống trị literature; #5 cho thấy Claude cũng mạnh → mở rộng được'],
            ['"Lấy gì chắc LLM có ích?"', 'Ablation #6: bỏ LLM → coverage rớt 10.9–12.8%'],
            ['"Mutation #5 = ground truth rồi?"', 'Mutant tự sinh, 6 API tự dựng, không so người/EvoMaster — khác lỗi gieo sẵn dùng chung'],
            ['"Số liệu SLR tin được?"', '104 trích dẫn verify tới trang; 13 PDF tải sẵn; 2 lệch trang + 1 not-present đã khai báo'],
          ] },
          { t: 'warn', md: 'Học thuộc 6 cặp này. Câu **#1 (2 loại coverage)** và **#4 (ablation)** bị hỏi nhiều nhất.' },
          { t: 'slide', n: [52] },
        ],
        quiz: [
          { t: 'mcq', q: '"Chỉ 3 API thì sao tổng quát?" — trả lời tốt nhất?', options: ['Thừa nhận bài yếu', 'Threat đã nêu; bù bằng phân tích per-fault (McNemar) + effect size; #10 dùng 3, #12 dùng 6 — đúng tầm', 'Nói 3 là đủ rồi', 'Đổi chủ đề'], correct: 1, explain: 'Thành thật về giới hạn + nêu cách bù đắp = câu trả lời mạnh.' },
          { t: 'mcq', q: '"Mutation score của #5 chẳng phải ground truth rồi?" — phản biện?', options: ['Đồng ý, bỏ GAP-2', 'Đó là mutant TỰ SINH trên 6 API tự dựng, không so người/EvoMaster — khác lỗi gieo sẵn dùng chung', 'Không biết', 'Mutation sai'], correct: 1, explain: 'Mutant tự sinh ≠ lỗi gieo sẵn thực tế trên benchmark chung → GAP-2 vẫn đứng.' },
        ],
      },
      {
        id: 'm6l4', title: 'Diễn tập toàn bộ deck (Rehearsal)', mins: 10, slides: [], rehearsal: true,
        teach: [
          { t: 'p', md: 'Đây là phòng tập cuối. Chế độ **Rehearsal** sẽ hiện tên từng slide; bạn tự nói trong đầu → bấm "Hiện lời thoại" để so → tự chấm. Lặp tới khi trôi cả 59 slide.' },
          { t: 'p', md: 'Mẹo: đừng học vẹt. Với mỗi slide hỏi bản thân *"slide này tồn tại để chứng minh điều gì?"* rồi nói lý do đó.' },
          { t: 'say', md: 'Khi đã trôi: bạn là **Hero** — present được toàn bộ mà không cần đọc paper. Chúc bảo vệ tốt! 🎓' },
        ],
        quiz: [],
      },
    ],
  },
];

// flat list of all lessons (for progress + navigation)
export const allLessons = course.flatMap((m) => m.lessons.map((l) => ({ ...l, moduleId: m.id, moduleTitle: m.title, color: m.color })));
export const totalLessons = allLessons.length;

// ---- Q&A defense bank (6 câu hỏi khó nhất của hội đồng) ----
export const defenseQA = [
  { t: 'mcq', q: 'Hội đồng: "Đã có tool đạt >90% coverage rồi, vậy gap ở đâu?"', options: ['Thừa nhận hết gap', 'Đó là ENDPOINT coverage (#9 ~95%); CODE coverage vẫn ~52%; và chưa ai kiểm trên lỗi gieo sẵn + bóc tách loại endpoint', 'Nói con số đó sai', 'Đổi sang câu khác'], correct: 1, explain: 'Phân biệt 2 loại coverage là câu trả lời "vàng" — endpoint cao ≠ code cao.' },
  { t: 'mcq', q: 'Hội đồng: "Chỉ 3 API thì sao đủ tổng quát?"', options: ['3 là quá đủ', 'Đây là threat em đã nêu; em bù bằng phân tích từng-lỗi (McNemar) + effect size; EvoMaster dùng 3, Morest dùng 6 — đúng tầm', 'Tại không có thời gian', 'Sẽ làm thêm sau'], correct: 1, explain: 'Thành thật về giới hạn + nêu cách bù đắp = câu trả lời mạnh, không phòng thủ yếu.' },
  { t: 'mcq', q: 'Hội đồng: "Sao chọn GPT mà không phải model khác?"', options: ['GPT nổi tiếng nhất', 'Vì họ GPT thống trị các paper LLM (#1,2,4,6) → đại diện SOTA; và #5 cho thấy Claude cũng mạnh nên có thể mở rộng so model', 'GPT rẻ nhất', 'Ngẫu nhiên'], correct: 1, explain: 'Lựa chọn truy về evidence table (decision-log #3), không tự đặt.' },
  { t: 'mcq', q: 'Hội đồng: "Lấy gì chắc chính LLM tạo ra cải thiện, không phải may rủi?"', options: ['Vì LLM thông minh', 'Ablation của AutoRestTest (#6): bỏ LLM ra thì coverage rớt 10.9–12.8% — bằng chứng nhân–quả trực tiếp', 'Vì coverage cao', 'Không chứng minh được'], correct: 1, explain: 'Ablation (thí nghiệm gỡ-bỏ-thành-phần) là bằng chứng nhân–quả mạnh nhất.' },
  { t: 'mcq', q: 'Hội đồng: "Mutation score của #5 chẳng phải đã là ground truth rồi sao?"', options: ['Đúng, vậy bỏ GAP-2', 'Đó là mutant TỰ SINH trên 6 API tự dựng, không so với người/EvoMaster — khác với lỗi gieo sẵn thực tế trên benchmark chung', 'Mutation score sai', 'Không rõ'], correct: 1, explain: 'Mutant tự sinh ≠ lỗi gieo sẵn dùng chung → GAP-2 vẫn đứng vững.' },
  { t: 'mcq', q: 'Hội đồng: "Làm sao tin số liệu trong SLR của em?"', options: ['Em đọc kỹ rồi', '104 trích dẫn đã verify tới từng trang, 13 PDF gốc tải sẵn để kiểm; 2 chỗ lệch trang nhỏ + 1 claim future-work em đã chủ động khai báo', 'Vì paper uy tín', 'Tin em đi'], correct: 1, explain: 'Tựa vào tính truy vết được + chủ động khai báo điểm yếu = đáng tin nhất.' },
];

// pool câu hỏi khái niệm có chấm điểm (mcq/tf/cloze) gom từ mọi bài
export const conceptPool = allLessons.flatMap((l) =>
  (l.quiz || []).filter((q) => ['mcq', 'tf', 'cloze'].includes(q.t)).map((q) => ({ ...q, _mod: l.moduleTitle }))
);

// order item của chuỗi nhân–quả (m6l1)
export const causalChainItem = (allLessons.find((l) => l.id === 'm6l1')?.quiz || []).find((q) => q.t === 'order');
