#!/usr/bin/env node
// 行业页/品类页 v2 静态验收（fullcolorcam 系 Astro 站通用，retail-security v2 首例实测）
// usage: node verify-industry-page.mjs <page.astro> --kws "kw1|kw2|kw3"
// checks: frontmatter JS 语法 / 关键词精确子串 / 裸 & / desc<=250 / <p> 句长<=25 词 / em-dash 计数(仅报告)
// 注意：frontmatter JS 字符串里的裸 & 合法（插值转义），裸 & 扫描会把 line 6 这类也报出来——人工核对位置即可，
//       真问题是 JSX 静态文本（<Layout title=...>、chapters 内文本）里的裸 &。
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--'));
const kwArg = args[args.indexOf('--kws') + 1];
const kws = kwArg ? kwArg.split('|').map((s) => s.trim()).filter(Boolean) : [];
const src = readFileSync(file, 'utf8');
let fail = 0;
const bad = (msg) => { fail++; console.log('FAIL: ' + msg); };

const m = src.match(/^---\r?\n([\s\S]*?)\r?\n---/);
if (!m) { bad('no frontmatter'); process.exit(1); }
try { new Function(m[1].replace(/import[^;]*;/g, '')); console.log('OK: frontmatter JS syntax'); }
catch (e) { bad('frontmatter syntax: ' + e.message); }

for (const k of kws) {
  const hit = src.includes(k);
  if (!hit) bad('keyword MISS: ' + k); else console.log('HIT  ' + k);
}

const bare = src.match(/&(?!(amp;|nbsp;|lt;|gt;|quot;|#\d+;))/g) || [];
if (bare.length) bad('bare & x' + bare.length + ' -> ' + JSON.stringify(bare));
else console.log('OK: no bare &');

const d = (src.match(/desc: '([^']*)'/) || [])[1] || '';
if (d.length > 250) bad('desc ' + d.length + ' chars (>250)'); else console.log('OK: desc ' + d.length + ' chars');

const ps = [...src.matchAll(/<p[^>]*>([\s\S]*?)<\/p>/g)];
let long = 0;
for (const pm of ps) {
  const text = pm[1].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').trim();
  for (const s of text.split(/(?<=[.!?])\s+/)) {
    const w = s.split(/\s+/).filter(Boolean).length;
    if (w > 25) { long++; console.log('LONG(' + w + 'w): ' + s.slice(0, 100) + '...'); }
  }
}
if (long) bad(long + ' long <p> sentences (>25w)'); else console.log('OK: <p> sentences <=25 words');

const em = (src.match(/\u2014/g) || []).length;
console.log('em-dash count: ' + em + ' (report only, target 0-5)');

console.log(fail === 0 ? 'ALL GREEN' : fail + ' FAILURES');
process.exit(fail === 0 ? 0 : 1);
