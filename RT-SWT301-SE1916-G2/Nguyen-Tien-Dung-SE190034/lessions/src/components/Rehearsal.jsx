import { useMemo, useState } from 'react';
import slides from '../data/slides.json';

export default function Rehearsal({ onHome }) {
  const [i, setI] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [rated, setRated] = useState(0);
  const s = slides[i];
  const last = i === slides.length - 1;
  const isDivider = /divider/.test(s.cls);
  const notes = useMemo(() => (s.notes && s.notes.trim()) ? s.notes : '<p class="muted">Slide phân mục / chuyển phần — chỉ cần nói một câu dẫn sang phần tiếp theo.</p>', [s]);

  function rate() { setRated((r) => r + 1); if (last) return; setI(i + 1); setRevealed(false); }

  if (i >= slides.length) return null;

  return (
    <div className="reh">
      <div className="rprog"><span>Diễn tập slide {i + 1} / {slides.length}</span><span>đã luyện: {rated}</span></div>
      <div className="lprog"><i style={{ width: ((i + 1) / slides.length * 100) + '%' }} /></div>

      <div className="rehstage">
        <div className="rkick">{isDivider ? 'Slide phân mục' : 'Slide ' + (i + 1)}</div>
        <div className="rtitle">{s.title}</div>

        {!revealed ? (
          <>
            <div className="prompt">🤔 <b>Tự hỏi:</b> slide này tồn tại để chứng minh điều gì? Bạn sẽ nói gì? (nghĩ trong đầu hoặc nói ra miệng)</div>
            <div className="lnav" style={{ marginTop: 'auto' }}>
              <button className="btn ghost" onClick={onHome}>← Thoát</button>
              <button className="btn primary" onClick={() => setRevealed(true)}>Hiện lời thoại 🎤</button>
            </div>
          </>
        ) : (
          <>
            <div className="reveal" dangerouslySetInnerHTML={{ __html: notes }} />
            <div className="rate">
              <button className="again" onClick={rate}>😵 Chưa thuộc</button>
              <button className="good" onClick={rate}>🙂 Tạm ổn</button>
              <button className="easy" onClick={rate}>😎 Trôi chảy</button>
            </div>
          </>
        )}
      </div>

      {last && revealed && (
        <div className="done-card" style={{ marginTop: 20 }}>
          <div className="big">🏆</div>
          <h3>Bạn đã diễn tập hết 59 slide!</h3>
          <div className="score">Giờ bạn là Hero — present được toàn bộ deck mà không cần đọc paper.</div>
          <div className="lnav" style={{ justifyContent: 'center' }}>
            <button className="btn primary" onClick={onHome}>Về bản đồ 🎓</button>
          </div>
        </div>
      )}
    </div>
  );
}
