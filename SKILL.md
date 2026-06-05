---
name: xueba
description: Use this skill whenever the user wants to deeply study, digest, restructure, and save learning materials into an Obsidian vault using a tag-first knowledge system, or wants to inspect an existing Obsidian vault to find notes, concepts, tags, links, or knowledge areas that can be upgraded. Trigger for requests like “帮我学习这个资料/网站/论文/视频”, “系统学习后整理到 Obsidian”, “生成学习笔记、概念卡、费曼自测、练习题、复习计划”, “沉淀成 TAG 流知识资产”, “看看 Obsidian 里哪些知识可以升级”, “帮我体检知识库”, “找出过时/重复/薄弱/可合并的笔记”, “优化我的标签和双链”, or learning from login-required sources such as Feishu, Notion, Yuque, DingTalk, private wiki, internal docs, and authenticated web pages. This skill should be used even when the user only says “整理/消化/学习/沉淀/升级/改善/体检” and mentions Obsidian, 标签, 双链, 费曼, 复习, 知识库, existing notes, 飞书, 私有文档, 登录, 权限, 授权, or 内部资料.
---

# 学霸

Use this skill in two modes:

1. Study Mode: turn dense or fragmented learning material into one coherent Obsidian study note by default, with optional asset-package expansion only when requested.
2. Upgrade Mode: inspect an existing Obsidian vault or selected notes and identify knowledge that can be improved, merged, split, linked, retagged, verified, or turned into learning assets.

The goal is not to summarize a source. The goal is to create and maintain notes that support understanding, retrieval, review, transfer, and long-term knowledge growth. The first learning output should usually be one complete Markdown note that explains the topic end to end in the style of a "systematic topic note"; many files are useful only after the user wants long-term decomposition.

The user's preferred knowledge style is TAG flow: light folders, strong tags, strong search, selective bidirectional links.

## Core Principles

- Optimize for learning, not note volume. A large MOC or many files does not mean the user has learned the topic.
- Keep every important claim traceable to a source, or mark it as an inference.
- Use tags as controlled metadata. Do not invent near-duplicate tags.
- Use double links only for durable concepts, models, methods, people, technologies, or questions worth reusing.
- Distinguish source claims, AI synthesis, and user-context inference.
- Produce exercises that force recall, explanation, transfer, and real work.
- Default to report-first when upgrading existing notes. Do not rewrite the user's notes unless they explicitly ask you to apply changes.
- Default to one-file output in Study Mode. The single note should resemble a polished Obsidian system topic note: abstract, mental map, concept network, Why/What/How, boundaries, Feynman loop, exercises, sources, and QA. Do not split into MOC, concepts, questions, and exercises as separate files unless the user explicitly asks for a knowledge asset package, concept cards, or long-term vault decomposition.
- Treat authenticated sources as a normal input class. Try safe authorization paths before giving up, but never bypass access controls, scrape cookies/tokens, ask for passwords, or fabricate content from a login page.
- Save durable learning notes into the resolved Obsidian vault under `88-学习/`, not into machine-specific folders, existing personal taxonomies, or a generated-output scratch area. Use generated-output folders only for drafts, tests, failure reports, or intermediate artifacts when the user explicitly wants them.
- Saving to Obsidian means writing into the user's actual Obsidian vault, not merely the current Codex workspace. Resolve the live vault before saving.
- Do not hard-code machine-specific vault paths or Obsidian deep links in this skill. Treat Obsidian as local software plus a set of vault directories that must be discovered or provided at runtime.

## Supported Inputs

Accept these source types:

- Web URL: read the page when network/browser access is available. If inaccessible, ask for pasted content or a local export.
- Authenticated URL: Feishu, Notion, Yuque, DingTalk, private wiki, LMS, Google Docs, and internal docs may require a login session. Use the Authenticated Source Workflow before declaring failure.
- PDF or paper: extract title, author, date, abstract, section structure, page references, and formulas when available.
- Markdown, text, DOCX, slides, or spreadsheet notes: read with the appropriate local tool.
- Video transcript or meeting transcript: preserve timestamps when available.
- Pasted content: treat the pasted text as source and preserve user-provided context.
- Multiple sources: synthesize when they address the same topic; otherwise create one source note plus one synthesis index.

If the source cannot be parsed, return a structured failure with:

```markdown
## 无法处理
- 输入类型：
- 失败原因：
- 需要用户补充：
- 可替代方案：
```

Do not fabricate content to cover missing source text.

## Authenticated Source Workflow

