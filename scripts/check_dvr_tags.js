const fs = require('fs');
const src = fs.readFileSync('src/pages/products/dvr.astro', 'utf8');
let bad = 0;
for (const t of ['div', 'section', 'table', 'thead', 'tbody', 'tr', 'ul', 'li', 'p', 'h2', 'h3', 'span', 'a', 'nav']) {
  const openRe = new RegExp('<' + t + '(\\s|>)', 'g');
  const closeRe = new RegExp('</' + t + '>', 'g');
  const open = (src.match(openRe) || []).length;
  const close = (src.match(closeRe) || []).length;
  if (open !== close) { bad++; console.log(t, 'open', open, 'close', close, 'MISMATCH'); }
}
// self-closing check on CategoryPageTemplate
const cpt = (src.match(/<CategoryPageTemplate[^>]*\/>/) || []).length;
const cptOpen = (src.match(/<CategoryPageTemplate(?:\s|>)/g) || []).length;
console.log('CategoryPageTemplate self-closed:', cpt, '| open tags:', cptOpen);
console.log(bad === 0 ? 'ALL TAGS BALANCED' : bad + ' tag types mismatched');
