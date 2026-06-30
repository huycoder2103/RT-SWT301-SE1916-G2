import { Fragment } from 'react';
import { slides } from '../data';

export default function Overview({ idx, onGoto, onClose }) {
  return (
    <div className="overlay" onClick={onClose}>
      <div className="ov-grid" onClick={(e) => e.stopPropagation()}>
        {slides.map((s, i) => (
          <Fragment key={s.id}>
            {/divider/.test(s.cls) && <div className="ov-h">{s.title}</div>}
            <div className={`ov ${i === idx ? 'current' : ''}`} onClick={() => { onGoto(i); onClose(); }}>
              <div className="ovn">{String(i + 1).padStart(2, '0')}</div>
              <div className="ovt">{s.title}</div>
              <div className="ovk">{s.cls.replace(/\s*(active|enter)\s*/g, '').trim() || 'slide'}</div>
            </div>
          </Fragment>
        ))}
      </div>
    </div>
  );
}
