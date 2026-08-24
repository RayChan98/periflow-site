#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PERIFLOW 上线前 on-page SEO 检查"""
import re, os

issues = []
pages = []
for root, dirs, files in os.walk('dist'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            html = open(p, encoding='utf-8', errors='replace').read()
            rel = os.path.relpath(p, 'dist').replace(os.sep, '/')
            pages.append(rel)
            t = re.search(r'<title>(.*?)</title>', html, re.S)
            if not t or len(t.group(1).strip()) < 10:
                issues.append('[NO-TITLE] ' + rel)
            d = re.search(r'<meta name="description" content="([^"]*)"', html)
            if not d or len(d.group(1)) < 50:
                issues.append('[NO-DESC] ' + rel)
            c = re.search(r'<link rel="canonical" href="([^"]*)"', html)
            if not c:
                issues.append('[NO-CANONICAL] ' + rel)
            elif 'periflow.pages.dev' not in c.group(1):
                issues.append('[BAD-CANONICAL] ' + rel + ': ' + c.group(1))
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
            if not h1:
                issues.append('[NO-H1] ' + rel)
            og = re.search(r'<meta property="og:title"', html)
            if not og:
                issues.append('[NO-OG] ' + rel)
            j = re.search(r'application/ld\+json', html)
            if not j:
                issues.append('[NO-JSONLD] ' + rel)
            for bad in ['FULLCOLORCAM', 'fullcolorcam', 'CCTV', 'night vision', 'surveillance']:
                if bad.lower() in html.lower():
                    issues.append('[RESIDUAL:' + bad + '] ' + rel)
                    break

print('页面总数:', len(pages))
print('问题数:', len(issues))
for i in issues:
    print(' ', i)
