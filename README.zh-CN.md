# 企业级 AI OS：一个架构，三个尺度

### 为什么护城河是「记忆」与「治理」，而不是模型

> 一份自底向上的企业 AI 参考架构——从一个跑通的 n=1 系统推算出来，而不是从厂商 PPT 自顶向下。作者：naze。

**[English](README.md)** · **中文**

---

## TL;DR

任何「AI OS」——无论它运行的是一个人的生活、一家创业公司的运营，还是十万人的企业——本质都是**同一套七层栈**。其中五层（算力、接入、模型、行动、编排）是 **commodity**：人人都会有，且会卷到同质。真正决定胜负的是两层：

- **③ 记忆** —— 组织积累的、专属的、带 provenance 的认知。模型之所以可换，正因为连续性住在这一层。
- **⑦ 治理** —— 让自治 agent 跑得快**又不悄悄漂移**、且这一切可审计的内核。这是企业采购的真门槛。

而且这套架构**尺度不变**。从 n=1 到企业，变的只是 actor 数、规模、合规——不是内核。这意味着：**把内核做对的最便宜的地方，是最小的尺度。**

## 七层栈

```
⑦ 治理 Governance ★    provenance · drift · 合规审计 · judgment gate · capability token
⑥ 编排 Orchestration   agent mesh · A2A 跨 BU · workflow · 调度 · durable execution
⑤ 行动 Executor        工具网关 · MCP server farm · RPA · 权限校验 · 幂等/补偿
④ 智能 Brain           模型层(可换) · 路由 · 微调 · 规则层 · eval
③ 记忆 Memory ★        企业知识图 · role-scoped 视图 · 向量+图+时序   ← 第一护城河
② 感知 Sensor          全渠道+全系统 ingestion · event bus · 入口脱敏
① 基底 Substrate       算力 · 数据湖 · 组织身份/RBAC · 网络
  ── 横切 PaaS：各 BU 自建 vertical agent · role-scoped digest · 信息损耗 router ──
```

## 目录

- [01 · 七层架构](01-seven-layer-architecture.zh-CN.md) —— 每层是什么、组件、agents、怎么失败
- [02 · 两条护城河与治理内核](02-moat-and-governance.zh-CN.md) —— 记忆 + 治理为什么不可复制
- [03 · 一个架构，三个尺度](03-three-scales.zh-CN.md) —— 个人 / 创业 / 大厂是同一件事
- [04 · 落地、战略与边界](04-adoption-and-boundaries.zh-CN.md) —— build sequence + 战略含义 + 这不是什么

## 一句话

如果模型是 commodity、护城河是记忆与治理，那理性的路径不是去追最大的模型，而是**在最便宜、迭代最快的尺度（n=1）把内核做对，再向上放大**。一个人跑通这套架构，验证机制的成本只是一个 git 仓库加一点纪律。

## 内核与相关

这套架构的内核（provenance / drift / judgment / 反 silent-capture / calibration）来自一份更上游的 position paper —— 它把"人类判断与自进化 agent 之间那层缺失的内核"讲清楚；本仓库是它的**企业尺度延伸**。

- [coevolution-kernel](https://github.com/hegu-1/coevolution-kernel) —— 内核 thesis（人类判断 ↔ 自进化 agent）
- [personal-memory-vault-starter](https://github.com/hegu-1/personal-memory-vault-starter) —— n=1 尺度的可 clone 结构 starter

---

_由 naze 整理。源自一个 n=1 的个人记忆系统 + 关于 provenance / drift / judgment / calibration 的公开 kernel 工作。_

_这是一份**参考架构**，推算自一个跑通的小尺度系统，不是任何特定大公司的真实内部架构。_
