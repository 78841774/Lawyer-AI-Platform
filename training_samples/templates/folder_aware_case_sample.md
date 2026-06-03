# Folder-Aware Case Sample Template

This template describes a sanitized local sample for v3.4-C validation.

Do not place real case materials in this directory.

## Case

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

## Folder Structure

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

## Example Sanitized File Notes

* `01_合同/采购合同.txt`: Describe generic delivery, acceptance, and payment terms.
* `02_履行/送货记录.txt`: Describe generic delivery and receipt status.
* `03_付款/付款记录.txt`: Describe generic partial payment and unpaid balance.
* `04_沟通/微信沟通记录.txt`: Describe generic payment follow-up communication.

Do not include real names, phone numbers, addresses, account numbers, contract numbers, or original evidence text.
