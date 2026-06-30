import { useEffect, useRef } from 'react';

export default function Slide({ slide, scale, frag, onOpen }) {
  const ref = useRef(null);

  useEffect(() => {
    const frags = ref.current?.querySelectorAll('.frag') || [];
    frags.forEach((f, i) => f.classList.toggle('in', i < frag));
  }, [frag, slide]);

  function handleClick(e) {
    const el = e.target.closest('[data-open]');
    if (!el) return;
    e.preventDefault();
    if (el.dataset.open === 'pdf') {
      onOpen({ type: 'pdf', arxiv: el.dataset.arxiv, page: parseInt(el.dataset.page || '1', 10), quote: el.dataset.quote || '' });
    } else if (el.dataset.open === 'md') {
      onOpen({ type: 'md', file: el.dataset.file });
    }
  }

  return (
    <section
      key={slide.id}
      className={`slide ${slide.cls} slide-anim`}
      style={{ '--scale': scale }}
      onClick={handleClick}
      ref={ref}
      dangerouslySetInnerHTML={{ __html: slide.body }}
    />
  );
}
