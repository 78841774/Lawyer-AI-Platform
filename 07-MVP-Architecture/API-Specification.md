# API Specification

API Specification 定义 Lawyer AI Platform v0.4 MVP REST API 草案。

接口使用 REST/JSON 风格，统一使用 /api/v1 版本前缀。所有写操作应记录 request_id，并在必要时支持 Idempotency-Key。

## 通用响应字段

成功响应建议包含：

```json
{
  "request_id": "req_20260603_0001",
  "data": {}
}
```

错误响应建议包含：

```json
{
  "request_id": "req_20260603_0001",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数不符合要求",
    "details": {}
  }
}
```

## Case API

### POST /api/v1/cases

创建案件。

请求：

```json
{
  "title": "软件开发合同纠纷",
  "case_type": "contract_dispute",
  "objective": "评估违约责任并生成法律分析报告",
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

响应：

```json
{
  "request_id": "req_0001",
  "data": {
    "case_id": "case_0001",
    "status": "created"
  }
}
```

### GET /api/v1/cases

查询案件列表。

查询参数：

* case_type
* status
* page
* page_size

### GET /api/v1/cases/{case_id}

查询案件详情。

## Material API

### POST /api/v1/cases/{case_id}/materials

上传或登记案件材料。

请求：

```json
{
  "name": "软件开发服务合同.pdf",
  "material_type": "contract",
  "content_type": "application/pdf",
  "storage_path": "cases/case_0001/materials/originals/mat_0001/contract.pdf"
}
```

响应：

```json
{
  "request_id": "req_0002",
  "data": {
    "material_id": "mat_0001",
    "parse_status": "pending"
  }
}
```

### GET /api/v1/cases/{case_id}/materials

查询案件材料列表。

### GET /api/v1/cases/{case_id}/materials/{material_id}

查询材料详情和解析状态。

## Fact API

### POST /api/v1/cases/{case_id}/facts/extract

触发事实提炼。

请求：

```json
{
  "material_ids": ["mat_0001"],
  "options": {
    "min_confidence": 0.7
  }
}
```

响应：

```json
{
  "request_id": "req_0003",
  "data": {
    "job_id": "job_fact_0001",
    "status": "running"
  }
}
```

### GET /api/v1/cases/{case_id}/facts

查询案件事实列表。

### PATCH /api/v1/cases/{case_id}/facts/{fact_id}

更新事实状态或人工修订内容。

请求：

```json
{
  "status": "verified",
  "description": "原告与被告签订软件开发服务合同，并约定第一阶段交付期限。"
}
```

## Legal API

### POST /api/v1/cases/{case_id}/legal/analyze

触发法律分析。

请求：

```json
{
  "fact_ids": ["fact_0001", "fact_0002"],
  "issues": ["被告逾期交付是否构成违约"]
}
```

响应：

```json
{
  "request_id": "req_0004",
  "data": {
    "job_id": "job_legal_0001",
    "status": "running"
  }
}
```

### GET /api/v1/cases/{case_id}/legal-analyses

查询法律分析列表。

### GET /api/v1/cases/{case_id}/legal-analyses/{analysis_id}

查询法律分析详情。

## Report API

### POST /api/v1/cases/{case_id}/reports/generate

生成报告。

请求：

```json
{
  "report_type": "legal_analysis_report",
  "source": {
    "fact_ids": ["fact_0001", "fact_0002"],
    "analysis_ids": ["analysis_0001"]
  }
}
```

响应：

```json
{
  "request_id": "req_0005",
  "data": {
    "job_id": "job_report_0001",
    "status": "running"
  }
}
```

### GET /api/v1/cases/{case_id}/reports

查询报告列表。

### GET /api/v1/cases/{case_id}/reports/{report_id}

查询报告详情。

## Experience Package API

### GET /api/v1/experience-packages

查询可用经验包列表。

查询参数：

* case_type
* status

### GET /api/v1/experience-packages/{package_id}

查询经验包详情。

## Job API

### GET /api/v1/jobs/{job_id}

查询异步任务状态。

响应：

```json
{
  "request_id": "req_0006",
  "data": {
    "job_id": "job_fact_0001",
    "job_type": "fact_extraction",
    "status": "succeeded",
    "output_ref": "cases/case_0001/ai-results/facts/job_fact_0001/result.json"
  }
}
```
