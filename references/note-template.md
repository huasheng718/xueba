# 学霸单文件学习笔记模板

Use this template when Study Mode creates one Obsidian learning note.

The note should be complete but concise. Keep the main headings fixed and simple:

```markdown
## 1. 全景
## 2. 概念
## 3. 正文
## 4. 练习
## 5. 来源
```

Do not expand these into many top-level sections. Put detail inside the existing sections.

## Template

````markdown
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
audience: "[目标读者或使用场景]"
depth: "[beginner/intermediate/advanced]"
---

# 系统化专题：[[主题]]

> [!abstract] 一句话系统本质
> 用不超过 100 字说明这个知识解决的核心问题、底层机制和适用价值。不要写“本文介绍了...”，直接给本质判断。

## 1. 全景

### 学习目标

学完本文后，应该能够：

1. 理解 [...]
2. 解释 [...]
3. 应用 [...]

### 前置知识

| 前置知识 | 为什么需要 |
|---|---|
|  |  |

```text
[[核心主题]]
├── Why -> 为什么需要它？
├── What -> 它的核心骨架与运转逻辑是什么？
├── How -> 如何应用、实施或复用？
└── Limits -> 何时失效、误区是什么？
```

## 2. 概念

| ID | 概念 | 别名/英文 | 一句话解释 | 边界/误区 | 关系 | 可拆卡 | 来源锚点 |
|---|---|---|---|---|---|---|---|
| C001 | [[概念A]] |  |  |  | depends_on: C002 | 是/否 |  |

## 3. 正文

### Why：问题与背景

### What：机制与结构

### How：应用与步骤

### Limits：边界与误区

### Evidence：依据、推论与待验证

| 类型 | 内容 | 来源锚点/原因 |
|---|---|---|
| 原文依据 |  |  |
| 推论 |  |  |
| 待补充 |  |  |
| 待验证 |  |  |

### Links：和已有知识/工作的连接

## 4. 练习

### 费曼自测

### 闭卷回忆

### 迁移任务

### 复习节奏

## 5. 来源

### 来源与可信度

### AI 读取区

```yaml
summary:
  topic: "[主题]"
  main_idea: "[核心思想]"
  key_takeaways:
    - "[要点1]"
concepts:
  - id: C001
    name: "[概念名]"
    definition: "[定义]"
    aliases: []
    related:
      - C002
relations:
  - from: C001
    to: C002
    type: "depends_on"
    description: "[关系说明]"
keywords:
  primary: []
  secondary: []
  english_terms: []
qa_pairs:
  - question: "[问题]"
    answer: "[答案]"
    type: "recall"
```

### 质量检查
````

## Section Rules

- `全景`: Give learning goals, prerequisites, the topic map, and 2-5 high-level judgments.
- `概念`: Link only durable concepts with Obsidian double brackets. Use stable IDs such as `C001` only as retrieval/relationship handles.
- `正文`: Explain the topic end to end. Keep Why / What / How / Limits / Evidence / Links as subheadings.
- `练习`: Every question should include an answer, scoring rule, or expected output.
- `来源`: Include source access method, source list, confidence, limitations, AI-readable YAML, and quality checks.

## Quality Checklist

```markdown
### 质量检查

#### 来源追踪
- [ ] 关键论断有来源锚点
- [ ] 原文观点、AI 转述、推理扩展已区分
- [ ] `原文依据`、`推论`、`待补充`、`待验证` 已清楚标记

#### TAG 流
- [ ] 标签使用受控词表
- [ ] domain 标签没有过度推断
- [ ] status/type/source/access/confidence 标签齐全

#### 双链
- [ ] 只链接长期可复用概念
- [ ] 没有给普通关键词制造伪双链

#### 学习效果
- [ ] 主目录保持简洁：全景、概念、正文、练习、来源
- [ ] 全景包含学习目标、前置知识和知识地图
- [ ] 正文覆盖 Why / What / How / Limits / Evidence
- [ ] 练习题包含答案或评分标准
- [ ] 复习节奏有间隔和具体任务
- [ ] AI 读取区包含概念 ID、关键词、关系和问答对
```
