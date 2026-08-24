// 品类页 v2 静态验收脚本（fullcolorcam-site-ops 附带）
// Usage (from site root, e.g. F:/.../fullcolorcam-site):
//   node scripts/verify-category-page.mjs src/pages/products/<slug>.astro --kws "what is ahd|ahd dvr 8 camera kit|dvr dvr"
// Checks: frontmatter JS syntax, bare &, keyword exact substrings, tag balance, body word count, sentences >25 words.
// Note: .mjs required — site package.json is "type": "module"; .js would fail with "require is not defined".
import fs from 'node:fs';

const args = process.argv.slice(2);
const file = args.find((a) => a.endsWith('.astro'));
if (!file || !fs.existsSync(file)) {
  console.error('Usage: node verify-category-page.mjs src/pages/products/<slug>.astro --kws "kw1|kw2|kw3"');
  process.exit(1);
}
const kwsIdx = args.indexOf('--kws');
const kws = kwsIdx >= 0 ? args[kwsIdx + 1].split('|') : [];
const src = fs.readFileSync(file, 'utf8');
let fail = 0;

// 1. frontmatter JS syntax (CRLF-tolerant: \r?\n)
const fmMatch = src.match(/^---\r?\n([\s\S]*?)\r?\n---/);
if (!fmMatch) { console.log('FAIL: frontmatter not found'); fail++; }
else {
  try { new Function(fmMatch[1].replace(/^import.*$/gm, '')); console.log('frontmatter JS: OK'); }
  catch (e) { console.log('FAIL: frontmatter JS:', e.message); fail++; }
}

// 2. bare & (HTML text nodes must use &amp;). & inside JS strings or quoted
// JSX attributes is allowed (e.g. title: 'A & B' renders escaped) — strip
// quoted spans first so only visible HTML text is checked.
const noQuoted = src.replace(/'[^'\n]*'/g, '').replace(/"[^"\n]*"/g, '');
const bareAmp = noQuoted.match(/&(?!(amp;|nbsp;|lt;|gt;|quot;|#\d+;))/g);
if (bareAmp) { console.log('FAIL: bare & x' + bareAmp.length, bareAmp.slice(0, 8)); fail++; }
else console.log('bare &: OK (0)');

// 3. main keywords as exact substrings
for (const k of kws) {
  if (!src.toLowerCase().includes(k.toLowerCase())) { console.log('MISSING kw:', k); fail++; }
}
console.log('keywords: ' + (kws.length ? (kws.length - (kws.filter((k) => !src.toLowerCase().includes(k.toLowerCase())).length)) + '/' + kws.length : 'n/a (pass --kws)'));

// 4. tag balance
let tagBad = 0;
for (const t of ['div', 'section', 'table', 'thead', 'tbody', 'tr', 'ul', 'li', 'p', 'h2', 'h3', 'span', 'a', 'nav']) {
  const open = (src.match(new RegExp('<' + t + '(\\s|>)', 'g')) || []).length;
  const close = (src.match(new RegExp('</' + t + '>', 'g')) || []).length;
  if (open !== close) { tagBad++; console.log('TAG MISMATCH:', t, 'open', open, 'close', close); }
}
if (tagBad) fail++;
else console.log('tags: OK (balanced)');

// 5. body word count (category page target ~500; blog needs 3000+)
const html = src.replace(/^---[\s\S]*?---/, '');
const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
const words = text.split(' ').filter(Boolean).length;
console.log('body words: ~' + words);

// 6. sentences >25 words (table cells / colon lists will false-positive — structural, not a real issue)
const sents = text.split(/(?<=[.!?])\s+/);
let long = 0;
for (const s of sents) {
  const w = s.replace(/[^a-zA-Z0-9'"\/+%\-]/g, ' ').trim().split(/\s+/).filter(Boolean).length;
  if (w > 25) { long++; if (long <= 5) console.log('NOTE long(>' + w + '):', s.slice(0, 120)); }
}
if (long) console.log('sentences >25 words: ' + long + ' (check: usually table/list false positives)');

console.log(fail === 0 ? 'PASS' : 'FAIL: ' + fail + ' problem(s)');
process.exit(fail === 0 ? 0 : 1);
