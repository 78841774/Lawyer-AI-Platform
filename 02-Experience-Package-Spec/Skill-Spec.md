Skill 规范（Skill Specification）

一、定位

Skill 是律师经验的最小能力单元。

Skill 不等于 Prompt。

Skill 不等于 Agent。

Skill 不等于模型。

Skill 是可训练、可复用、可部署的能力对象。

⸻

二、Skill 生命周期

经验

↓

训练

↓

Skill

↓

验证

↓

Experience Package

↓

Workspace部署

↓

反馈

↓

再训练

⸻

三、Skill 组成

Metadata

基础信息

包括：

* Skill名称
* Skill版本
* 适用案由
* 作者
* 发布时间

⸻

Capability

能力定义

例如：

事实提取

证据分析

法律关系识别

抗辩策略分析

损失计算

⸻

Reasoning

推理规则

包括：

* 思考步骤
* 推理流程
* 分析框架

⸻

Knowledge Reference

知识引用规则

包括：

* 法条
* 司法解释
* 指导案例
* 裁判规则

⸻

Gate Reference

门控规则引用

关联：

Gate Skill

⸻

Output Schema

输出结构

例如：

Fact JSON

Legal JSON

Report JSON

⸻

四、Skill 分类

Fact Skill

事实技能

例如：

主体识别

时间线提取

证据提取

⸻

Legal Skill

法律技能

例如：

法律关系识别

法条匹配

争议焦点分析

⸻

Strategy Skill

策略技能

例如：

原告策略

被告策略

执行策略

⸻

Report Skill

报告技能

例如：

分析报告

代理意见

法律意见书

⸻

五、Skill 与 Prompt

Prompt 是 Skill 的实现方式之一。

Skill 不依赖 Prompt。

未来：

Prompt

Agent

Workflow

Rule Engine

均可实现 Skill。

⸻

六、Skill 与模型

Skill 不绑定模型。

支持：

GPT

Claude

DeepSeek

Qwen

未来模型

⸻

七、Skill 与 SkillOpt

SkillOpt 是训练框架。

Skill 是训练结果。

因此：

SkillOpt 可替换。

Skill 保持稳定。

⸻

八、Skill 与 Experience Package

多个 Skill 组合：

形成 Experience Package。

例如：

Construction Package

├── Fact Skill
├── Legal Skill
├── Strategy Skill
└── Report Skill

⸻

九、Skill 版本

采用：

Major.Minor.Patch

例如：

FactSkill 2.1.3

LegalSkill 1.8.0

⸻

十、平台原则

平台不绑定训练工具。

平台不绑定模型。

平台只认：

Skill Standard

Experience Package Standard

确保：

训练系统可演化。

生产系统保持稳定。