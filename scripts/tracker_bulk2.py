#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PERIFLOW 记录表批量录入（公司应用，26 页）"""
import json, os, re, urllib.request

ENV = r'C:\Users\admin\AppData\Local\hermes\.env'
def env(k):
    m = re.search(rf'^{re.escape(k)}=(.*)$', open(ENV, encoding='utf-8', errors='replace').read(), re.M)
    return m.group(1).strip() if m else ''

def api(path, data=None, company=True):
    app_id = env('FEISHU_COMPANY_APP_ID') if company else env('FEISHU_APP_ID')
    app_sec = env('FEISHU_COMPANY_APP_SECRET') if company else env('FEISHU_APP_SECRET')
    body = json.dumps({'app_id': app_id, 'app_secret': app_sec}).encode()
    req = urllib.request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=body, headers={'Content-Type': 'application/json'})
    tok = json.loads(urllib.request.urlopen(req, timeout=20).read())['tenant_access_token']
    req = urllib.request.Request('https://open.feishu.cn' + path, headers={'Authorization': 'Bearer ' + tok})
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header('Content-Type', 'application/json')
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        return {'error': str(e)}

app = 'R6yYbxbzga2pwyswPlQcXegln1b'
tbl = 'tblugts5WOg5DTOr'

# dist 提取页面
pages = []
for root, dirs, files in os.walk('dist'):
    for f in files:
        if f == 'index.html':
            p = os.path.join(root, f)
            html = open(p, encoding='utf-8', errors='replace').read()
            rel = os.path.relpath(p, 'dist').replace(os.sep, '/')
            url = '/' + rel.replace('/index.html', '') if rel != 'index.html' else '/'
            title = re.search(r'<title>(.*?)</title>', html, re.S)
            desc = re.search(r'<meta name="description" content="([^"]*)"', html)
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
            t = title.group(1).strip() if title else ''
            d = desc.group(1) if desc else ''
            h = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
            segs = url.strip('/').split('/')
            if url == '/': ptype = '首页'
            elif url in ('/about', '/contact', '/faq', '/privacy', '/terms', '/thank-you'): ptype = '普通内页'
            elif len(segs) == 1: ptype = '分类页'
            elif len(segs) == 2 and segs[0] == 'blog': ptype = '博客文章'
            else: ptype = '详情页'
            pages.append({'页面 URL': url, 'SEO TITLE': t, 'SEO DESC': d, '核心词': ['待定'], 'H1 Title': h, '页面类型': ptype, '收录情况': '未收录', '状态': '已上线', '上线日期': 1787529600000, '字数': 0, '配图数': 0, '最后更新': 1787529600000, '备注': 'PERIFLOW 上线首日'})

# 批量录入（每批 50）
total_ok = 0
for i in range(0, len(pages), 50):
    batch = pages[i:i+50]
    r = api(f'/open-apis/bitable/v1/apps/{app}/tables/{tbl}/records/batch_create', {'records': [{'fields': x} for x in batch]}, company=True)
    n = len(r.get('data', {}).get('records', [])) if r.get('code') == 0 else 0
    total_ok += n
    print(f'批次 {i//50+1}: code={r.get("code")} 写入={n} {r.get("msg", "")}')
print('TOTAL 写入:', total_ok, '/', len(pages))
print('URL:', f'https://kcnkn5gq5sh6.feishu.cn/base/{app}')
