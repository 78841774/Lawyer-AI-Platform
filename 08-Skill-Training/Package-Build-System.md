# Package Build System

Package Build System 定义 Skill Factory 如何将通过评估的 Skill Candidate 构建为 Experience Package。

本文件只定义架构与输出格式，不涉及运行代码实现。

## 一、构建目标

构建系统的目标是生成稳定、可审计、可发布的 Experience Package。

Experience Package 必须包含：

- 技能元数据
- 事实抽取 Prompt
- 法律分析 Prompt
- 报告生成 Prompt
- 文档模板
- 测试样本
- 评估结果

## 二、输出目录结构

标准输出格式：

```text
experience-package/
├── skill.json
├── fact_prompt.txt
├── analysis_prompt.txt
├── report_prompt.txt
├── templates/
│   ├── fact_report.md
│   ├── legal_analysis.md
│   ├── litigation_strategy.md
│   └── client_report.md
└── tests/
    ├── cases/
    ├── expected_outputs/
    ├── evaluation_report.json
    └── evaluation_summary.md
```

## 三、skill.json

skill.json 是 Experience Package 的入口文件。

必须包含：

- skill_id
- skill_name
- domain
- jurisdiction
- version
- prompts
- templates
- evaluation_metrics
- metadata

示例：

```json
{
  "skill_id": "contract-dispute-cn-v1",
  "skill_name": "Contract Dispute Skill",
  "domain": "contract_dispute",
  "jurisdiction": "CN",
  "version": "v1",
  "prompts": {
    "fact_prompt": "fact_prompt.txt",
    "analysis_prompt": "analysis_prompt.txt",
    "report_prompt": "report_prompt.txt"
  },
  "templates": {
    "fact_report": "templates/fact_report.md",
    "legal_analysis": "templates/legal_analysis.md",
    "litigation_strategy": "templates/litigation_strategy.md",
    "client_report": "templates/client_report.md"
  },
  "evaluation_metrics": {
    "accuracy": 0.88,
    "consistency": 0.84,
    "completeness": 0.86,
    "legal_relevance": 0.89,
    "report_quality": 0.83
  },
  "metadata": {
    "lifecycle_status": "Published",
    "source_case_count": 25,
    "created_at": "2026-06-03",
    "published_at": "2026-06-03"
  }
}
```

## 四、Prompt 文件

### fact_prompt.txt

用途：

指导系统从案件材料中抽取事实模式。

必须定义：

- 输入材料范围
- 主体识别规则
- 时间线抽取规则
- 证据映射规则
- 缺失事实识别规则
- 输出 JSON 或 Markdown 结构

### analysis_prompt.txt

用途：

指导系统基于事实模式完成法律分析。

必须定义：

- 法律关系识别规则
- 争议焦点归纳规则
- 法条与裁判规则匹配规则
- 请求与抗辩分析规则
- 风险判断规则
- 禁止虚构法律依据规则

### report_prompt.txt

用途：

指导系统将事实和法律分析生成律师报告。

必须定义：

- 报告受众
- 报告章节结构
- 风险表达方式
- 证据引用方式
- 结论表达方式
- 自检清单

## 五、templates/

templates 目录保存文档模板。

模板要求：

- 可复用
- 不绑定单个案件
- 明确必填字段
- 支持律师修改
- 与 report_prompt 对齐

标准模板：

```text
templates/fact_report.md
templates/legal_analysis.md
templates/litigation_strategy.md
templates/client_report.md
```

## 六、tests/

tests 目录保存技能测试材料。

标准结构：

```text
tests/
├── cases/
│   ├── case-001.md
│   └── case-002.md
├── expected_outputs/
│   ├── case-001.expected.md
│   └── case-002.expected.md
├── evaluation_report.json
└── evaluation_summary.md
```

tests 必须包含：

- 正常案件样本
- 边界案件样本
- 材料缺失样本
- 事实冲突样本
- 典型抗辩样本

## 七、构建检查

构建前检查：

- skill.json 字段完整
- Prompt 文件存在
- Template 文件存在
- tests 目录存在
- evaluation_report.json 存在
- 评估结果达到发布阈值
- lifecycle_status 为 Validated 或 Published

构建失败情形：

- 缺少必要文件
- 评估未通过
- 版本号冲突
- 法域未声明
- 存在严重错误
- metadata 缺少来源记录

## 八、发布边界

Experience Package 发布后不可直接修改。

任何调整必须：

- 创建新版本
- 重新评估
- 重新构建
- 重新发布

Workspace System 只能加载 Published 状态的 Experience Package。

## 九、v2.3 Builder Runtime

v2.3 将 Package Build System 落到主后端。

运行时模块：

```text
app/skill_training/package_builder.py
app/skill_training/package_validator.py
app/skill_training/package_manifest.py
app/services/experience_package_service.py
app/api/experience_packages.py
```

构建入口：

```text
POST /skills/{skill_id}/packages/build
```

构建前校验：

- skill 存在
- skill 已完成 evaluation
- validation_status = validated

v2.3 输出结构：

```text
Lawyer-AI-Platform-App/experience-packages/{package_id}/
├── package.json
├── skill.json
├── prompts/
│   ├── fact_prompt.txt
│   ├── analysis_prompt.txt
│   └── report_prompt.txt
├── templates/
│   └── report_template.md
└── tests/
    └── test_case.json
```

package.json 包含：

- package_id
- skill_id
- name
- domain
- version
- status
- entrypoints
- validation

v2.3 的 status 为 built。

built 不是 Published。

后续仍需 Package Registry、发布审批和 Workspace 加载策略。
