import { useEffect, useState } from 'react';
import TeachBlock from './TeachBlock.jsx';
import Quiz from './Quiz.jsx';

export default function Lesson({ lesson, moduleTitle, onComplete, onNext, onHome, onStartRehearsal, hasNext }) {
  const [phase, setPhase] = useState('learn'); // learn | quiz | done
  const [score, setScore] = useState(100);
  useEffect(() => { setPhase('learn'); window.scrollTo(0, 0); }, [lesson.id]);

  const finish = (s) => { setScore(s); setPhase('done'); onComplete(s); };

  return (
    <div className="lesson">
      <div className="lcrumb"><b>{moduleTitle}</b> <span>·</span> <span>{lesson.mins} phút</span>{lesson.key && <span className="ktag" style={{ padding: '1px 8px', borderRadius: 100 }}>trọng tâm</span>}</div>
      <h2 className="lh">{lesson.title}</h2>

      {phase === 'learn' && (
        <>
          <div className="lprog"><i style={{ width: '40%' }} /></div>
          {lesson.teach.map((b, i) => <TeachBlock key={i} b={b} />)}
          <div className="lnav">
            <button className="btn ghost" onClick={onHome}>← Bản đồ</button>
            {lesson.rehearsal
              ? <button className="btn primary" onClick={() => { onComplete(100); onStartRehearsal(); }}>Bắt đầu diễn tập 🎤</button>
              : lesson.quiz.length
                ? <button className="btn primary" onClick={() => { setPhase('quiz'); window.scrollTo(0, 0); }}>Kiểm tra để hoàn thành →</button>
                : <button className="btn primary" onClick={() => finish(100)}>Hoàn thành ✓</button>}
          </div>
        </>
      )}

      {phase === 'quiz' && (
        <>
          <div className="lprog"><i style={{ width: '70%' }} /></div>
          <Quiz key={lesson.id} items={lesson.quiz} onComplete={finish} />
        </>
      )}

      {phase === 'done' && (
        <div className="done-card">
          <div className="big">{score >= 80 ? '🎉' : score >= 50 ? '👍' : '📚'}</div>
          <h3>{score >= 80 ? 'Xuất sắc!' : score >= 50 ? 'Tốt — đã nắm ý chính' : 'Hoàn thành — ôn lại sẽ chắc hơn'}</h3>
          <div className="score">Điểm bài này: {score}/100 · đã lưu tiến độ</div>
          <div className="lnav" style={{ justifyContent: 'center' }}>
            <button className="btn ghost" onClick={onHome}>Về bản đồ</button>
            {hasNext && <button className="btn primary" onClick={onNext}>Bài tiếp theo →</button>}
          </div>
        </div>
      )}
    </div>
  );
}
