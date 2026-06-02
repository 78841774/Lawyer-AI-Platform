# Runtime Architecture

Workspace Runtime 是 Lawyer AI Platform 中负责案件执行的运行时系统。

Runtime 不训练能力，只负责加载、调度、执行和记录。能力由 Training System 生产为 Experience Package，并由 Workspace Runtime 在具体案件中加载和使用。

## 运行时模块

* Material Runtime：负责案件材料上传、解析、分片、元数据记录和来源定位。
* Fact Runtime：负责调用事实抽取技能，生成 Fact Schema，维护事实状态和证据引用。
* Legal Runtime：负责基于 Fact Schema 调用法律分析技能，生成 Legal Reasoning Schema。
* Strategy Runtime：负责基于事实、法律分析和案件目标生成诉讼策略、谈判策略或执行策略。
* Document Runtime：负责基于模板和案件上下文生成报告、诉讼文书、函件和工作底稿。
* Gate Runtime：负责执行质量门禁，检查事实完整性、引用完整性、法律依据、风险提示和输出质量。
* Experience Package Loader：负责加载经验包，解析 package.json、技能、模板、schema、gate 和 runtime_config。

## 职责边界

* Runtime 不负责模型训练、技能训练或经验沉淀。
* Runtime 不修改 Experience Package 的核心能力内容。
* Runtime 可记录执行日志、审计日志、Gate 结果和人工复核意见。
* Runtime 应保证每次输出均可回溯到输入材料、事实、法律依据和运行配置。

## 运行流程

1. 创建案件，初始化 case_id 和案件上下文。
2. Experience Package Loader 根据案件类型加载对应 Experience Package。
3. Material Runtime 接收案件材料，完成解析、分片和来源记录。
4. Fact Runtime 基于材料和经验包技能抽取案件事实，生成 Fact Schema。
5. Gate Runtime 执行事实完整性和来源可追溯检查。
6. Legal Runtime 基于 Fact Schema、法律规则和知识引用生成 Legal Reasoning Schema。
7. Gate Runtime 执行法律依据、事实引用和推理链检查。
8. Strategy Runtime 生成案件策略建议，并引用事实和法律分析结果。
9. Document Runtime 基于模板生成法律分析报告、策略报告或诉讼文书。
10. Gate Runtime 对最终输出执行质量检查并记录 gate_results。
11. Workspace Runtime 写入执行日志、审计日志和可复核记录。

## 简化架构图

```text
Training System
      |
      v
Experience Package
      |
      v
Experience Package Loader
      |
      v
Workspace Runtime
  | Material Runtime
  | Fact Runtime
  | Legal Runtime
  | Strategy Runtime
  | Document Runtime
  | Gate Runtime
      |
      v
Audit Log / Gate Results / Case Outputs
```
