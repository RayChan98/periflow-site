#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PERIFLOW 记录表：公司应用建字段 + 批量录入（已建表 R6yYbxbzga2pwyswPlQcXegln1b）"""
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

# 1. 建字段（公司应用）
fields = [
    ('页面 URL', 1), ('SEO TITLE', 1), ('SEO DESC', 1), ('核心词', 4), ('H1 Title', 1),
    ('页面类型', 3), ('收录情况', 3), ('状态', 3), ('上线日期', 5), ('字数', 2),
    ('配图数', 2), ('最后更新', 5), ('备注', 1),
]
for name, ftype in fields:
    r = api(f'/open-apis/bitable/v1/apps/{app}/tables/{tbl}/fields', {'field_name': name, 'type': ftype}, company=True)
    print(f'字段 {name}:', r.get('code'), r.get('msg', ''))
PYEOF