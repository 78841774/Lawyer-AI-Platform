# Skill Schema

Skill Schema 定义 Skill Candidate 与 Experience Package 中技能对象的标准结构。

本规范用于保证技能可以被训练、评估、版本管理和发布。

## 一、Schema 总览

```json
{
  "skill_id": "contract-dispute-cn-v1",
  "skill_name": "Contract Dispute Skill",
  "domain": "contract_dispute",
  "jurisdiction": "CN",
  "version": "v1",
  "prompts": {},
  "templates": {},
  "evaluation_metrics": {},
  "metadata": {}
}
```

## 二、字段定义

### skill_id

技能唯一标识。

要求：

- 全平台唯一
- 使用小写字母、数字和连字符
- 应包含领域、法域和版本信息

示例：

```text
contract-dispute-cn-v1
labor-dispute-cn-v1
loan-dispute-cn-v2
```

### skill_name

技能展示名称。

要求：

- 可读
- 能说明技能处理的案件类型或任务范围
- 不用于程序路由

示例：

```text
Contract Dispute Skill
民间借贷纠纷分析技能
劳动争议审查技能
```

### domain

技能适用领域。

domain 用于区分案件类型、业务场景或法律任务。

示例：

```text
contract_dispute
loan_dispute
labor_dispute
corporate_dispute
construction_dispute
```

### jurisdiction

技能适用法域。

示例：

```text
CN
US-CA
US-NY
EU
```

要求：

- 必须明确法域
- 不允许使用模糊值
- 跨法域技能必须拆分为多个技能或在 metadata 中声明边界

### version

技能版本。

使用语义化业务版本：

```text
v1
v1.1
v2
```

版本策略见 Skill-Versioning.md。

### prompts

prompts 定义技能运行所需的提示词集合。

标准结构：

```json
{
  "fact_prompt": {
    "path": "fact_prompt.txt",
    "purpose": "extract structured fact pattern",
    "input": ["case_materials", "evidence_list"],
    "output": "fact_pattern"
  },
  "analysis_prompt": {
    "path": "analysis_prompt.txt",
    "purpose": "perform legal reasoning",
    "input": ["fact_pattern", "legal_basis"],
    "output": "legal_analysis"
  },
  "report_prompt": {
    "path": "report_prompt.txt",
    "purpose": "generate lawyer-facing report",
    "input": ["fact_pattern", "legal_analysis", "templates"],
    "output": "final_report"
  }
}
```

要求：

- 每个 prompt 必须声明输入、输出和用途
- prompt 不得依赖未声明的外部材料
- prompt 必须与测试样本绑定

### templates

templates 定义技能生成交付成果时使用的文档模板。

标准结构：

```json
{
  "fact_report": {
    "path": "templates/fact_report.md",
    "purpose": "事实梳理报告"
  },
  "legal_analysis": {
    "path": "templates/legal_analysis.md",
    "purpose": "法律分析报告"
  },
  "client_report": {
    "path": "templates/client_report.md",
    "purpose": "客户交付报告"
  }
}
```

要求：

- 模板必须具有明确用途
- 模板字段必须能被 report_prompt 调用
- 模板不得与具体案件强绑定

### evaluation_metrics

evaluation_metrics 定义技能评估指标和阈值。

标准结构：

```json
{
  "accuracy": {
    "weight": 0.30,
    "pass_threshold": 0.85
  },
  "consistency": {
    "weight": 0.20,
    "pass_threshold": 0.80
  },
  "completeness": {
    "weight": 0.20,
    "pass_threshold": 0.80
  },
  "legal_relevance": {
    "weight": 0.20,
    "pass_threshold": 0.85
  },
  "report_quality": {
    "weight": 0.10,
    "pass_threshold": 0.80
  }
}
```

要求：

- 所有权重之和必须等于 1.00
- 每个指标必须有 pass_threshold
- 评估结果必须写入 metadata

### metadata

metadata 定义技能的追溯信息、训练来源和发布状态。

标准结构：

```json
{
  "created_by": "Skill Factory",
  "created_at": "2026-06-03",
  "updated_at": "2026-06-03",
  "source_case_count": 25,
  "source_case_type": ["contract_dispute"],
  "training_notes": "Built from contract formation, breach, damages, and defense patterns.",
  "lifecycle_status": "Draft",
  "evaluation_summary": {
    "overall_score": 0.88,
    "passed": true
  },
  "compatible_with": ["v1"],
  "deprecated": false
}
```

要求：

- 必须记录来源样本数量
- 必须记录生命周期状态
- 必须记录最近一次评估结果
- 发布后 metadata 不得被随意修改，更新必须进入新版本

## 三、完整示例

```json
{
  "skill_id": "contract-dispute-cn-v1",
  "skill_name": "Contract Dispute Skill",
  "domain": "contract_dispute",
  "jurisdiction": "CN",
  "version": "v1",
  "prompts": {
    "fact_prompt": {
      "path": "fact_prompt.txt",
      "purpose": "extract contract dispute fact pattern",
      "input": ["case_materials", "evidence_list"],
      "output": "fact_pattern"
    },
    "analysis_prompt": {
      "path": "analysis_prompt.txt",
      "purpose": "analyze contract formation, performance, breach, defenses, and damages",
      "input": ["fact_pattern", "legal_basis"],
      "output": "legal_analysis"
    },
    "report_prompt": {
      "path": "report_prompt.txt",
      "purpose": "generate contract dispute lawyer report",
      "input": ["fact_pattern", "legal_analysis", "templates"],
      "output": "final_report"
    }
  },
  "templates": {
    "fact_report": {
      "path": "templates/fact_report.md",
      "purpose": "事实梳理报告"
    },
    "legal_analysis": {
      "path": "templates/legal_analysis.md",
      "purpose": "法律分析报告"
    },
    "client_report": {
      "path": "templates/client_report.md",
      "purpose": "客户交付报告"
    }
  },
  "evaluation_metrics": {
    "accuracy": {"weight": 0.30, "pass_threshold": 0.85},
    "consistency": {"weight": 0.20, "pass_threshold": 0.80},
    "completeness": {"weight": 0.20, "pass_threshold": 0.80},
    "legal_relevance": {"weight": 0.20, "pass_threshold": 0.85},
    "report_quality": {"weight": 0.10, "pass_threshold": 0.80}
  },
  "metadata": {
    "created_by": "Skill Factory",
    "created_at": "2026-06-03",
    "source_case_count": 25,
    "source_case_type": ["contract_dispute"],
    "lifecycle_status": "Draft",
    "deprecated": false
  }
}
```

