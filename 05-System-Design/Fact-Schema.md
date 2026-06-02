# Fact Schema

Fact Schema 用于描述 Workspace System 在案件处理中识别、抽取、校验和沉淀的案件事实。

案件事实是 Legal Layer 进行法律分析、风险判断和文书生成的基础输入。事实必须可追溯、可验证、可被 Legal Layer 引用，不得以无法定位来源的自由文本直接参与法律结论生成。

## 字段定义

* fact_id：事实唯一标识。
* case_id：所属案件唯一标识。
* description：事实描述，应使用清晰、客观、可核验的表达。
* fact_type：事实类型，例如 identity、timeline、contract、payment、breach、damage、procedure。
* source_materials：事实来源材料列表，记录材料 ID、页码、段落、摘录等来源信息。
* evidence_refs：关联证据引用列表，记录证据编号、证据名称、证明目的等。
* time：事实发生、持续或被确认的时间信息。
* parties：事实涉及的当事人、第三人或其他主体。
* confidence：事实可信度，建议取值 0 到 1。
* status：事实状态，例如 extracted、verified、disputed、rejected。
* created_at：事实创建时间，使用 ISO 8601 格式。
* updated_at：事实更新时间，使用 ISO 8601 格式。

## 设计原则

* 可追溯：每一项事实必须能够定位到来源材料或证据。
* 可验证：事实应支持人工复核、证据比对和争议标记。
* 可引用：Legal Layer 只能通过 fact_id 或 related_facts 引用事实。
* 可演进：事实状态、可信度和来源引用应允许随案件推进更新。

## JSON 示例

```json
{
  "fact_id": "fact_20260603_0001",
  "case_id": "case_20260603_0001",
  "description": "原告与被告于 2024 年 3 月 18 日签订《软件开发服务合同》，约定被告应在 2024 年 6 月 30 日前交付第一阶段开发成果。",
  "fact_type": "contract",
  "source_materials": [
    {
      "material_id": "mat_0001",
      "name": "软件开发服务合同.pdf",
      "page": 2,
      "paragraph": "第二条 服务内容与交付期限",
      "excerpt": "乙方应于 2024 年 6 月 30 日前完成第一阶段开发成果交付。"
    }
  ],
  "evidence_refs": [
    {
      "evidence_id": "ev_0001",
      "evidence_no": "证据一",
      "name": "软件开发服务合同",
      "purpose": "证明双方存在合同关系及第一阶段交付期限"
    }
  ],
  "time": {
    "occurred_at": "2024-03-18",
    "deadline_at": "2024-06-30"
  },
  "parties": [
    {
      "party_id": "party_plaintiff",
      "role": "plaintiff",
      "name": "甲方科技有限公司"
    },
    {
      "party_id": "party_defendant",
      "role": "defendant",
      "name": "乙方软件有限公司"
    }
  ],
  "confidence": 0.94,
  "status": "verified",
  "created_at": "2026-06-03T10:00:00+08:00",
  "updated_at": "2026-06-03T10:20:00+08:00"
}
```
