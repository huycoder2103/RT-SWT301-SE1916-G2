import { useMemo, useState } from 'react';
import Quiz from './Quiz.jsx';
import { conceptPool, defenseQA, causalChainItem } from '../data/course';

function sample(arr, n) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a.slice(0, n);
}

export default function MockDefense({ best, onFinish, onHome, onRehearsal, onCheatSheet }) {
  const [phase, setPhase] = useState('intro'); // intro | test | verdict
  const [attempt, setAttempt] = useState(0);
  const [score, setScore] = useState(0);

  const items = useMemo(() => {
    const concept = sample(conceptPool, 10);
    const qa = sample(defenseQA, defenseQA.length);
    const base = causalChainItem ? [causalChainItem] : [];
    return [...base, ...concept, ...qa].map((q, i) => ({ ...q, __k: `mk${attempt}-${i}` }));
  }, [attempt]);

  const start = () => { setAttempt((a) => a + 1); setPhase('test'); window.scrollTo(0, 0); };
  const finish = (s) => { setScore(s); setPhase('verdict'); onFinish(s); window.scrollTo(0, 0); };

  const verdict = score >= 85
    ? { emoji: '🏆', t: 'SẴN SÀNG BẢO VỆ!', sub: 'Bạn nắm chắc bài. Giờ chỉ cần đọc trôi là xong.', cls: 'ok' }
    : score >= 65
      ? { emoji: '💪', t: 'Gần sẵn sàng', sub: 'Hiểu khá rồi — ôn lại các bài trọng tâm rồi thi lại để chạm 85%.', cls: 'mid' }
      : { emoji: '📚', t: 'Cần luyện thêm', sub: 'Quay lại học từ các chương còn yếu, rồi thi thử lại.', cls: 'low' };

  if (phase === 'intro') {
    return (
      <div className="lesson">
        <h2 className="lh">🎯 Phòng Bảo Vệ Thử</h2>
        <p className="tb p">Bài thi tổng hợp để biết bạn <b>đã sẵn sàng bảo vệ chưa</b>. Gồm 3 phần, chấm điểm khách quan:</p>
        <div className="tb terms">
          <div className="trow"><div className="tk">1. Chuỗi nhân–quả</div><div className="tv">Sắp đúng 5 mắt xích cốt lõi của cả bài</div></div>
          <div className="trow"><div className="tk">2. Khái niệm (10 câu)</div><div className="tv">Random từ toàn bộ khóa học — kiểm tra hiểu thật</div></div>
          <div className="trow"><div className="tk">3. Q&amp;A bảo vệ (6 câu)</div><div className="tv">6 câu hỏi khó nhất hội đồng có thể hỏi</div></div>
        </div>
        <div className="tb why"><div className="ic" /><div><b>Ngưỡng sẵn sàng: ≥ 85%.</b> Đạt mức này nghĩa là bạn trả lời được câu hỏi + hiểu vì sao — phần còn lại chỉ là đọc trôi (Diễn tập).</div></div>
        {best > 0 && <div className="tb slide">Điểm thi thử tốt nhất: {best}%</div>}
        <div className="lnav">
          <button className="btn ghost" onClick={onHome}>← Bản đồ</button>
          <button className="btn primary" onClick={start}>Bắt đầu thi thử →</button>
        </div>
      </div>
    );
  }

  if (phase === 'test') {
    return (
      <div className="lesson">
        <div className="lcrumb"><b>🎯 Bảo vệ thử</b> · 17 câu · không hiện đáp án trước</div>
        <h2 className="lh">Giữ bình tĩnh — trả lời như đang đứng trước hội đồng</h2>
        <div className="lprog"><i style={{ width: '60%' }} /></div>
        <Quiz key={attempt} items={items} onComplete={finish} />
      </div>
    );
  }

  return (
    <div className="lesson">
      <div className={`done-card`}>
        <div className="big">{verdict.emoji}</div>
        <h3>{verdict.t}</h3>
        <div className="score">Điểm thi thử: {score}/100 {best > score ? `· kỷ lục ${best}%` : '· kỷ lục mới!'}</div>
        <p className="tb p" style={{ textAlign: 'center', maxWidth: 440, margin: '0 auto 16px' }}>{verdict.sub}</p>
        <div className="lnav" style={{ justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn ghost" onClick={() => { setPhase('intro'); }}>Thi lại</button>
          <button className="btn ghost" onClick={onCheatSheet}>🧾 Phao thi</button>
          <button className="btn primary" onClick={onRehearsal}>🎤 Vào diễn tập</button>
        </div>
        <div style={{ marginTop: 12 }}><button className="btn ghost" onClick={onHome}>Về bản đồ</button></div>
      </div>
    </div>
  );
}
