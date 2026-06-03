# Training Pipeline

Training Pipeline 定义 Skill Factory 从真实案件生成 Experience Package 的标准流水线。

## 一、总体流程

```text
Case
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

## 二、Case

Case 是训练输入。

Case 可以来源于：

- 已结案件
- 在办案件复盘
- 律师审核过的模拟案例
- 裁判文书与律师复盘结合样本

Case 应包含：

- 案件基本信息
- 当事人关系
- 案件材料
- 证据目录
- 律师意见
- 裁判结果或预期结果
- 办案复盘

训练前必须完成：

- 脱敏处理
- 权限确认
- 样本归类
- 材料完整性检查

## 三、Fact Pattern Extraction

目标：

从案件材料中提炼可复用事实模式。

任务：

- 识别主体
- 识别法律关系
- 抽取关键时间线
- 抽取合同、付款、履行、违约、损失等事实
- 建立事实与证据映射
- 标记缺失事实和事实冲突

输出：

```text
fact_pattern.json
fact_evidence_map.json
missing_fact_list.json
```

质量要求：

- 不遗漏关键法律事实
- 不将无证据支持的信息写成确定事实
- 明确区分陈述事实、证据事实和推定事实

## 四、Reasoning Extraction

目标：

从律师分析和裁判规则中抽取可复用推理路径。

任务：

- 归纳争议焦点
- 提炼构成要件
- 匹配法条和裁判规则
- 识别举证责任
- 提炼原告论证路径
- 提炼被告抗辩路径
- 提炼风险判断标准

输出：

```text
reasoning_pattern.json
legal_issue_map.json
argument_strategy.json
risk_assessment_rule.json
```

质量要求：

- 法律依据必须明确
- 推理链条必须可追溯
- 不得混淆事实判断与法律评价
- 必须覆盖主要争议焦点

## 五、Prompt Generation

目标：

将事实模式和推理模式转化为可执行 Prompt。

Prompt 类型：

- fact_prompt.txt
- analysis_prompt.txt
- report_prompt.txt

生成规则：

- fact_prompt 负责事实抽取和证据映射
- analysis_prompt 负责法律分析、争议焦点和风险判断
- report_prompt 负责生成律师可审阅、客户可交付的报告

Prompt 必须包含：

- 任务定义
- 输入范围
- 输出结构
- 禁止事项
- 质量标准
- 自检规则

输出：

```text
fact_prompt.txt
analysis_prompt.txt
report_prompt.txt
```

## 六、Template Generation

目标：

将律师交付成果沉淀为可复用模板。

模板类型：

- 事实梳理模板
- 法律分析模板
- 诉讼策略模板
- 客户报告模板
- 风险提示模板

模板必须包含：

- 标题结构
- 章节结构
- 必填字段
- 可选字段
- 引用规则
- 证据展示规则

输出：

```text
templates/fact_report.md
templates/legal_analysis.md
templates/litigation_strategy.md
templates/client_report.md
```

## 七、Skill Candidate

目标：

将 Prompt、Template、测试样本和元数据组装为候选技能。

Skill Candidate 包含：

- skill.json
- fact_prompt.txt
- analysis_prompt.txt
- report_prompt.txt
- templates/
- tests/
- evaluation_config.json

状态：

```text
Draft
```

进入下一阶段前必须完成：

- Schema 校验
- Prompt 完整性检查
- Template 字段检查
- 测试样本绑定

## 八、Evaluation

目标：

验证 Skill Candidate 是否具备可发布质量。

评估维度：

- accuracy
- consistency
- completeness
- legal_relevance
- report_quality

评估输入：

- 标准测试案件
- 律师标注答案
- 预期报告结构
- 评价阈值

评估输出：

```text
evaluation_report.json
evaluation_summary.md
failure_cases/
```

通过条件：

- overall_score 达到发布阈值
- 所有核心指标达到最低阈值
- 无严重法律错误
- 报告可供律师复核

未通过：

返回 Prompt Generation 或 Template Generation 阶段继续优化。

## 九、Experience Package

目标：

将通过评估的 Skill Candidate 封装为 Experience Package。

输出：

```text
experience-package/
├── skill.json
├── fact_prompt.txt
├── analysis_prompt.txt
├── report_prompt.txt
├── templates/
└── tests/
```

发布后：

- 状态变更为 Published
- 写入版本记录
- 写入评估摘要
- 可被 Workspace System 加载

## 十、闭环机制

Workspace 运行产生的反馈可以进入下一轮训练。

反馈包括：

- 律师修改记录
- Gate 评分
- 用户反馈
- 失败样本
- 新增证据类型
- 新增争议焦点

反馈不得直接修改已发布 Experience Package。

必须进入新版本训练。

## 十一、v2.1 Runtime 映射

v2.1 将架构流水线落到主后端的规则式 Skill Training Runtime。

运行时输入来自已完成的案件链路：

```text
Case
  |
  v
Material
  |
  v
Fact
  |
  v
Legal Analysis
  |
  v
Report
```

Skill Training Runtime 在此基础上生成：

```text
Fact Pattern Extraction
  -> app/skill_training/fact_pattern_extractor.py

Reasoning Extraction
  -> app/skill_training/reasoning_extractor.py

Prompt Generation
  -> app/skill_training/prompt_generator.py

Template Generation
  -> app/skill_training/template_generator.py

Skill Candidate
  -> app/skill_training/skill_builder.py

Evaluation
  -> app/skill_training/evaluator.py

Experience Package Export
  -> app/skill_training/package_exporter.py
```

v2.1 输出：

```text
Lawyer-AI-Platform-App/skills/{skill_id}/
├── skill.json
├── fact_prompt.txt
├── analysis_prompt.txt
├── report_prompt.txt
└── templates/
    └── report_template.md
```

v2.1 限制：

- 仅生成 Skill Candidate 草稿
- 仅使用规则方法
- 不接真实 AI
- 不执行完整律师评估
- 不发布正式 Experience Package
