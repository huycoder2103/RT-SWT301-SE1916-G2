import { course, allLessons } from '../data/course';
import { readiness, moduleProgress, nextLesson } from '../data/progress';

const ACCENT = { teal: 'var(--teal)', indigo: 'var(--indigo)', red: 'var(--red)', gold: 'var(--gold)' };
const GRAD = {
  teal: 'linear-gradient(135deg,#0E8C84,#0A655F)',
  indigo: 'linear-gradient(135deg,#6366F1,#4338CA)',
  red: 'linear-gradient(135deg,#E5544B,#B91C1C)',
  gold: 'linear-gradient(135deg,#E0B400,#B98900)',
};

export default function Home({ progress, onOpen, onMock, onCheat, mock = 0 }) {
  const ready = readiness(progress);
  const nextId = nextLesson(progress);
  const nextLes = allLessons.find((l) => l.id === nextId);
  const started = ready > 0;

  return (
    <div>
      <section className="hero">
        <div className="htxt">
          <div className="eyebrow">Khóa học · Zero → Hero</div>
          <h1>Thuyết trình <span className="g">SLR LLM × REST API</span><br />mà không cần đọc paper</h1>
          <p>Học từng khái niệm bằng ví dụ đời thường, luyện quiz, rồi diễn tập cả 59 slide. Hết khóa: bạn present được toàn bộ bài một cách tự tin.</p>
          <button className="cta" onClick={() => onOpen(nextId)}>
            {started ? `Tiếp tục → ${nextLes?.title}` : 'Bắt đầu từ con số 0 →'}
          </button>
        </div>
        <div className="ring" style={{ '--p': ready }}>
          <div className="rin"><div className="rv">{ready}%</div><div className="rl">sẵn sàng</div></div>
        </div>
      </section>

      <div className="actions">
        <button className="actcard mock" onClick={onMock}>
          <div className="ai">🎯</div>
          <div><div className="at">Bảo vệ thử</div><div className="as">{mock ? `Kỷ lục ${mock}% · thi lại để chạm 85%` : 'Kiểm tra khách quan: bạn đã sẵn sàng bảo vệ chưa?'}</div></div>
        </button>
        <button className="actcard cheat" onClick={onCheat}>
          <div className="ai">🧾</div>
          <div><div className="at">Phao thi (in được)</div><div className="as">1 trang: chuỗi nhân–quả · số liệu · Q&amp;A · cue 59 slide</div></div>
        </button>
      </div>

      {course.map((m) => {
        const mp = moduleProgress(progress, m.lessons);
        return (
          <section className="modsec" key={m.id}>
            <div className="modhead">
              <div className="disc" style={{ background: GRAD[m.color] }}>{m.icon}</div>
              <div>
                <div className="mtitle">{m.title}</div>
                <div className="msub">{m.subtitle}</div>
              </div>
              <div className="mprog">
                <div className="mbar"><i style={{ width: mp.pct + '%', background: ACCENT[m.color] }} /></div>
                {mp.done}/{mp.total}
              </div>
            </div>
            <div className="lessons">
              {m.lessons.map((l, idx) => {
                const pr = progress[l.id];
                const done = !!pr?.done;
                const best = pr?.best || 0;
                return (
                  <button key={l.id} className={`lcard ${done ? 'done' : ''} ${l.rehearsal ? 'rehcard' : ''}`}
                    style={{ '--accent': ACCENT[m.color] }} onClick={() => onOpen(l.id)}>
                    <div className="lnode" style={{ '--accent': ACCENT[m.color], '--p': best }}>
                      <span>{done ? '✓' : idx + 1}</span>
                    </div>
                    <div className="lbody">
                      <div className="lt">{l.title}</div>
                      <div className="lmeta">
                        <span className="stag">{l.mins}′</span>
                        {l.key && <span className="ktag">trọng tâm</span>}
                        {l.rehearsal && <span className="ktag">🎤 diễn tập</span>}
                        {l.slides?.length > 0 && <span className="stag">slide {l.slides.map((s) => '#' + s).join(' ')}</span>}
                        {done && <span className="stag" style={{ color: 'var(--green)' }}>{best}%</span>}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}
