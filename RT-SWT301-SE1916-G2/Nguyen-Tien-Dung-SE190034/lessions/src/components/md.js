// tiny inline markdown -> safe HTML (author-controlled content only)
// supports **bold**, *italic*, `code`
export function mdInline(s = '') {
  const esc = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return esc
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
}
