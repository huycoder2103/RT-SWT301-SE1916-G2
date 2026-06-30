import { allLessons, totalLessons } from './course';

const KEY = 'lessions-progress-v1';

export function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
}
export function save(p) {
  try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
}
// record a lesson result: keep the BEST score (0..100)
export function record(p, lessonId, score) {
  const prev = p[lessonId]?.best ?? -1;
  const next = { ...p, [lessonId]: { done: true, best: Math.max(prev, Math.round(score)) } };
  save(next);
  return next;
}

export function xp(p) { return allLessons.reduce((s, l) => s + (p[l.id]?.best || 0), 0); }
export function doneCount(p) { return allLessons.filter((l) => p[l.id]?.done).length; }
export function readiness(p) {
  const sum = allLessons.reduce((s, l) => s + (p[l.id]?.best || 0), 0);
  return Math.round((sum / (totalLessons * 100)) * 100);
}
export function moduleProgress(p, lessons) {
  const done = lessons.filter((l) => p[l.id]?.done).length;
  return { done, total: lessons.length, pct: Math.round((done / lessons.length) * 100) };
}
// recommended next lesson id (first not-done in course order)
export function nextLesson(p) {
  const n = allLessons.find((l) => !p[l.id]?.done);
  return (n || allLessons[0]).id;
}

// mock-defense best score (kept separate from lesson progress)
export function recordMock(p, score) {
  const next = { ...p, __mock: Math.max(p.__mock || 0, Math.round(score)) };
  save(next);
  return next;
}
export function mockBest(p) { return p.__mock || 0; }
