# Legal Reasoning Schema

Legal Reasoning Schema 用于描述 Legal Layer 在案件分析中形成的争点、规则、推理链、结论和风险判断。

法律分析必须基于 Fact Schema。Legal Layer 不得脱离已抽取、已引用或可追溯的案件事实直接生成结论。所有法律结论都应通过 related_facts 关联事实，通过 legal_rules 和 citations 关联法律规则、裁判规则或检索依据。

## 字段定义

* issue_id：法律争点唯一标识。
* case_id：所属案件唯一标识。
* issue：待分析的法律争点。
* related_facts：关联事实 ID 列表，应引用 Fact Schema 中的 fact_id。
* legal_rules：适用的法律规则、司法解释、合同规则或裁判规则。
* reasoning_chain：法律推理链，记录从事实到规则再到结论的分析步骤。
* conclusion：针对争点形成的初步结论。
* risk_level：风险等级，例如 low、medium、high、critical。
* citations：引用来源，包括法条、案例、合同条款、证据或内部知识引用。
* confidence：法律分析可信度，建议取值 0 到 1。

## 设计原则

* 事实先行：每个 issue 的分析必须引用 related_facts。
* 规则明确：每项结论应标明依据的 legal_rules 或 citations。
* 推理可审查：reasoning_chain 应保留关键分析步骤，便于律师复核。
* 风险可表达：risk_level 用于辅助策略判断和 Gate System 审核。
* 置信度可调整：confidence 应随事实补充、证据变化和人工复核更新。

## JSON 示例

```json
{
  "issue_id": "issue_20260603_0001",
  "case_id": "case_20260603_0001",
  "issue": "被告未按期交付第一阶段开发成果是否构成违约",
  "related_facts": [
    "fact_20260603_0001",
    "fact_20260603_0002",
    "fact_20260603_0003"
  ],
  "legal_rules": [
    {
      "rule_id": "rule_contract_performance",
      "type": "law",
      "name": "民法典合同编关于合同履行和违约责任的规则",
      "summary": "当事人应当按照约定履行合同义务，未按约定履行的，应承担相应违约责任。"
    },
    {
      "rule_id": "rule_contract_clause_8",
      "type": "contract_clause",
      "name": "《软件开发服务合同》第八条",
      "summary": "乙方逾期交付超过 15 日的，甲方有权要求违约金并保留解除合同的权利。"
    }
  ],
  "reasoning_chain": [
    {
      "step": 1,
      "type": "fact",
      "content": "合同约定第一阶段交付期限为 2024 年 6 月 30 日。",
      "fact_refs": ["fact_20260603_0001"]
    },
    {
      "step": 2,
      "type": "fact",
      "content": "现有材料显示被告至 2024 年 7 月 20 日仍未完成交付。",
      "fact_refs": ["fact_20260603_0002"]
    },
    {
      "step": 3,
      "type": "rule_application",
      "content": "被告未在约定期限内履行交付义务，且暂无有效免责事实，具备违约构成要件。"
    }
  ],
  "conclusion": "在现有事实和证据基础上，被告逾期交付第一阶段开发成果构成违约的可能性较高。",
  "risk_level": "medium",
  "citations": [
    {
      "citation_id": "cit_0001",
      "type": "law",
      "title": "中华人民共和国民法典",
      "reference": "合同履行与违约责任相关条款"
    },
    {
      "citation_id": "cit_0002",
      "type": "contract",
      "title": "软件开发服务合同",
      "reference": "第八条 违约责任"
    }
  ],
  "confidence": 0.86
}
```
