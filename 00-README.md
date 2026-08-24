# PERIFLOW — Peristaltic Pump B2B 外贸站（T-53 蠕动泵）

> 品牌：PERIFLOW（Peristaltic + Flow）
> 域名：periflow.pages.dev（待注册正式域名，走 CF Registrar）
> 技术栈：Astro 7 + Tailwind v4（fullcolorcam 原生模式，非 molditquick）
> 状态：2026-08-24 夜间预跑 → 放权建站启动
> Git 归属：**个人兼职（RayChan98 / cj226144）**，禁 grohoprecision-hub

## 定位（来自 M1 选品报告 01-选品报告-蠕动泵-M1.md）

- 品类：Peristaltic Pump 蠕动泵品类站
- 旗舰：泵头（Pump Heads）+ 泵管（Tubing）耗材组合
- 次旗舰：实验室台式泵（Benchtop）/ 化学计量泵（Dosing）
- 切入逻辑：泵管 3-6 月必换=品类级复购；保定产业带 OEM 现货；竞对内容空白

## 页面地图（25+ 页）

| 区 | 页面 | 状态 |
|:--|:--|:--|
| 基础 | 首页 / about / contact / faq / privacy / terms / thank-you / 404 | ✅ |
| 产品 | products/ 总览 + pump-heads / tubing / benchtop-pumps / dosing-pumps / oem-pumps | ⏳ delegate 中 |
| 应用 | applications/ 总览 + laboratory / chemical-dosing / food-beverage / biopharma | ⏳ delegate 中 |
| 服务 | services/ 总览 + oem-odm / wholesale-distribution / technical-support | ⏳ delegate 中 |
| 博客 | blog/ 总览 + ptfe-vs-silicone / tubing-life / peristaltic-vs-diaphragm | ⏳ delegate 中 |

## 竞对弹药（夜间预跑/ 目录）

- 01-竞对主域名清单.md（31 域分类）
- 02-竞对内容策略分析.md（crpump/jihpump/prefluid 深挖）
- 03-页面内容提炼.md（3 类页面骨架 + 素材）
- 04-范本文-PTFE-vs-Silicone.md（自审通过范本）
- 05-交付汇总.md

## 部署

- CF Pages 个人号（cj226144）→ periflow.pages.dev
- 表单：functions/api/contact.js → Zoho OAuth2（凭证走 CF env，全站统一口径）
- 上线前：on-page SEO + technical SEO 大检查

## 待办

- [ ] delegate 页面组完成后全量构建验证
- [ ] 死链检查（qc_crawler 或 curl 全站 href）
- [ ] CF Pages 部署 + 表单 env 配置 + 实测
- [ ] 飞书网站记录表建表录入
- [ ] 正式域名注册（CF Registrar，主人操作）
- [ ] 内容批量（A-E 五批：对比文/指南/选型/维护/FAQ）
