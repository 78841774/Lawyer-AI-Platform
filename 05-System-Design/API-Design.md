# API Design

API Design 定义 Lawyer AI Platform v0.2 模块 API 的基础设计原则和 v1 接口草案。

## 设计原则

* REST/JSON 风格：接口使用资源化路径， 请求和响应主体使用 JSON。
* 版本号：所有接口路径包含版本号，例如 /api/v1。
* 错误结构：错误响应使用统一 code、message、details、request_id 结构。
* 请求 ID：每次请求应生成或透传 request_id，用于日志关联和问题排查。
* 幂等性：创建、上传、生成类接口应支持 idempotency_key，避免重复提交导致重复资源。
* 审计日志：关键操作应记录 actor、case_id、request_id、input_ref、output_ref、created_at。

## 通用错误结构

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数不符合接口要求",
    "details": {
      "field": "case_type",
      "reason": "case_type 不能为空"
    },
    "request_id": "req_20260603_0001"
  }
}
```

## 通用请求头

```text
X-Request-Id: req_20260603_0001
Idempotency-Key: idem_20260603_0001
```

## 接口草案

### POST /api/v1/cases

创建案件。

请求示例：

```json
{
  "case_type": "contract_dispute",
  "title": "软件开发服务合同纠纷",
  "parties": [
    {
      "role": "plaintiff",
      "name": "甲方科技有限公司"
    },
    {
      "role": "defendant",
      "name": "乙方软件有限公司"
    }
  ],
  "experience_package_id": "exp_contract_dispute_v0_2"
}
```

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "status": "created",
  "request_id": "req_20260603_0001"
}
```

### POST /api/v1/cases/{case_id}/materials

上传或登记案件材料。

请求示例：

```json
{
  "materials": [
    {
      "name": "软件开发服务合同.pdf",
      "content_type": "application/pdf",
      "storage_ref": "oss://lawyer-ai/cases/case_20260603_0001/materials/contract.pdf"
    }
  ]
}
```

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "material_ids": ["mat_0001"],
  "status": "accepted",
  "request_id": "req_20260603_0002"
}
```

### POST /api/v1/cases/{case_id}/facts/extract

触发案件事实抽取。

请求示例：

```json
{
  "material_ids": ["mat_0001"],
  "options": {
    "require_evidence_refs": true,
    "min_confidence": 0.7
  }
}
```

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "job_id": "job_fact_extract_0001",
  "status": "running",
  "request_id": "req_20260603_0003"
}
```

### POST /api/v1/cases/{case_id}/legal/analyze

基于 Fact Schema 触发法律分析。

请求示例：

```json
{
  "fact_ids": [
    "fact_20260603_0001",
    "fact_20260603_0002"
  ],
  "issues": [
    "被告未按期交付是否构成违约"
  ]
}
```

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "job_id": "job_legal_analyze_0001",
  "status": "running",
  "request_id": "req_20260603_0004"
}
```

### POST /api/v1/cases/{case_id}/reports/generate

生成案件报告或法律文书。

请求示例：

```json
{
  "report_type": "legal_analysis_report",
  "template_id": "tpl_legal_analysis_report",
  "include_gate_results": true
}
```

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "job_id": "job_report_generate_0001",
  "status": "running",
  "request_id": "req_20260603_0005"
}
```

### GET /api/v1/cases/{case_id}/gate-results

查询案件 Gate 检查结果。

响应示例：

```json
{
  "case_id": "case_20260603_0001",
  "gate_results": [
    {
      "gate_id": "gate_fact_completeness",
      "name": "事实完整性检查",
      "status": "passed",
      "checked_at": "2026-06-03T10:30:00+08:00"
    },
    {
      "gate_id": "gate_legal_citation",
      "name": "法律依据引用检查",
      "status": "passed",
      "checked_at": "2026-06-03T10:40:00+08:00"
    }
  ],
  "request_id": "req_20260603_0006"
}
```
