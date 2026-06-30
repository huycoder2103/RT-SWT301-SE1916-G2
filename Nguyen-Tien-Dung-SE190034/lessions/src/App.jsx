import { useState } from 'react';
import { allLessons } from './data/course';
import * as P from './data/progress';
import Home from './components/Home.jsx';
import Lesson from './components/Lesson.jsx';
import Rehearsal from './components/Rehearsal.jsx';
import MockDefense from './components/MockDefense.jsx';
import CheatSheet from './components/CheatSheet.jsx';

export default function App() {
  const [view, setView] = useState({ type: 'home' });
  const [progress, setProgress] = useState(() => P.load());
  const [theme, setTheme] = useState(() => document.documentElement.getAttribute('data-theme') || 'light');
  const [toast, setToast] = useState(null);

  const idxOf = (id) => allLessons.findIndex((l) => l.id === id);
  const nav = (v) => { setView(v); window.scrollTo(0, 0); };
  const openLesson = (id) => nav({ type: 'lesson', lessonId: id });
  const goHome = () => nav({ type: 'home' });
  const flash = (msg) => { setToast(msg); setTimeout(() => setToast(null), 1800); };

  const complete = (id, score) => { setProgress((p) => P.record(p, id, score)); flash(`+${Math.round(50 + score / 2)} XP · đã lưu`); };
  const goNext = (id) => { const n = allLessons[idxOf(id) + 1]; if (n) openLesson(n.id); else goHome(); };
  const finishMock = (score) => { setProgress((p) => P.recordMock(p, score)); flash(score >= 85 ? '🏆 Sẵn sàng bảo vệ!' : `Thi thử: ${score}%`); };

  const toggleTheme = () => setTheme((t) => {
    const nt = t === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nt);
    try { localStorage.setItem('lessions-theme', nt); } catch (e) {}
    return nt;
  });

  const lesson = view.type === 'lesson' ? allLessons.find((l) => l.id === view.lessonId) : null;

  return (
    <div className="shell">
      <header className="bar">
        <div className="logo" onClick={goHome}><span className="spark">🎓</span> Zero → Hero</div>
        <div className="grow" />
        <button className="pillbtn mock" onClick={() => nav({ type: 'mock' })} title="Thi thử để biết đã sẵn sàng chưa">🎯 Bảo vệ thử{P.mockBest(progress) ? ` ${P.mockBest(progress)}%` : ''}</button>
        <button className="pillbtn" onClick={() => nav({ type: 'cheatsheet' })} title="Phao thi in được">🧾 Phao</button>
        <span className="streak" title="Số bài đã hoàn thành">🔥 {P.doneCount(progress)}/{allLessons.length}</span>
        <span className="xp" title="Điểm kinh nghiệm">⚡ {P.xp(progress)}</span>
        <button className="icbtn" onClick={toggleTheme} title="Sáng/Tối">◐</button>
      </header>

      <main className="wrap">
        {view.type === 'home' && <Home progress={progress} onOpen={openLesson} onMock={() => nav({ type: 'mock' })} onCheat={() => nav({ type: 'cheatsheet' })} mock={P.mockBest(progress)} />}
        {view.type === 'lesson' && lesson && (
          <Lesson lesson={lesson} moduleTitle={lesson.moduleTitle} hasNext={idxOf(lesson.id) < allLessons.length - 1}
            onComplete={(s) => complete(lesson.id, s)} onNext={() => goNext(lesson.id)} onHome={goHome}
            onStartRehearsal={() => nav({ type: 'rehearsal' })} />
        )}
        {view.type === 'rehearsal' && <Rehearsal onHome={goHome} />}
        {view.type === 'mock' && <MockDefense best={P.mockBest(progress)} onFinish={finishMock} onHome={goHome} onRehearsal={() => nav({ type: 'rehearsal' })} onCheatSheet={() => nav({ type: 'cheatsheet' })} />}
        {view.type === 'cheatsheet' && <CheatSheet onHome={goHome} />}
      </main>

      {toast && <div className="toast no-print">{toast}</div>}
    </div>
  );
}
