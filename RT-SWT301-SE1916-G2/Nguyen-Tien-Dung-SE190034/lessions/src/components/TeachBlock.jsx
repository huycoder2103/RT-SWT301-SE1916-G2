import { mdInline } from './md';

const H = (s) => ({ dangerouslySetInnerHTML: { __html: mdInline(s) } });

export default function TeachBlock({ b }) {
  switch (b.t) {
    case 'p':
      return <p className="tb p" {...H(b.md)} />;
    case 'analogy':
      return (
        <div className="tb analogy">
          <div className="at">{b.title || 'Hình dung như…'}</div>
          <div {...H(b.md)} />
        </div>
      );
    case 'warn':
      return (
        <div className="tb warn">
          <div className="at">{b.title || 'Lưu ý quan trọng'}</div>
          <div {...H(b.md)} />
        </div>
      );
    case 'why':
      return (
        <div className="tb why">
          <div className="ic" />
          <div {...H(b.md)} />
        </div>
      );
    case 'say':
      return (
        <div className="tb say">
          <div className="slbl">Lên sân khấu nói gì</div>
          <div className="stext" {...H(b.md)} />
        </div>
      );
    case 'terms':
      return (
        <div className="tb terms">
          {b.items.map(([k, v], i) => (
            <div className="trow" key={i}><div className="tk">{k}</div><div className="tv" {...H(v)} /></div>
          ))}
        </div>
      );
    case 'numbers':
      return (
        <div className="tb numbers">
          {b.items.map((n, i) => (
            <div className="nc" key={i}><div className="nv">{n.v}</div><div className="nl">{n.l}</div></div>
          ))}
        </div>
      );
    case 'slide':
      return <div className="tb slide">Slide trong deck: {b.n.map((x) => `#${x}`).join(', ')}</div>;
    default:
      return null;
  }
}