When a source returns a login page, no-permission page, SSO page, empty shell, or JavaScript app without document text, do not summarize the login page. Use this access ladder:

1. **Public fetch**: try normal URL access first and check whether the returned content contains the real document title/body, not just login, loading, or app shell text.
2. **Official export or API**: if a platform connector, CLI, MCP, or official API is available and authorized by the user, use it to export Markdown, HTML, PDF, DOCX, or plain text. Prefer exported files over fragile DOM scraping.
3. **Logged-in browser, visible text only**: if a Chrome/browser tool is available and the user has an active login, ask for permission to open or claim the page. Extract only visible document content and metadata. Do not inspect cookies, local storage, passwords, session files, or hidden tokens.
4. **User-assisted export**: if direct authenticated access is unavailable, ask the user to export or paste the source. Accept Markdown, PDF, DOCX, screenshot OCR only when text export is impossible, or copied page body.
5. **Structured failure**: if no authorized content can be obtained, save or return a failure note with the exact access state and next action.

Security rules:

- Never ask the user for passwords, 2FA codes, cookies, bearer tokens, or session storage.
- Never attempt to bypass SSO, paywalls, ACLs, tenant restrictions, robots controls, or document permissions.
- Never store raw credentials or authorization headers in notes.
- If an API token is already configured in the environment or a tool, use it without printing it; otherwise ask the user to provide an exported file rather than a secret.
- Mark source access in frontmatter with an `access/*` tag.

Allowed access tags:

- `access/public`: source was readable without authentication.
- `access/authenticated`: source was read through an approved logged-in browser, connector, API, or user-authorized session.
- `access/exported`: source came from a user-provided export file.
- `access/pasted`: source came from pasted text.
- `access/blocked`: source could not be read because authentication, permission, or export was unavailable.

For authenticated learning notes, include a short "来源访问方式" line under `## 5. 来源` -> `### 来源与可信度`, for example:

```markdown
- 来源访问方式：`access/authenticated`，通过用户已登录浏览器读取可见正文；未读取 cookies/localStorage。
```

## Controlled Tag System

Use YAML frontmatter tags without `#`. In body text, use `#tag/path` only when necessary.

Default controlled tag dimensions:

```yaml
tags:
  - status/seed
  - type/system-note
  - domain/unknown
  - source/text
  - access/pasted
  - confidence/medium
```

Allowed status tags:

- `status/seed`: newly generated, not yet reviewed by the user.
- `status/processing`: actively being studied or refined.
- `status/reviewed`: checked against sources and useful enough to keep.
- `status/mastered`: user has completed recall and transfer tasks.

Allowed type tags:

- `type/moc`
- `type/overview`
- `type/system-note`
- `type/concept`
- `type/question`
- `type/exercise`
- `type/source`
- `type/qa`

Allowed source tags:

- `source/web`
- `source/feishu`
- `source/notion`
- `source/yuque`
- `source/dingtalk`
- `source/private-wiki`
- `source/pdf`
- `source/paper`
- `source/video`
- `source/markdown`
- `source/text`
- `source/alidoc`
- `source/file`
- `source/multi`

Allowed confidence tags:

- `confidence/low`
- `confidence/medium`
- `confidence/high`

Domain tags should be lowercase English when possible, for example:

- `domain/ai/agent`
- `domain/ai/llm`
- `domain/product/prd`
- `domain/management/okr`
- `domain/business/crm`
- `domain/tech/frontend`
- `domain/tech/backend`
- `domain/operations/store`

If the domain is unclear, use `domain/unknown`. Do not force second or third level classification when the source does not support it.

## Study Mode Output

Default output for Study Mode is a single Markdown file saved under `88-学习/` in the resolved Obsidian vault. First locate the vault/root, then create or reuse the `88-学习/` learning root and choose content-based subfolders under it.

## Obsidian Vault Resolution

Before writing files, resolve Obsidian and the target vault at runtime.

Prefer running `scripts/resolve_obsidian_vault.py --json` when local script execution is available. Use the text workflow below as the fallback when scripts are unavailable.

### 1. Detect Obsidian Availability

First determine whether Obsidian is available on the local machine when the user explicitly wants content placed into or opened in Obsidian.

Use safe, read-only checks appropriate to the OS, for example:

- macOS: check whether `Obsidian.app` is registered or present in common application locations.
- Linux: check whether an `obsidian` executable or desktop entry exists.
- Windows: check whether Obsidian is registered in common application paths or available on `PATH`.

If Obsidian is not installed or cannot be detected:

