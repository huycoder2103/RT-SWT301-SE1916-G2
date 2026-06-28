import { useMemo, useState } from 'react';
import { mdInline } from './md';

const H = (s) => ({ dangerouslySetInnerHTML: { __html: mdInline(s) } });
const KEYS = ['A', 'B', 'C', 'D', 'E'];
const GRADEABLE = new Set(['mcq', 'tf', 'cloze', 'order']);

export default function Quiz({ items, onComplete }) {
  const [i, setI] = useState(0);
  const [correct, setCorrect] = useState(0);
  const [answered, setAnswered] = useState(false);
  const item = items[i];
  const last = i === items.length - 1;
  const gradeable = items.filter((q) => GRADEABLE.has(q.t)).length || 1;

  function onResult(isCorrect) {
    setAnswered(true);
    if (isCorrect && GRADEABLE.has(item.t)) setCorrect((c) => c + 1);
  }
  function nextQ() {
    if (last) { onComplete(Math.round((correct / gradeable) * 100)); return; }
    setI(i + 1); setAnswered(false);
  }

  return (
    <div className="quiz">
      <div className="qhead">🧠 Kiểm tra nhanh <span className="qcount">{i + 1}/{items.length}</span></div>
      <div className="qcard" key={item.__k || i}>
        {item.t === 'mcq' && <MCQ item={item} answered={answered} onResult={onResult} />}
        {item.t === 'tf' && <TF item={item} answered={answered} onResult={onResult} />}
        {item.t === 'cloze' && <Cloze item={item} answered={answered} onResult={onResult} />}
        {item.t === 'flip' && <Flip item={item} answered={answered} onResult={() => onResult(true)} />}
        {item.t === 'order' && <Order item={item} answered={answered} onResult={onResult} />}
      </div>
      {answered && (
        <div className="lnav">
          <button className="btn primary" onClick={nextQ}>{last ? 'Hoàn thành bài ✓' : 'Câu tiếp →'}</button>
        </div>
      )}
    </div>
  );
}

function Feedback({ ok, text }) {
  if (text == null) return null;
  return <div className={`explain ${ok ? 'ok' : 'no'}`}><span className="eic">{ok ? '✓' : '✕'}</span><span {...H(text)} /></div>;
}

function MCQ({ item, answered, onResult }) {
  const [pick, setPick] = useState(null);
  const choose = (idx) => { if (answered) return; setPick(idx); onResult(idx === item.correct); };
  return (
    <>
      <div className="qq" {...H(item.q)} />
      <div className="opts">
        {item.options.map((o, idx) => {
          let cls = 'opt';
          if (answered) { if (idx === item.correct) cls += ' correct'; else if (idx === pick) cls += ' wrong'; }
          return (
            <button key={idx} className={cls} disabled={answered} onClick={() => choose(idx)}>
              <span className="ki">{KEYS[idx]}</span><span {...H(o)} />
            </button>
          );
        })}
      </div>
      {answered && <Feedback ok={pick === item.correct} text={item.explain} />}
    </>
  );
}

function TF({ item, answered, onResult }) {
  const [pick, setPick] = useState(null);
  const choose = (v) => { if (answered) return; setPick(v); onResult(v === item.answer); };
  const opt = (v, label) => {
    let cls = 'opt';
    if (answered) { if (v === item.answer) cls += ' correct'; else if (v === pick) cls += ' wrong'; }
    return <button className={cls} disabled={answered} onClick={() => choose(v)}><span className="ki">{v ? '✓' : '✕'}</span>{label}</button>;
  };
  return (
    <>
      <div className="qq" {...H(item.q)} />
      <div className="opts">{opt(true, 'Đúng')}{opt(false, 'Sai')}</div>
      {answered && <Feedback ok={pick === item.answer} text={item.explain} />}
    </>
  );
}

function Cloze({ item, answered, onResult }) {
  const [pick, setPick] = useState(null);
  const choose = (o) => { if (answered) return; setPick(o); onResult(o === item.answer); };
  return (
    <>
      <div className="qq cloze">
        <span {...H(item.before)} />
        <span className={`blank ${answered ? '' : 'empty'}`}>{answered ? item.answer : '? ? ?'}</span>
        <span {...H(item.after)} />
      </div>
      <div className="opts">
        {item.options.map((o, idx) => {
          let cls = 'opt';
          if (answered) { if (o === item.answer) cls += ' correct'; else if (o === pick) cls += ' wrong'; }
          return <button key={idx} className={cls} disabled={answered} onClick={() => choose(o)}><span className="ki">{KEYS[idx]}</span>{o}</button>;
        })}
      </div>
      {answered && <Feedback ok={pick === item.answer} text={item.explain || ('Đáp án: ' + item.answer)} />}
    </>
  );
}

function Flip({ item, answered, onResult }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <>
      <div className={`flip ${flipped ? 'flipped' : ''}`} onClick={() => { setFlipped(true); if (!answered) onResult(); }}>
        <div className="inner" style={{ minHeight: 150 }}>
          <div className="face front"><div className="flbl">Câu hỏi — bấm để lật</div><div className="ftext" {...H(item.front)} /><div className="hint">👆 nhớ câu trả lời trong đầu rồi lật</div></div>
          <div className="face back"><div className="flbl">Đáp án</div><div className="ftext" {...H(item.back)} /></div>
        </div>
      </div>
      {answered && <div className="explain ok"><span className="eic">★</span><span>Flashcard — không tính điểm, dùng để ghi nhớ.</span></div>}
    </>
  );
}

function Order({ item, answered, onResult }) {
  // correct order = item.items as given; shuffle for display
  const initial = useMemo(() => {
    const idx = item.items.map((_, k) => k);
    for (let k = idx.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [idx[k], idx[j]] = [idx[j], idx[k]]; }
    // avoid already-sorted
    if (idx.every((v, k) => v === k)) idx.reverse();
    return idx;
  }, [item]);
  const [ord, setOrd] = useState(initial);
  const move = (pos, dir) => {
    if (answered) return;
    const j = pos + dir; if (j < 0 || j >= ord.length) return;
    const n = [...ord]; [n[pos], n[j]] = [n[j], n[pos]]; setOrd(n);
  };
  const check = () => onResult(ord.every((v, k) => v === k));
  return (
    <>
      <div className="qq" {...H(item.prompt)} />
      <div className="order">
        {ord.map((orig, pos) => {
          let cls = 'oitem';
          if (answered) cls += orig === pos ? ' ok' : ' bad';
          return (
            <div className={cls} key={orig}>
              <span className="onum">{pos + 1}</span>
              <span {...H(item.items[orig])} />
              {!answered && <span className="oc">
                <button onClick={() => move(pos, -1)} disabled={pos === 0}>↑</button>
                <button onClick={() => move(pos, 1)} disabled={pos === ord.length - 1}>↓</button>
              </span>}
            </div>
          );
        })}
      </div>
      {!answered && <div className="lnav"><button className="btn ghost" onClick={check}>Kiểm tra thứ tự</button></div>}
      {answered && <Feedback ok={ord.every((v, k) => v === k)} text={ord.every((v, k) => v === k) ? 'Chuẩn thứ tự!' : 'Chưa đúng — xem thứ tự đúng đã tô màu.'} />}
    </>
  );
}
