# Database Blueprint

Database Blueprint 定义 Lawyer AI Platform v0.3 的核心数据库表设计。

数据库负责保存案件执行过程中的结构化数据，包括案件、材料、事实、法律分析、Gate 结果、报告、经验包和审计日志。

## 表设计

### cases

保存案件基础信息。

建议字段：

* id：主键。
* case_id：案件唯一标识。
* title：案件名称。
* case_type：案件类型。
* status：案件状态。
* parties：当事人 JSON。
* owner_id：负责人 ID。
* experience_package_id：绑定经验包 ID。
* created_at：创建时间。
* updated_at：更新时间。

### materials

保存案件材料元数据。

建议字段：

* id：主键。
* material_id：材料唯一标识。
* case_id：所属案件 ID。
* name：材料名称。
* material_type：材料类型。
* evidence_no：证据编号。
* proof_purpose：证明目的。
* content_type：文件类型。
* storage_path：原始文件路径。
* ocr_path：OCR 结果路径。
* parse_status：解析状态。
* created_at：创建时间。
* updated_at：更新时间。

### facts

保存 Fact Schema。

建议字段：

* id：主键。
* fact_id：事实唯一标识。
* case_id：所属案件 ID。
* description：事实描述。
* fact_type：事实类型。
* source_materials：来源材料 JSON。
* evidence_refs：证据引用 JSON。
* time：时间信息 JSON。
* parties：主体信息 JSON。
* confidence：可信度。
* status：事实状态。
* created_at：创建时间。
* updated_at：更新时间。

### legal_analyses

保存 Legal Reasoning Schema。

建议字段：

* id：主键。
* issue_id：法律争点唯一标识。
* case_id：所属案件 ID。
* issue：法律争点。
* related_facts：关联事实 ID JSON。
* legal_rules：法律规则 JSON。
* reasoning_chain：推理链 JSON。
* conclusion：分析结论。
* risk_level：风险等级。
* citations：引用 JSON。
* confidence：可信度。
* version：分析版本。
* created_at：创建时间。
* updated_at：更新时间。

### gate_results

保存门控检查结果。

建议字段：

* id：主键。
* gate_result_id：Gate 结果唯一标识。
* case_id：所属案件 ID。
* gate_id：Gate 唯一标识。
* name：Gate 名称。
* target_type：检查对象类型，例如 fact、legal_analysis、report。
* target_id：检查对象 ID。
* status：检查状态，例如 passed、failed、warning。
* findings：问题项 JSON。
* checked_at：检查时间。
* created_at：创建时间。

### reports

保存报告和文书记录。

建议字段：

* id：主键。
* report_id：报告唯一标识。
* case_id：所属案件 ID。
* report_type：报告类型。
* template_id：模板 ID。
* status：生成状态。
* version：报告版本。
* storage_path：报告文件路径。
* gate_status：报告 Gate 状态。
* created_at：创建时间。
* updated_at：更新时间。

### experience_packages

保存经验包元数据。

建议字段：

* id：主键。
* package_id：经验包唯一标识。
* name：经验包名称。
* version：版本号。
* case_type：适用案件类型。
* manifest_path：package.json 存储路径。
* status：可用状态。
* created_by：创建者。
* created_at：创建时间。
* updated_at：更新时间。

### audit_logs

保存审计日志。

建议字段：

* id：主键。
* audit_id：审计日志唯一标识。
* request_id：请求 ID。
* actor_id：操作人或系统 ID。
* case_id：关联案件 ID。
* action：操作类型。
* target_type：操作对象类型。
* target_id：操作对象 ID。
* input_ref：输入引用。
* output_ref：输出引用。
* metadata：扩展信息 JSON。
* created_at：创建时间。

## 索引建议

* cases：case_id、case_type、status、updated_at。
* materials：case_id、material_id、parse_status。
* facts：case_id、fact_id、fact_type、status。
* legal_analyses：case_id、issue_id、risk_level、version。
* gate_results：case_id、gate_id、target_type、target_id、status。
* reports：case_id、report_id、report_type、version。
* experience_packages：package_id、case_type、version、status。
* audit_logs：case_id、request_id、actor_id、created_at。