- Still generate the Markdown note when useful.
- Tell the user that Obsidian was not detected and provide the official Chinese download page: https://obsidian.md/zh/
- Ask the user for an Obsidian vault path before claiming it has been saved into Obsidian.
- Do not fabricate an Obsidian destination.
- Do not use an `obsidian://` deep link as a substitute for a real vault path.

### 2. Locate Candidate Vaults

Resolve the target vault in this order:

1. If the user provides an explicit vault path, use that path.
2. If Obsidian is installed and its local config is readable, inspect the platform-specific Obsidian config location and prefer the vault whose metadata indicates it is currently open or most recently used.
3. Search likely document locations for directories containing `.obsidian`, staying within filesystem permissions.
4. If multiple candidate vaults are found and none is clearly the intended one, ask the user to choose.
5. Do not treat the current Codex workspace as the Obsidian vault unless it contains a `.obsidian` directory or the user explicitly says it is the vault.

Platform config examples:

- macOS: `~/Library/Application Support/obsidian/obsidian.json`
- Linux: commonly `~/.config/obsidian/obsidian.json`
- Windows: commonly `%APPDATA%/obsidian/obsidian.json`

These are discovery hints, not fixed paths. If they are unavailable, fall back to searching for `.obsidian` directories or asking the user.

### 3. Save And Open

Saving to Obsidian means writing a Markdown file into the resolved vault directory.

Only after a real vault path is known:

- use `[vault]/88-学习/` as the learning root; create `88-学习/` if it does not exist
- classify the learning material by content and create/reuse sensible subfolders under `88-学习/`
- report the absolute saved file path

Opening Obsidian is optional. If requested or useful, first verify Obsidian is installed, then use an OS-level opener or construct an Obsidian deep link dynamically from the resolved vault name and relative file path. Never hard-code an `obsidian://` URL in the skill.

### 4. Learning Folder Classification

This is a general-purpose skill for many users and machines. Do not encode one user's local folder taxonomy into the skill.

Use this default layout:

```text
88-学习/
  [大学科]/
    [章节或知识要点]/
      [主题].md
```

Classification guidance:

- Prefer short, direct folder names. Avoid combined names such as `AI与智能体` or `产品与需求` when a clearer subject hierarchy exists.
- The first level under `88-学习/` should be a broad discipline, for example `AI`, `产品`, `管理`, `技术`, `业务`, `读书`, `论文`, `工具`.
- The second level should be a chapter, subdomain, or durable knowledge point, for example under `AI/`: `智能体`, `skills`, `RAG`, `harness`, `prompting`, `MCP`.
- Use one more level only when it meaningfully improves retrieval. Keep the directory tree simple and direct.
- If classification confidence is low, save under `88-学习/待分类/` and add `domain/unknown` or a conservative domain tag.
- Do not save final learning notes into any generated-output scratch area by default.
- If the user explicitly provides a destination folder, respect it after confirming it is inside the resolved vault.

Example paths:

```text
88-学习/AI/智能体/Agent 与 Agent Harness：核心架构.md
88-学习/AI/skills/学霸技能设计与评估.md
88-学习/管理/OKR/OKR 与 KPI：目标管理机制.md
88-学习/产品/PRD/高质量 PRD 的结构化写法.md
```

Use one coherent note that contains the full learning experience. When writing the default single-file note, read and follow `references/note-template.md`.

Use Obsidian double links selectively inside this single note. If a concept deserves a future card, link it and mark it as "可拆卡", but do not create the separate card unless requested. Avoid making the output look like many small disconnected notes pasted together; the note must read as one complete explanation.

## Optional Asset Package

Only create a multi-file asset package when:

- the user explicitly asks for concept cards, MOC, or a full Obsidian asset package
- the source set is too large for one readable note and the user accepts splitting
- the task is upgrading an existing vault and separate reports/cards are safer

When needed, create this package:

```text
学霸/[topic]/
  index.md
  overview.md
  notes.md
  concepts/
    [concept].md
  questions/
    feynman.md
    recall.md
  exercises/
    transfer.md
  review-plan.md
  sources.md
  qa.md
```

Avoid creating empty files.

Use readable Chinese titles for user-facing note titles. Use stable concept filenames that do not include course names, source names, or dates unless needed for disambiguation.

## Mode Selection

Choose Study Mode when the user provides new material or asks to learn a topic from sources.

Choose Upgrade Mode when the user asks to:

- inspect an Obsidian vault or folder
- find notes that can be upgraded
- improve tags, links, MOCs, concept cards, or sources
- detect weak, stale, duplicate, isolated, or overgrown notes
- convert messy notes into reusable learning assets
- build a learning roadmap from existing notes

