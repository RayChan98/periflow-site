#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PERIFLOW 飞书网站记录表：建表 + 建字段 + 批量录入（seo-page-tracker 模式）"""
import json, os, re, time, urllib.request, urllib.parse

ENV = r'C:\Users\admin\AppData\Local\hermes\.env'
def env(k):
    m = re.search(rf'^{re.escape(k)}=(.*)$', open(ENV, encoding='utf-8', errors='replace').read(), re.M)
    return m.group(1).strip() if m else ''

def api(path, data=None, method='GET', company=False):
    app_id = env('FEISHU_COMPANY_APP_ID') if company else env('FEISHU_APP_ID')
    app_sec = env('FEISHU_COMPANY_APP_SECRET') if company else env('FEISHU_APP_SECRET')
    # 刷 token
    body = json.dumps({'app_id': app_id, 'app_secret': app_sec}).encode()
    req = urllib.request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=body, headers={'Content-Type': 'application/json'})
    tok = json.loads(urllib.request.urlopen(req, timeout=20).read())['tenant_access_token']
    req = urllib.request.Request('https://open.feishu.cn' + path, headers={'Authorization': 'Bearer ' + tok})
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header('Content-Type', 'application/json')
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return r
    except Exception as e:
        return {'error': str(e)}

# 1. 建表（公司应用）——已建则复用
app = env('PERIFLOW_BITABLE_APP') or ''
tbl = env('PERIFLOW_BITABLE_TBL') or ''
if not app:
    r = api('/open-apis/bitable/v1/apps', {'name': 'PERIFLOW 网站记录表'}, 'POST', company=True)
    print('建表:', r.get('code'))
    app = r.get('data', {}).get('app', {}).get('app_token')
    if not app:
        print('建表失败:', r); raise SystemExit
    tbl = r['data']['app'].get('default_table_id')
    if not tbl:
        r2 = api(f'/open-apis/bitable/v1/apps/{app}/tables')
        tbl = r2['data']['items'][0]['table_id']
else:
    # 已有表：确认 table
    r2 = api(f'/open-apis/bitable/v1/apps/{app}/tables')
    if r2.get('code') == 0 and r2['data']['items']:
        tbl = r2['data']['items'][0]['table_id']
print('app:', app, 'table:', tbl)
open(ENV, 'a', encoding='utf-8').write(f'\nPERIFLOW_BITABLE_APP={app}\nPERIFLOW_BITABLE_TBL={tbl}\n')

# 2. 建字段
fields = [
    ('页面 URL', 1), ('SEO TITLE', 1), ('SEO DESC', 1), ('核心词', 4), ('H1 Title', 1),
    ('页面类型', 3), ('收录情况', 3), ('状态', 3), ('上线日期', 5), ('字数', 2),
    ('配图数', 2), ('最后更新', 5), ('备注', 1),
]
for name, ftype in fields:
    api(f'/open-apis/bitable/v1/apps/{app}/tables/{tbl}/fields', {'field_name': name, 'type': ftype}, 'POST')
print('字段创建完成')

# 3. dist 提取页面
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
            # 页面类型
            segs = url.strip('/').split('/')
            if url == '/': ptype = '首页'
            elif url in ('/about', '/contact', '/faq', '/privacy', '/terms', '/thank-you'): ptype = '普通内页'
            elif len(segs) == 1: ptype = '分类页'
            elif len(segs) == 2 and segs[0] == 'blog': ptype = '博客文章'
            else: ptype = '详情页'
            pages.append({'页面 URL': url, 'SEO TITLE': t, 'SEO DESC': d, '核心词': ['待定'], 'H1 Title': h, '页面类型': ptype, '收录情况': '未收录', '状态': '已上线', '上线日期': '2026-08-24', '字数': 0, '配图数': 0, '最后更新': '2026-08-24', '备注': 'PERIFLOW 上线首日'})

# 4. 批量录入
for i in range(0, len(pages), 50):
    batch = pages[i:i+50]
    r = api(f'/open-apis/bitable/v1/apps/{app}/tables/{tbl}/records/batch_create', {'records': [{'fields': x} for x in batch]}, 'POST')
    print(f'录入 {len(batch)} 条:', r.get('code'))
print('TOTAL:', len(pages))
print('URL:', f'https://kcnkn5gq5sh6.feishu.cn/base/{app}')
