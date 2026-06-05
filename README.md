# xueba

“学霸”是一个面向深度学习、Obsidian TAG 流沉淀和已有知识升级的智能体技能。

## 适用场景

- 给一个网站、论文、PDF、视频转写或粘贴资料，让智能体系统学习。
- 给一个需要登录/授权的飞书、Notion、语雀、钉钉、私有 Wiki 或内部文档，让智能体通过合规授权路径读取后学习。
- 把资料整理成 Obsidian 可长期复用的学习资产。
- 生成 MOC、系统化笔记、原子概念卡、费曼自测、练习题和复习计划。
- 使用轻文件夹、重标签、强检索的 TAG 流知识管理方式。
- 扫描已有 Obsidian vault 或文件夹，找出可升级、可合并、可拆分、可补来源、可优化标签和双链的笔记。

## 两种模式

### 学习模式

用于处理新资料，默认生成一篇完整 Markdown，把一个主题讲清楚。只有用户明确要求概念卡、MOC 或完整知识资产包时，才拆成多文件。

### 升级模式

用于检查已有 Obsidian 知识库，输出知识库升级报告。默认只生成报告，不直接改旧笔记；只有用户明确要求“应用修改”时，才逐篇升级。

## 核心输出

学习模式默认生成一个单文件系统化专题笔记，并保存到 Obsidian 当前真实 vault 下的 `88-学习/`，而不是只放到 Codex 工作区、某台机器的个人目录或生成输出区。

```text
88-学习/[大学科]/[章节或知识要点]/[主题].md
```

写入前应先动态解析 Obsidian 环境：

- 先检查本机是否安装 Obsidian。
- 如果未检测到 Obsidian，提示用户到官方中文下载页安装：https://obsidian.md/zh/
- 再通过 Obsidian 本地配置、`.obsidian` 目录搜索或用户显式路径定位 vault。
- 不写死任何本机绝对 vault 路径。
- 不把 `obsidian://` 深链当作保存目标；保存目标必须是真实 vault 文件夹。
- 只有在已确认 Obsidian 安装且已解析出 vault 名称和文件相对路径后，才动态构造打开链接或使用系统打开器。

解析到 vault 后，统一使用 `88-学习/` 作为学习沉淀根目录：

```text
88-学习/
  AI/
    智能体/
      Agent 与 Agent Harness：核心架构.md
    skills/
      学霸技能设计与评估.md
  管理/
    OKR/
      OKR 与 KPI：目标管理机制.md
  产品/
    PRD/
      高质量 PRD 的结构化写法.md
```

如果 vault 中没有 `88-学习/`，创建它；如果已经存在，直接复用。目录保持简洁直接：`大学科` 放第一层，例如 `AI`、`产品`、`管理`、`技术`、`业务`；章节或知识要点放第二层，例如 `AI/智能体`、`AI/skills`、`AI/RAG`、`产品/PRD`。分类信心不足时，保存到 `88-学习/待分类/`，并用保守标签标记。

单文件内包含：

- 一句话系统本质
- 知识全景架构树 (Mental Map)
- 原子概念与双链网
- Why / What / How / Limits
- 应用边界、熔断条件和常见误区
- 和已有知识/工作的连接
- 费曼闭环与延伸思考
- 闭卷回忆题
- 迁移练习
- 复习计划
- 来源与质量验收

可选资产包模式才生成：

```text
学霸/[主题]/
  index.md
  overview.md
  notes.md
  concepts/
  questions/
  exercises/
  review-plan.md
  sources.md
  qa.md
```

升级模式默认生成：

```text
学霸/知识库升级报告/YYYY-MM-DD-知识库升级报告.md
```

## TAG 规范

Frontmatter 中使用受控嵌套标签，不带 `#`：

```yaml
tags:
  - status/seed
  - type/system-note
  - domain/ai/agent
  - source/web
  - access/public
  - confidence/medium
```

## 登录/授权资料处理

遇到飞书、Notion、语雀、钉钉、私有 Wiki、内部文档等需要登录的资料时，“学霸”不应直接放弃，也不能绕过权限。默认按以下顺序处理：

1. 先尝试公开 URL 读取，确认返回的是正文而不是登录页。
2. 如果有官方导出、API、MCP 或 CLI，并且用户已授权，优先导出 Markdown / PDF / DOCX / HTML。
3. 如果有可用的已登录浏览器工具，征得用户许可后只读取页面可见正文，不读取 cookies、localStorage、密码或 token。
4. 如果无法直接授权读取，请用户粘贴正文或提供导出文件。
5. 仍无法取得正文时，生成结构化失败说明，不伪造学习笔记。

访问方式用 `access/*` 标签标记：

```yaml
tags:
  - access/public
  - access/authenticated
  - access/exported
  - access/pasted
  - access/blocked
```

## 质量要求

- 双链只用于长期可复用概念。
- 关键论断必须有来源锚点。
- 原文观点、AI 转述、推理扩展需要区分。
- 练习题必须包含答案或评分标准。
- 复习计划必须有间隔和具体任务。
- 升级已有笔记时必须先报告后修改，避免污染知识库。
- 学习新资料时默认一篇 Markdown 讲清楚，不要过早拆成多个零散文件。
- 默认输出应像一篇完整的“系统化专题”，而不是多个卡片、摘录、问答的拼接。
- 正式学习笔记应进入 Obsidian vault 下的 `88-学习/` 并按内容智能分类；生成输出区只作为草稿、测试或失败报告区。

## 默认单文件模板

```markdown
---
title: "系统化专题：[主题]"
tags:
  - status/seed
  - type/system-note
  - domain/[domain]
  - source/[source-type]
  - access/[access-type]
  - confidence/[level]
source: "[source]"
created: "YYYY-MM-DD"
---

# 系统化专题：[[主题]]

> [!abstract] 一句话系统本质
> 不超过 100 字，一针见血说明该知识解决的核心问题、底层机制和适用价值。

## 1. 知识全景架构树 (Mental Map)

## 2. 原子概念与双链网 (Concepts)

## 3. 系统化内容详解

### 3.1 核心痛点与背景（Why）

### 3.2 体系与架构（What）

### 3.3 落地应用与 SOP（How）

### 3.4 应用边界、熔断条件与常见误区（Limits）

## 4. 和我已有知识/工作的连接

## 5. 费曼闭环与延伸思考

## 6. 闭卷回忆题

## 7. 迁移练习

## 8. 复习计划

## 9. 来源与可信度

## 10. 质量验收
```

## 测试提示

测试用例保存在 `evals/evals.json`。后续可按 `skill-creator` 流程运行评估。
