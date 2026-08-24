#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 dist 收集页面生成 sitemap.xml（PERIFLOW）"""
import os

base = 'https://periflow.pages.dev'
pages = []
for root, dirs, files in os.walk('dist'):
    for f in files:
        if f == 'index.html':
            rel = os.path.relpath(os.path.join(root, f), 'dist').replace(os.sep, '/')
            url = base + '/' + rel[:-len('index.html')]
            pages.append(url)
pages = sorted(set(p for p in pages if '404' not in p))
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
    xml.append(f'  <url><loc>{p}</loc><lastmod>2026-08-24</lastmod></url>')
xml.append('</urlset>')
os.makedirs('public', exist_ok=True)
with open('public/sitemap.xml', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(xml))
print(f"sitemap generated: {len(pages)} pages")
for p in pages:
    print(p)
