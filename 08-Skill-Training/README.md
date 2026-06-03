# Skill Training

Skill Training 是 Lawyer AI Platform v2.0 的技能工厂模块。

本模块负责将真实案件中的律师经验沉淀为可复用、可评估、可发布的 Experience Package。

Skill Training 不处理线上案件运行，也不替代 Workspace System。

它的职责是：

- 从真实案件中抽取事实模式
- 从律师分析中抽取推理路径
- 将办案经验转化为 Prompt
- 将交付成果转化为 Template
- 生成 Skill Candidate
- 通过 Evaluation Framework 验证候选技能
- 构建 Experience Package

## 一、模块定位

Skill Training 位于 Training System 与 Experience Package Spec 之间。

Training System 定义能力生产流程。

Skill Training 定义能力如何被沉淀、评价和封装。

Experience Package Spec 定义最终包的标准结构。

Workspace System 只加载已发布的 Experience Package，不参与技能训练。

## 二、总体架构

```text
Real Case
  |
  v
Fact Pattern Extraction
  |
  v
Reasoning Extraction
  |
  v
Prompt Generation
  |
  v
Template Generation
  |
  v
Skill Candidate
  |
  v
Evaluation
  |
  v
Experience Package
```

## 三、核心对象

### Case

真实案件样本，包括材料、事实、证据、律师意见、裁判结果和复盘记录。

### Fact Pattern

从案件中抽取出的可复用事实结构。

例如：

- 合同订立事实
- 履行过程事实
- 违约行为事实
- 损失计算事实
- 证据对应关系

### Reasoning Pattern

从律师分析中抽取出的法律推理路径。

例如：

- 法律关系识别
- 争议焦点归纳
- 构成要件分析
- 举证责任分配
- 抗辩路径评估
- 裁判风险判断

### Skill Candidate

尚未发布的候选技能。

Skill Candidate 必须包含 Prompt、Template、测试样本、评价指标和元数据。

### Experience Package

通过评估后的技能包。

Experience Package 是 Workspace System 可以加载的能力交付单元。

## 四、文档结构

- Skill-Schema.md：Skill 数据结构定义
- Training-Pipeline.md：技能训练流水线
- Evaluation-Framework.md：评估框架与评分机制
- Package-Build-System.md：Experience Package 构建与输出格式
- Skill-Versioning.md：技能版本管理
- Skill-Lifecycle.md：技能生命周期
- Example-Contract-Dispute-Skill.md：合同纠纷技能示例

## 五、设计原则

### 来源真实

技能必须来源于真实案件、真实律师经验或经过律师确认的模拟样本。

### 结构稳定

事实、推理、提示词、模板和测试必须被结构化保存。

### 可评估

每个技能都必须通过 accuracy、consistency、completeness、legal_relevance 和 report_quality 评估。

### 可升级

技能必须支持版本升级、兼容性检查和废弃管理。

### 可追溯

每个 Experience Package 必须记录来源案件类型、训练样本范围、评估结果、版本和发布状态。

