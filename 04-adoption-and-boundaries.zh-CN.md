# 04 · 落地、战略与边界

> [English (full paper) →](README.md) · [← 中文总览](README.zh-CN.md)

## 落地 sequence

任何尺度都是同一套分阶段推进：

1. **单 vertical（或单 BU）打样** —— 选一个高频、高痛的场景，把四层闭环跑通。
2. **横向复制到 2–3 个** —— 证明底座可复用。平台（PaaS）层在这一步成形。
3. **信号回流 + 跨 vertical** —— 让用户/业务信号在各 vertical 之间流动。
4. **加跨域 OS 层** —— 共享记忆图 + cross-BU router + role/exec digest + 治理。

只有到第 4 步，它才从「N 个堆在一起的自动化」变成「一个 OS」——因为这时信息不再卡在孤岛之间。

**每一步内部都是 provenance 优先**——没有它，上面一切都建在沙子上。

## 战略含义

如果模型是 commodity、护城河是记忆与治理，那理性路径不是去追最大的模型，而是**在最便宜、迭代最快的尺度，把内核——记忆即容器 / provenance / 判断保全 / 反 silent-capture / calibration——做对，再向上放大**。

n=1 就是那个尺度。一个人跑通这套架构，验证机制的成本只是一个 git 仓库加一点纪律。

大厂有规模、有合规。多数还没有的，是一个想清楚的内核——它们还在 commodity 层卷。本文是一次尝试，去**指出真正的、持久的价值到底坐落在哪一层**。

## 这不是什么

- 这是一份**从跑通的小尺度系统推算出的参考架构**，不是任何特定大公司的真实内部架构。各层对应到具体厂商只是示意。
- 论点不是「我做出了企业 AI OS」，而是：**两条护城河的「机制」是尺度不变的、且能被廉价验证**——而能力（人人都在拼的那部分）恰恰是会 commoditize 的部分。

---

_由 naze 整理。结构开源 starter：[personal-memory-vault-starter](https://github.com/hegu-1/personal-memory-vault-starter)。_