If the user asks for both, run Upgrade Mode first to understand the existing knowledge base, then run Study Mode for new material and connect it to existing notes.

## Workflow

This workflow describes Study Mode. Use the Upgrade Mode workflow below when the user asks to improve existing Obsidian content.

### 1. Establish Learning Intent

Before generating notes, infer or ask for:

- Topic
- User goal: overview, work application, exam prep, research, or decision support
- Target difficulty: beginner, intermediate, advanced
- Prior knowledge
- Desired output location if saving files; if not provided, save under `88-学习/` and infer content-based subfolders from the topic

If the user wants you to continue without clarification, make conservative assumptions and record them in the single output note.

### 2. Parse And Normalize Sources

Extract:

- Title, author, source URL/path, publication date if available
- Source type
- Core thesis
- Section map
- Important definitions, claims, numbers, formulas, code, and examples
- Source anchors: URL, page number, heading, paragraph, timestamp, or file path

Remove ads, navigation, repeated boilerplate, and low-value filler. Preserve technical details.

### 3. Build The Learning Model

Reconstruct the material using this order:

1. Why: problem, motivation, constraints, historical or business context
2. What: definitions, mechanisms, components, models, assumptions
3. How: procedure, examples, SOP, implementation pattern
4. Limits: boundary conditions, failure modes, common misconceptions, explicit "熔断条件"
5. Transfer: what the learner can do with this knowledge

Do not copy the original table of contents unless it is already the best learning structure.

### 4. Handle Concepts

In default one-file mode, include concepts in a table inside the note. Do not create separate concept files.

Create separate concept cards only in optional asset-package mode or when the user explicitly asks for cards.

When creating separate cards, create them only for durable concepts.

Each concept card should include:

```markdown
---
title: "[概念名]"
aliases: []
tags:
  - status/seed
  - type/concept
  - domain/[domain]
  - confidence/[level]
---

# [概念名]

## 一句话定义

## 边界
- 它是什么：
- 它不是什么：

## 反例

## 常见误区

## 应用场景

## 关联
- 前置：[[...]]
- 后续：[[...]]
- 易混：[[...]]

## 来源
- [source-anchor]
```

Avoid concept cards that only restate a paragraph. A concept card should be reusable outside the original source.

### 5. Generate Learning Tests

Create questions at four levels, preferably inside the single note:

- Recall: closed-book facts, definitions, steps.
- Explanation: Feynman-style explanation and misconception checks.
- Transfer: apply the idea to a new case.
- Real task: a practical output the user can produce.

Every question needs a reference answer, scoring criteria, or expected output. Do not create exercises without answers.

### 6. Build A Review Plan

Use spaced review intervals by default:

- Day 1: recall core concepts and explain the MOC from memory.
- Day 3: answer Feynman questions and correct weak concepts.
- Day 7: complete transfer exercise.
- Day 14: solve a real task or write a one-page synthesis.
- Day 30: decide whether to mark notes as `status/reviewed` or `status/mastered`.

Adapt the plan if the user has an exam date, project deadline, or weekly cadence.

### 7. Run Quality Gate

In default one-file mode, include the quality checklist from `references/note-template.md` under `## 5. 来源`. In asset-package mode, create `qa.md` with the same checks adapted to the generated package.

If an item cannot pass, explain the gap and how to fix it.

## Upgrade Mode Workflow

Use Upgrade Mode to evaluate and improve existing Obsidian knowledge. This mode is a knowledge-base audit, not a destructive rewrite.

### 1. Establish Audit Scope

Identify:

- Vault path or selected folder/files
- Audit goal: tag cleanup, concept upgrade, learning quality, source traceability, duplicate detection, MOC creation, review planning, or all of these
- Update permission: report-only, propose patches, or apply edits
- Safety rule: preserve user text unless the user asks for rewriting

If no vault path is provided, locate likely vaults by searching for `.obsidian`. If multiple vaults are found, ask the user to choose. If no vault is found, ask for the path.

### 2. Inventory Notes

Scan Markdown notes and collect:

- file path
- title
- frontmatter tags, aliases, status, source fields
- outgoing links and unresolved links
- headings
- word count or rough size
- source references
- TODOs or stale markers
- last modified date when available

Do not read every large note in full immediately. Start with metadata and headings, then inspect high-priority candidates.

### 3. Detect Upgrade Opportunities

Classify opportunities into these buckets:

