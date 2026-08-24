# PERIFLOW — Peristaltic Pump B2B 外贸站（T-53 蠕动泵）

> 品牌：PERIFLOW（Peristaltic + Flow）
> 域名：https://periflow.pages.dev（待注册正式域名，走 CF Registrar）
> 技术栈：Astro 7 + Tailwind v4（fullcolorcam 原生模式，非 molditquick）
> 状态：2026-08-25 上线 ✅ **29 页全 200**（26 基础 + 3 内容增量）
> Git 归属：**个人兼职（RayChan98 / cj226144）**，禁 grohoprecision-hub
> Git：https://github.com/RayChan98/periflow-site
> 记录表：https://kcnkn5gq5sh6.feishu.cn/base/R6yYbxbzga2pwyswPlQcXegln1b（29 条）

## 状态（2026-08-24 夜间预跑+建站首日 → 08-25 内容增量）

- [x] 品牌定名 PERIFLOW（Peristaltic + Flow）
- [x] 竞对调研（预跑 01 清单 31 域 / 02 内容策略 / 03 内容提炼）
- [x] 骨架：26 页全构建 + 0 死链 + 27/27 全 200（含 404）
- [x] SEO 检查：title/desc/canonical/h1/og/jsonld 全过（404 页除外，设计使然）
- [x] 部署：https://periflow.pages.dev（个人号 CF，32 文件 + Functions）
- [x] Git 推送：RayChan98/periflow-site（远端 HEAD 验证）
- [x] 飞书记录表：26 条 → **29 条**（+3 内容增量，全量重建）
- [x] 内容增量（广播③）：+3 篇博客 = 全站 29 页（head-guide 1880 词 / chemical-dosing 1784 词 / top-10-manufacturers 1904 词，3 体裁覆盖）
- [x] 博客列表 6 卡片 + sitemap 29 条
- [ ] 表单 env 配置（ZOHO_CLIENT_SECRET/REFRESH_TOKEN 被 CF 掩码 → 需主人从 fullcolorcam Dashboard 复制到 periflow 项目）——当前 fail-closed 不丢单
- [ ] 色板/LOGO（后置，随时可换）
- [ ] 正式域名注册（periflow.com 类，CF Registrar）

## 页面地图（29 页）

| 类 | 页面 |
|:--|:--|
| 首页 | / |
| 产品 6 | /products/ + pump-heads / tubing / benchtop-pumps / dosing-pumps / oem-pumps |
| 应用 5 | /applications/ + laboratory / chemical-dosing / food-beverage / biopharma |
| 服务 4 | /services/ + oem-odm / wholesale-distribution / technical-support |
| 博客 6 | /blog/ + ptfe-vs-silicone-tubing / how-long-does-pump-tubing-last / peristaltic-vs-diaphragm-pump / peristaltic-pump-head-guide / peristaltic-pump-for-chemical-dosing / top-10-peristaltic-pump-manufacturers |
| 基础 7 | about / contact / faq / privacy / terms / thank-you / 404 |

## 关键决策

- 色板/LOGO 后置（总控铁律：先搭内容，随时可换）
- 表单 Zoho（全站统一口径），fail-closed 部署
- 内容对标 jihpump 打法（tube replacement 词 SERP 前 3 实证），博客是 SEO 引擎
- 意图内容工厂：指南/应用/listicle 三体裁覆盖核心词

## 坑（复盘沉淀）

- 复制 fullcolorcam 站需清 node_modules 重装（增量安装漏 yargs-parser）
- node 22 需 npm approve-scripts（esbuild）
- CF 掩码 secret 无法读取 → 表单 env 只能 Dashboard 手动配
- 飞书 bitable 建表/建字段/写记录必须用公司应用 token（个人应用 403）
- 日期字段要毫秒时间戳（1254064 DatetimeFieldConvFail）
- 记录表默认自带 11 条空记录需 batch_delete
- 飞书 batch_create 端点偶发 RecordIdNotFound → 用单条 records 循环写入（29 条实测可靠）
- GitHub 网络间歇不通（Recv failure/Empty reply）→ 本地 commit 不丢，网络恢复再推；远端被其他会话更新时需 pull --rebase 解决冲突

## 部署命令

```bash
export HTTPS_PROXY=http://127.0.0.1:7897
export CLOUDFLARE_API_TOKEN=<CF_PERSONAL_TOKEN>
export CLOUDFLARE_ACCOUNT_ID=<CF_PERSONAL_ACCOUNT_ID>
npx wrangler pages deploy dist --project-name=periflow
```
