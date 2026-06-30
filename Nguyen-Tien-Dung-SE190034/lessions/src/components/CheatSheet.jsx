import { HERO_LINE, defenseQA } from '../data/course';
import slides from '../data/slides.json';

const NUMBERS = [
  ['~52%', 'trần code coverage tool cũ (#11)'],
  ['41% vs 82%', 'EvoMaster gen THUA test người (#10)'],
  ['97% · +329%', 'RESTGPT precision · input hợp lệ vs ARTE (#1)'],
  ['71.7% / 40.8%', 'Claude 3.5 branch cov / mutation (#5, Table 3 p.9)'],
  ['42 vs 20', 'AutoRestTest lỗi 500 hơn EvoMaster (#6)'],
  ['−10.9–12.8%', 'bỏ LLM → coverage rớt (ablation #6)'],
  ['204 vs 130', 'LlamaRestTest fault hơn EvoMaster (#7)'],
  ['71.78% line', 'LogiAgent — cao nhất nhóm LLM (#8)'],
  ['128/134', 'RESTifAI operations vs AutoRestTest 33 (#9)'],
  ['280 → 13', 'PRISMA: thô → cuối (9 LLM + 4 baseline)'],
  ['5.73/6', 'điểm chất lượng trung bình'],
  ['104 · 102', 'trích dẫn · đã verify verbatim'],
];
const GAPS = [
  ['GAP-1 So sánh', 'Chưa ai so LLM ↔ thủ công ↔ EvoMaster CÙNG LÚC trên cùng API'],
  ['GAP-2 Ground truth', 'Đếm lỗi mà không biết tổng → không tính được Recall (cần lỗi gieo sẵn)'],
  ['GAP-3 Thước đo', 'Thiếu metric edge-case & bóc tách loại endpoint bị bỏ sót'],
];
const RQS = [
  ['Main RQ', 'LLM sinh test từ OpenAPI hiệu quả tới đâu, so với thủ công & EvoMaster, trên API có lỗi gieo sẵn?'],
  ['RQ1 (coverage)', '≥90% endpoint? loại nào bị bỏ? · H0: ≤90% / H1: >90% · Wilcoxon 1 mẫu'],
  ['RQ2 (fault) ⭐', 'LLM vs thủ công vs EvoMaster bắt lỗi gieo sẵn · Friedman + post-hoc Wilcoxon'],
  ['RQ3 (edge-case)', 'LLM vs thủ công số kịch bản 4xx/5xx+biên · Wilcoxon ghép cặp · α=0.05'],
];

export default function CheatSheet({ onHome }) {
  return (
    <div className="cheat-wrap">
      <div className="cheat-toolbar no-print">
        <button className="btn ghost" onClick={onHome}>← Bản đồ</button>
        <div className="grow" />
        <button className="btn primary" onClick={() => window.print()}>🖨 In / Lưu PDF</button>
      </div>

      <div className="cheat">
        <header className="ch-head">
          <h1>PHAO THI — Thuyết trình SLR (LLM × REST API Testing)</h1>
          <div className="ch-sub">SE1916 · Nguyễn Tiến Dũng SE190034 · liếc nhanh khi quên — đừng đọc nguyên văn</div>
        </header>

        <section className="ch-hero">
          <div className="ch-lbl">🎯 Chuỗi nhân–quả (đọc trôi câu này = nắm cả bài)</div>
          <p>{HERO_LINE}</p>
        </section>

        <div className="ch-cols">
          <section>
            <div className="ch-lbl">📊 Số liệu phải nhớ</div>
            <table className="ch-tbl">
              <tbody>{NUMBERS.map(([v, l], i) => <tr key={i}><td className="ch-v">{v}</td><td>{l}</td></tr>)}</tbody>
            </table>
          </section>

          <section>
            <div className="ch-lbl">🎯 3 Khoảng trống</div>
            {GAPS.map(([k, v], i) => <div className="ch-row" key={i}><b>{k}:</b> {v}</div>)}
            <div className="ch-lbl" style={{ marginTop: 12 }}>🧪 Câu hỏi & Giả thuyết</div>
            {RQS.map(([k, v], i) => <div className="ch-row" key={i}><b>{k}:</b> {v}</div>)}
          </section>
        </div>

        <section>
          <div className="ch-lbl">🛡 Q&amp;A — 6 câu khó & cách trả lời</div>
          {defenseQA.map((q, i) => (
            <div className="ch-qa" key={i}>
              <div className="ch-q">{q.q.replace(/^Hội đồng:\s*/, '')}</div>
              <div className="ch-a">→ {q.options[q.correct]}</div>
            </div>
          ))}
        </section>

        <section>
          <div className="ch-lbl">🖥 Cue 59 slide (số + tên → nhớ slide đó nói gì)</div>
          <div className="ch-slides">
            {slides.map((s) => (
              <div className="ch-slide" key={s.id}><span className="ch-n">{s.n}</span> {s.title}</div>
            ))}
          </div>
        </section>

        <footer className="ch-foot">Mọi con số đều dẫn được tới trang trong PDF gốc · 13 PDF sẵn trong presentation/papers · "mọi khẳng định của em đều có nguồn".</footer>
      </div>
    </div>
  );
}
