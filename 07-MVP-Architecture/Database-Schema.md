# Database Schema

Database Schema 定义 Lawyer AI Platform v0.4 MVP 的核心数据表。

MVP 数据库建议使用 PostgreSQL。JSONB 字段用于保存结构化扩展数据，核心检索字段应独立成列并建立索引。

## cases

案件表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| case_id | varchar | 案件唯一标识 |
| title | varchar | 案件名称 |
| case_type | varchar | 案件类型 |
| status | varchar | 案件状态 |
| parties | jsonb | 当事人信息 |
| objective | text | 案件目标 |
| experience_package_id | varchar | 绑定经验包 ID |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(case_id)
* index(case_type)
* index(status)
* index(updated_at)

## materials

材料表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| material_id | varchar | 材料唯一标识 |
| case_id | varchar | 所属案件 |
| name | varchar | 材料名称 |
| material_type | varchar | 材料类型 |
| content_type | varchar | 文件类型 |
| storage_path | text | 原始文件路径 |
| text_path | text | 解析文本路径 |
| parse_status | varchar | 解析状态 |
| metadata | jsonb | 页数、大小、来源等扩展信息 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(material_id)
* index(case_id)
* index(parse_status)

## facts

事实表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| fact_id | varchar | 事实唯一标识 |
| case_id | varchar | 所属案件 |
| description | text | 事实描述 |
| fact_type | varchar | 事实类型 |
| source_materials | jsonb | 来源材料 |
| evidence_refs | jsonb | 证据引用 |
| occurred_at | timestamptz | 事实发生时间 |
| parties | jsonb | 涉及主体 |
| confidence | numeric | 可信度 |
| status | varchar | 事实状态 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(fact_id)
* index(case_id)
* index(fact_type)
* index(status)

## legal_analyses

法律分析表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| analysis_id | varchar | 分析唯一标识 |
| issue_id | varchar | 法律争点 ID |
| case_id | varchar | 所属案件 |
| issue | text | 法律争点 |
| related_facts | jsonb | 关联 fact_id 列表 |
| legal_rules | jsonb | 法律规则 |
| reasoning_chain | jsonb | 推理链 |
| conclusion | text | 结论 |
| risk_level | varchar | 风险等级 |
| citations | jsonb | 引用 |
| confidence | numeric | 可信度 |
| version | integer | 版本 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(analysis_id)
* index(case_id)
* index(issue_id)
* index(risk_level)

## reports

报告表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| report_id | varchar | 报告唯一标识 |
| case_id | varchar | 所属案件 |
| report_type | varchar | 报告类型 |
| title | varchar | 报告标题 |
| status | varchar | 生成状态 |
| version | integer | 版本 |
| storage_path | text | 报告文件路径 |
| source_refs | jsonb | 引用的 facts 和 legal_analyses |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(report_id)
* index(case_id)
* index(report_type)
* index(status)

## experience_packages

经验包表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| package_id | varchar | 经验包唯一标识 |
| name | varchar | 经验包名称 |
| version | varchar | 版本 |
| case_type | varchar | 适用案件类型 |
| manifest_path | text | package.json 路径 |
| status | varchar | 状态 |
| metadata | jsonb | skills、schemas、templates 摘要 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(package_id, version)
* index(case_type)
* index(status)

## jobs

异步任务表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| job_id | varchar | 任务唯一标识 |
| case_id | varchar | 所属案件 |
| job_type | varchar | 任务类型 |
| status | varchar | 任务状态 |
| input_ref | text | 输入引用 |
| output_ref | text | 输出引用 |
| error | jsonb | 错误信息 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

建议索引：

* unique(job_id)
* index(case_id)
* index(job_type)
* index(status)

## audit_logs

审计日志表。

| Field | Type | Description |
| --- | --- | --- |
| id | bigint | 主键 |
| audit_id | varchar | 审计日志 ID |
| request_id | varchar | 请求 ID |
| actor_id | varchar | 操作人或系统 |
| case_id | varchar | 所属案件 |
| action | varchar | 操作类型 |
| target_type | varchar | 对象类型 |
| target_id | varchar | 对象 ID |
| metadata | jsonb | 扩展信息 |
| created_at | timestamptz | 创建时间 |

建议索引：

* unique(audit_id)
* index(request_id)
* index(case_id)
* index(created_at)
