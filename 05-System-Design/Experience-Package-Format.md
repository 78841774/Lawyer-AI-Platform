# Experience Package Format

Experience Package 是 Lawyer AI Platform 中承载律师经验、办案流程、技能配置、Gate 规则、数据结构和模板资源的标准化能力包。

Training System 负责生产 Experience Package。Workspace System 负责加载 Experience Package，并在案件运行时根据包内配置调度事实抽取、法律分析、策略生成、文书生成和质量门禁。

## 字段定义

* package_id：经验包唯一标识。
* name：经验包名称。
* version：经验包版本号。
* case_type：适用案件类型，例如 contract_dispute、labor_dispute、loan_dispute。
* skills：经验包内包含的技能定义或技能引用。
* gates：质量门禁定义，包括事实完整性、法律依据、证据引用、文书质量等检查项。
* schemas：经验包使用的数据结构引用，例如 Fact Schema、Legal Reasoning Schema。
* templates：文书、报告、提示词或分析输出模板。
* knowledge_refs：外部知识库、法律库、案例库或内部知识引用。
* runtime_config：运行时加载、调度、超时、日志和模型策略配置。
* created_by：经验包创建者或生产系统标识。
* created_at：创建时间，使用 ISO 8601 格式。

## 目录结构示例

```text
experience-packages/
  contract-dispute-v0.2/
    package.json
    schemas/
      fact.schema.json
      legal-reasoning.schema.json
    skills/
      fact-extraction.md
      legal-analysis.md
      strategy-generation.md
    gates/
      fact-completeness.json
      legal-citation-check.json
      report-quality-check.json
    templates/
      legal-analysis-report.md
      litigation-strategy.md
      complaint-draft.md
    knowledge_refs/
      laws.json
      cases.json
    runtime/
      config.json
```

## package.json 示例

```json
{
  "package_id": "exp_contract_dispute_v0_2",
  "name": "合同纠纷办案经验包",
  "version": "0.2.0",
  "case_type": "contract_dispute",
  "skills": [
    {
      "skill_id": "skill_fact_extraction",
      "name": "合同纠纷事实抽取",
      "entry": "skills/fact-extraction.md"
    },
    {
      "skill_id": "skill_legal_analysis",
      "name": "合同违约法律分析",
      "entry": "skills/legal-analysis.md"
    }
  ],
  "gates": [
    {
      "gate_id": "gate_fact_completeness",
      "name": "事实完整性检查",
      "config": "gates/fact-completeness.json"
    },
    {
      "gate_id": "gate_legal_citation",
      "name": "法律依据引用检查",
      "config": "gates/legal-citation-check.json"
    }
  ],
  "schemas": {
    "fact": "schemas/fact.schema.json",
    "legal_reasoning": "schemas/legal-reasoning.schema.json"
  },
  "templates": [
    {
      "template_id": "tpl_legal_analysis_report",
      "name": "法律分析报告模板",
      "path": "templates/legal-analysis-report.md"
    }
  ],
  "knowledge_refs": [
    {
      "ref_id": "kb_contract_laws",
      "type": "law",
      "path": "knowledge_refs/laws.json"
    },
    {
      "ref_id": "kb_contract_cases",
      "type": "case",
      "path": "knowledge_refs/cases.json"
    }
  ],
  "runtime_config": {
    "loader": "workspace-runtime",
    "max_execution_seconds": 180,
    "enable_audit_log": true,
    "required_gates": [
      "gate_fact_completeness",
      "gate_legal_citation"
    ]
  },
  "created_by": "training-system",
  "created_at": "2026-06-03T10:00:00+08:00"
}
```