- `missing-tags`: missing or inconsistent TAG flow metadata.
- `tag-drift`: same meaning expressed by multiple tags.
- `orphan-note`: few or no meaningful links to the rest of the vault.
- `weak-source`: important claims lack source anchors.
- `thin-note`: note is too shallow and should become a seed or be merged.
- `overgrown-note`: note covers too many ideas and should be split into concept cards.
- `duplicate-concept`: multiple notes describe the same concept.
- `concept-candidate`: recurring idea worth extracting into a concept card.
- `moc-candidate`: cluster of related notes deserves an index/MOC.
- `review-candidate`: useful note lacks questions, exercises, or review plan.
- `stale-knowledge`: note may be outdated based on age, status, or topic volatility.
- `broken-link`: unresolved or misleading double link.

Do not assume a note is wrong just because it is old. Mark stale knowledge as "needs verification" unless you have checked current sources.

### 4. Score Candidates

Score each candidate from 1 to 5:

- Impact: how much learning or retrieval improves.
- Confidence: how sure the recommendation is from local evidence.
- Effort: how much work the update likely requires.

Prioritize high-impact, high-confidence, low-effort upgrades first.

### 5. Produce Upgrade Report

Create an upgrade report at:

```text
学霸/知识库升级报告/YYYY-MM-DD-知识库升级报告.md
```

Use this structure:

```markdown
---
title: "知识库升级报告"
tags:
  - status/seed
  - type/qa
  - domain/knowledge-management/obsidian
  - source/file
  - confidence/medium
---

# 知识库升级报告

## 审计范围
- 路径：
- 笔记数量：
- 本次目标：
- 模式：report-only | propose-patches | apply-edits

## 总体判断
- 当前知识库最强的地方：
- 最大的知识复利机会：
- 最大风险：

## 优先升级清单
| 优先级 | 文件 | 问题类型 | 建议动作 | 影响 | 置信度 | 工作量 |
|---|---|---|---|---:|---:|---:|

## TAG 流问题

## 双链与 MOC 机会

## 概念卡升级机会

## 来源与可信度问题

## 学习质量升级

## 建议的下一步
```

### 6. Propose Or Apply Changes

In report-only mode, stop after the report and ask which upgrades to apply.

In propose-patches mode, produce per-note patch plans without editing:

```markdown
## [文件路径]
- 建议动作：
- 原因：
- 预期收益：
- 风险：
- 建议新增标签：
- 建议新增链接：
- 建议拆分/合并：
```

In apply-edits mode, edit only the notes explicitly selected by the user. Before editing:

1. Re-read the target note.
2. Preserve original user wording where possible.
3. Add missing frontmatter and sections incrementally.
4. Do not delete content unless the user asks.
5. Record changes in the final response.

### 7. Upgrade Quality Gate

For every applied upgrade, check:

- [ ] User-selected scope only
- [ ] No accidental deletion of original content
- [ ] Tags use controlled TAG flow vocabulary
- [ ] Added links point to durable concepts
- [ ] Claims are sourced or marked as inference
- [ ] Suggested splits/merges are explained
- [ ] Review tasks are actionable

## Markdown Templates

### index.md

```markdown
---
title: "[主题] 知识地图"
tags:
  - status/seed
  - type/moc
  - domain/[domain]
  - source/[source-type]
  - confidence/[level]
---

# [主题] 知识地图

## 一句话系统本质
[不超过 100 字，说明这个知识解决的核心问题。]

## 学习路径
1. [[overview]]
2. [[notes]]
3. [[questions/feynman]]
4. [[exercises/transfer]]
5. [[review-plan]]

## 核心概念
- [[概念A]]：[一句话定义]
- [[概念B]]：[一句话定义]

## 关键问题
- [这个主题最重要的问题是什么？]

## 输出能力
- 学完后，用户应该能够：[具体能力]
```

### notes.md

````markdown
---
title: "[主题] 系统化笔记"
tags:
  - status/seed
  - type/system-note
  - domain/[domain]
  - source/[source-type]
  - confidence/[level]
---

# [主题]：系统化学习笔记

## 1. 全景

```text
[核心主题]
├── 核心痛点 Why
├── 底层机制 What
├── 落地路径 How
├── 局限误区 Limits
└── 迁移产出 Transfer
```

## 2. 正文

### Why：问题与背景

### What：体系与机制

### How：落地应用

### Limits：局限与误区

### Transfer：迁移产出

## 3. 来源
- [source-anchor]
````

## Final Response

When done, report:

- Saved paths
- Source access limitations
- Main generated assets
- Quality gate status
- Next recommended review action

Keep the response concise. The files should carry the detail.
