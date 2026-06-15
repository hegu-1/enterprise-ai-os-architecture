# 01 · 七层架构

> [English (full paper) →](README.md) · [← 中文总览](README.zh-CN.md)

自底向上。每层：是什么 / 组件 / 住在里面的 agents / 怎么失败 / 是买、是集成、还是赢。

## ① 基底 Substrate
- **是什么**：算力 + 数据 + 身份 + 网络 的物理/逻辑底。
- **组件**：GPU 池 + 推理调度、数据湖/lakehouse、组织身份（SSO/RBAC/SCIM）、网络隔离、secrets/KMS。
- **agents**：无（纯基础设施）；capacity-autoscaler / cost-governor 算半个。
- **怎么失败**：身份是权限的根——错了全盘错；数据湖治理不力会沼泽化。
- **结论**：买。不差异化。

## ② 感知 Sensor
- **是什么**：从每个渠道和系统接入——IM / 邮件 / 工单 / 会议 / 文档 / 代码 / CRM / ERP / 日志——汇入统一 event bus + schema registry。
- **组件**：各系统 connector、normalizer、dedup、**入口处的 PII 脱敏**（入口脱敏是记忆层权限的前置条件）。
- **怎么失败**：源 schema 静默漂移、事件重复或丢失、未脱敏 PII 入库污染下游。
- **结论**：集成。标准 data engineering。

## ③ 记忆 Memory ★（第一护城河）
- **是什么**：不是数据库，是一个**活的认知底**——每个 agent 持续读写、会巩固会遗忘、带来源带置信。查询模式是 pre-compile + 联想，不是 query-time 现拼（RAG 的局限）。
- **分层**（像记忆本身）：
  ```
  L4 战略/telos    组织目标、为什么做        ← 人 authored
  L3 语义+程序     概念 / SOP / 政策 / 知识图
  L2 工作知识      项目 / 文档 / 固化结论
  L1 情景          决策 / 事件 / 事故 / 交互
  L0 原始          全 ingestion，immutable，带 provenance 戳
  ```
- **物理**：时序**知识图**（实体/关系 + 有效期窗口）+ **向量库** + **文档底**，统一 hybrid 检索。
- **企业特有的难点**：**权限随记忆走**——同一张底图按 role / BU 投影出不同视图，检索**先过权限再返回**，不是先取后滤。这里出错不是 bug，是数据泄露。
- **recall 像人脑**：沿图的边联想（**跨 BU 的边就是打破信息孤岛**）、惰性只取「激活 ∩ 有权限」的子图、显著性/新近加权、后台持续**巩固**（raw→情景→语义，去重/合并/过期），与合规驱动的保留/遗忘并存。
- **为什么是护城河**：积累性（时间不可压缩）、专属性（别家没有你的组织认知）、可信（provenance + 审计）。模型可换，正因为这层持有连续性。

## ④ 智能 Brain
- **是什么**：模型能力层 + 怎么选/用模型。
- **组件**：基础模型（自研 + 外部，**可热插拔**）、模型路由（任务/成本/敏感度/延迟）、领域微调/adapter、规则层（简单不过大模型）、推理缓存。
- **agents**：model-router、domain-expert、rule-engine、eval-harness。
- **怎么失败**：什么都路由到最大模型（贵且慢）、微调过拟合/灾难遗忘、敏感数据进外部模型（合规红线）。
- **结论**：路由与微调有点 craft，但模型本身是 commodity。**真正的差异不在模型，在记忆喂给它的 context。**

## ⑤ 行动 Executor
- **是什么**：把决策变成真实世界动作。
- **组件**：工具/API 网关、**MCP server farm**（全公司工具统一暴露）、RPA、审批流、每个 action 过 RBAC + 治理、幂等/重试/补偿。
- **agents**：tool-gateway、action-executor、approval-router。
- **怎么失败**：越权执行（必须**先治理后执行**，不能先做后滤）、非幂等重复（重复扣款）、工具碎片（无统一网关则每 agent 各接各的）。
- **结论**：集成。MCP server farm 是 2026 的标准做法。

## ⑥ 编排 Orchestration
- **是什么**：多 agent 协同 + 跨 BU + 长流程。
- **组件**：agent mesh、A2A 跨 BU 委派（Agent Card 发现）、workflow 引擎、调度、durable execution（长流程崩溃可恢复）、saga/补偿。
- **agents**：orchestrator、cross-bu-router、scheduler。
- **怎么失败**：编排死锁/环、责任漂（该做的没 agent 认领）、长流程状态丢、过度编排（本可一个 agent 干的拆太碎）。
- **结论**：真 engineering，但有成熟开源；craft 在 router 把对的活给对的 agent。

## ⑦ 治理 Governance ★（第二护城河 + 采购门槛）
见 [02 · 两条护城河与治理内核](02-moat-and-governance.zh-CN.md)。

---

横切，还有一层 **平台（PaaS）**：各 BU 在共享底座上自建自己的 vertical agent；role-scoped digest 给每个角色各自的视图（高管层只看 结论 / 异常 / 决策）；信息损耗 router 把对的信号送到对的人或 agent。
