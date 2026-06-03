# Real Case Intake Test Plan

## 1. 测试目的

验证 AIHome.law v3.4-C 的真实案件录入闭环：

```text
Real Case Intake
-> Folder-aware Material Upload
-> Intake Status
-> Fact Extraction
-> Legal Analysis
-> Report Generation
-> Runtime Trace
-> source_refs / material path context
-> Report Detail Review
```

本测试仅使用脱敏样本，不使用真实客户、真实合同或真实案件材料。

## 2. 测试案件字段

```json
{
  "title": "v3.4-C 真实案件录入闭环测试",
  "case_type": "contract_dispute",
  "description": "用于验证真实案件录入、文件夹材料上传、事实抽取、法律分析和报告生成闭环的脱敏样本。",
  "jurisdiction": "CN",
  "client_name": "测试客户A",
  "opposing_party": "测试相对方B",
  "priority": "normal",
  "tags": ["合同", "付款争议", "v3.4-C"]
}
```

## 3. 测试文件夹结构

```text
测试案件材料/
├── 01_合同/
│   └── 采购合同.txt
├── 02_履行/
│   └── 送货记录.txt
├── 03_付款/
│   └── 付款记录.txt
└── 04_沟通/
    └── 微信沟通记录.txt
```

## 4. API 验证步骤

1. `POST /auth/login` 获取 JWT。
2. `POST /cases` 创建测试案件。
3. `GET /cases/{case_id}/intake/status` 验证无材料状态。
4. `POST /cases/{case_id}/materials/batch` 上传临时 txt 样本。
5. `GET /cases/{case_id}/materials` 验证 `relative_path`、`folder_path`、`original_filename`。
6. `POST /cases/{case_id}/facts/extract` 抽取事实。
7. `GET /cases/{case_id}/facts` 验证 `source_refs.material_id`、`source_refs.filename`、`source_refs.relative_path`。
8. `POST /cases/{case_id}/analysis/run` 运行法律分析。
9. `POST /cases/{case_id}/reports/generate` 生成报告。
10. `GET /cases/{case_id}/intake/status` 验证下一步建议为 `review_report`。

可直接运行：

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
python scripts/validate_real_case_intake_v3_4.py
```

## 5. 浏览器验证步骤

1. 打开 `http://localhost:3001`。
2. 本地登录。
3. 创建 v3.4-C 测试案件。
4. 打开案件详情。
5. 上传测试文件夹。
6. 确认材料中心按目录分组显示。
7. 确认 Intake 状态卡片显示下一步建议。
8. 依次运行事实抽取、法律分析、报告生成。
9. 查看 Report Detail 的 `source_refs` 与运行信息。
10. 打开 Runtime / Reports / Skills / Experience Packages / Skill Registry，确认不白屏。

## 6. 预期结果

* 新案件无材料时：`next_recommended_action = upload_material`。
* 上传材料后：`next_recommended_action = extract_facts`。
* 抽取事实后：`next_recommended_action = run_analysis`。
* 运行法律分析后：`next_recommended_action = generate_report`。
* 生成报告后：`next_recommended_action = review_report`。
* 材料返回保留 `relative_path` 和 `folder_path`。
* 事实抽取返回包含材料 path context。
* 页面没有 401 / 403 / 500。

## 7. 敏感信息注意事项

不要在测试文档、模板、脚本或仓库中放入：

* 真实客户名称。
* 身份证号、电话、地址。
* 银行账号。
* 真实合同编号。
* 真实聊天记录。
* 真实案件材料。
* API Key 或 `.env`。

真实测试材料应先脱敏，并放在被 `.gitignore` 排除的目录中。
