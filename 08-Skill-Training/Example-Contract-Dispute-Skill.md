# Example: Contract Dispute Skill

本文件以 Contract Dispute Skill 为例，说明 Skill Factory 如何从合同纠纷案件沉淀技能并生成 Experience Package。

## 一、技能定位

```text
skill_id: contract-dispute-cn-v1
skill_name: Contract Dispute Skill
domain: contract_dispute
jurisdiction: CN
version: v1
```

适用范围：

- 买卖合同纠纷
- 服务合同纠纷
- 合同履行争议
- 合同解除争议
- 违约责任争议
- 损失赔偿争议

不适用范围：

- 劳动合同纠纷
- 金融借款合同纠纷
- 建设工程合同纠纷中的复杂工程量争议
- 涉外合同中的外国法适用

## 二、训练输入

Case 样本应包含：

- 合同文本
- 订单、报价单或补充协议
- 付款凭证
- 履行记录
- 催告函、通知函、律师函
- 沟通记录
- 发票或结算单
- 起诉状或答辩状
- 判决书或律师复盘

样本覆盖：

- 合同成立争议
- 合同效力争议
- 履行是否完成争议
- 迟延履行争议
- 拒绝履行争议
- 质量瑕疵争议
- 违约金调整争议
- 损失证明不足争议

## 三、Fact Pattern

合同纠纷事实模式：

```json
{
  "parties": [],
  "contract": {
    "formation": "",
    "effective_date": "",
    "main_obligations": [],
    "price_or_payment": "",
    "performance_period": ""
  },
  "performance": {
    "plaintiff_performance": [],
    "defendant_performance": [],
    "payment_records": [],
    "delivery_records": []
  },
  "breach": {
    "alleged_breach": [],
    "breach_date": "",
    "notice_or_demand": []
  },
  "defenses": [],
  "damages": {
    "claimed_amount": "",
    "calculation_basis": "",
    "supporting_evidence": []
  },
  "evidence_map": []
}
```

关键事实：

- 合同是否成立
- 合同是否有效
- 双方主要义务
- 哪一方先履行或应先履行
- 是否存在违约行为
- 是否存在抗辩事由
- 损失或违约金是否有依据
- 证据是否足以支持请求

## 四、Reasoning Pattern

合同纠纷推理路径：

```text
1. 确认合同关系
2. 判断合同效力
3. 识别双方主要义务
4. 判断履行情况
5. 判断违约行为
6. 分析抗辩理由
7. 计算损失或违约金
8. 评估证据风险
9. 形成诉讼或谈判建议
```

争议焦点示例：

- 双方是否存在有效合同关系
- 原告是否已履行主要义务
- 被告是否构成迟延付款或拒绝履行
- 被告提出的质量瑕疵抗辩是否成立
- 违约金是否过高需要调整
- 损失金额是否有充分证据支持

## 五、Prompt 示例

### fact_prompt.txt

目标：

从合同纠纷材料中抽取事实结构。

核心要求：

- 按主体、合同、履行、违约、抗辩、损失和证据映射输出
- 对没有证据支持的信息标记为待核实
- 对日期、金额和合同编号保持原文一致
- 不得自行补充材料中不存在的事实

### analysis_prompt.txt

目标：

基于事实结构完成合同纠纷法律分析。

核心要求：

- 先判断合同关系和合同效力
- 再分析履行与违约
- 分别列明原告主张路径和被告抗辩路径
- 对损失、违约金和证据风险单独分析
- 法律依据必须与争议焦点对应

### report_prompt.txt

目标：

生成律师审阅版合同纠纷分析报告。

核心要求：

- 先给出摘要和核心结论
- 再展开事实、争议焦点、法律分析和证据风险
- 明确胜诉风险、败诉风险和补充证据建议
- 报告语言应当审慎、专业、可交付

## 六、Template 示例

标准模板：

```text
templates/fact_report.md
templates/legal_analysis.md
templates/litigation_strategy.md
templates/client_report.md
```

client_report.md 章节：

```text
# 合同纠纷案件分析报告

## 一、案件摘要

## 二、核心结论

## 三、关键事实

## 四、争议焦点

## 五、法律分析

## 六、证据风险

## 七、诉讼策略

## 八、补充材料建议
```

## 七、Evaluation Metrics

默认评估配置：

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

合同纠纷重点扣分项：

- 遗漏合同效力判断
- 遗漏履行顺序分析
- 未区分违约责任和损害赔偿
- 未分析抗辩理由
- 错误处理违约金调整
- 虚构证据或法律依据

## 八、Experience Package 输出

```text
contract-dispute-cn-v1/
├── skill.json
├── fact_prompt.txt
├── analysis_prompt.txt
├── report_prompt.txt
├── templates/
│   ├── fact_report.md
│   ├── legal_analysis.md
│   ├── litigation_strategy.md
│   └── client_report.md
└── tests/
    ├── cases/
    ├── expected_outputs/
    ├── evaluation_report.json
    └── evaluation_summary.md
```

## 九、生命周期

初始状态：

```text
Draft
```

通过结构校验后：

```text
Candidate
```

通过评估和律师复核后：

```text
Validated
```

构建并发布后：

```text
Published
```

被 v1.1 或 v2 替代后：

```text
Deprecated
```

