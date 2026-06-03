# Evaluation Framework

Evaluation Framework 定义 Skill Candidate 的质量评估指标、评分方法和发布门槛。

## 一、评估目标

评估的目标不是证明模型输出完美，而是确认技能是否达到律师可复核、平台可发布、客户交付可控的最低质量要求。

## 二、评估指标

### accuracy

accuracy 衡量输出内容是否准确。

评估内容：

- 事实提取是否准确
- 证据引用是否准确
- 法律关系识别是否准确
- 法条和裁判规则引用是否准确
- 结论是否与事实和法律依据一致

扣分情形：

- 将未证实事实写成确定事实
- 错误识别合同主体
- 错误适用法律
- 捏造证据、法条或裁判规则
- 结论与材料明显冲突

### consistency

consistency 衡量同一输入在多次运行或不同章节中的输出是否一致。

评估内容：

- 主体名称是否一致
- 金额、日期、合同编号是否一致
- 争议焦点前后是否一致
- 法律结论与风险提示是否一致
- 报告章节之间是否相互矛盾

扣分情形：

- 同一事实在不同章节表述冲突
- 同一金额出现多个版本且无说明
- 前文认定合同有效，后文又按合同无效分析
- 风险结论与分析过程不一致

### completeness

completeness 衡量输出是否覆盖案件处理所需的关键内容。

评估内容：

- 是否覆盖关键事实
- 是否覆盖主要证据
- 是否覆盖全部核心争议焦点
- 是否覆盖主要请求或抗辩
- 是否覆盖风险、缺失材料和补充建议

扣分情形：

- 遗漏核心合同或付款事实
- 遗漏主要抗辩理由
- 未说明关键证据缺口
- 未分析损失计算
- 报告结构缺章

### legal_relevance

legal_relevance 衡量输出是否聚焦法律问题，而非泛泛描述。

评估内容：

- 事实是否围绕法律要件组织
- 分析是否围绕请求、抗辩和裁判规则展开
- 法条引用是否与案件争议相关
- 风险提示是否具有法律可操作性
- 建议是否服务于诉讼、谈判或合规目标

扣分情形：

- 大量无关背景描述
- 法条引用与争议无关
- 分析没有对应请求或抗辩
- 结论缺乏法律评价
- 建议不可执行

### report_quality

report_quality 衡量报告是否具备律师审阅和客户交付价值。

评估内容：

- 结构是否清晰
- 语言是否专业
- 结论是否明确
- 风险分级是否可读
- 建议是否可操作
- 是否适合律师进一步修改

扣分情形：

- 章节混乱
- 大段重复
- 结论模糊
- 缺少摘要或重点提示
- 客户无法理解风险含义

## 三、评分机制

每个指标采用 0 到 1 分。

```text
0.00 - 0.39: 不合格
0.40 - 0.59: 较弱
0.60 - 0.74: 基本可用
0.75 - 0.84: 良好
0.85 - 1.00: 可发布
```

默认权重：

| Metric | Weight | Default Pass Threshold |
| --- | ---: | ---: |
| accuracy | 0.30 | 0.85 |
| consistency | 0.20 | 0.80 |
| completeness | 0.20 | 0.80 |
| legal_relevance | 0.20 | 0.85 |
| report_quality | 0.10 | 0.80 |

总体分计算：

```text
overall_score =
  accuracy * 0.30 +
  consistency * 0.20 +
  completeness * 0.20 +
  legal_relevance * 0.20 +
  report_quality * 0.10
```

## 四、通过规则

Skill Candidate 通过评估必须同时满足：

- overall_score >= 0.85
- accuracy >= 0.85
- legal_relevance >= 0.85
- consistency >= 0.80
- completeness >= 0.80
- report_quality >= 0.80
- 不存在严重法律错误
- 不存在虚构事实、证据、法条或案例

## 五、严重错误

出现严重错误时，无论 overall_score 多少，均不得发布。

严重错误包括：

- 虚构法律依据
- 虚构证据
- 错误识别诉讼主体并影响结论
- 错误适用核心法律规则
- 输出可能误导律师或客户作出重大决策
- 泄露训练案件敏感信息

## 六、评估流程

```text
Skill Candidate
  |
  v
Run Test Cases
  |
  v
Compare Expected Outputs
  |
  v
Lawyer Review
  |
  v
Metric Scoring
  |
  v
Pass / Return for Optimization
```

## 七、评估报告

评估报告必须包含：

- skill_id
- version
- test_case_count
- metric_scores
- overall_score
- pass_result
- failure_reasons
- severe_errors
- reviewer_notes
- recommended_next_action

示例：

```json
{
  "skill_id": "contract-dispute-cn-v1",
  "version": "v1",
  "test_case_count": 20,
  "metric_scores": {
    "accuracy": 0.88,
    "consistency": 0.84,
    "completeness": 0.86,
    "legal_relevance": 0.89,
    "report_quality": 0.83
  },
  "overall_score": 0.87,
  "pass_result": true,
  "severe_errors": [],
  "recommended_next_action": "Publish"
}
```

## 八、人工复核

所有技能发布前必须经过律师复核。

自动评分用于筛选和定位问题。

律师复核用于确认：

- 法律判断是否可靠
- 风险表达是否审慎
- 报告是否符合交付标准
- 是否存在职业责任风险

## 九、v2.2 Skill Evaluation Runtime

v2.2 引入轻量级 Skill Evaluation Runtime。

该 runtime 用于评估 Skill Candidate 草稿是否可以从 `candidate` 进入 `validated` 状态。

当前评估维度：

- fact_pattern_quality
- reasoning_quality
- prompt_quality
- template_quality
- legal_relevance
- report_reusability

每项评分范围：

```text
0.00 - 1.00
```

总分计算：

```text
average_score =
  (
    fact_pattern_quality +
    reasoning_quality +
    prompt_quality +
    template_quality +
    legal_relevance +
    report_reusability
  ) / 6
```

状态规则：

```text
average_score >= 0.75 -> validation_status = validated
average_score < 0.75  -> validation_status = needs_improvement
```

运行时接口：

```text
POST /skills/{skill_id}/evaluate
GET /skills/{skill_id}/evaluation
```

评估完成后写入：

- evaluation_score
- validation_status
- evaluation_details

并同步更新本地 Skill Package：

```text
Lawyer-AI-Platform-App/skills/{skill_id}/skill.json
```

v2.2 评估是规则评估，不替代律师复核。

正式发布前仍必须进入完整 Evaluation Framework 和人工审查。

## 十、数据库迁移说明

v2.2 为 `skills` 表增加：

- evaluation_details
- validation_status
- validated_at

本地 SQLite 开发环境使用启动时兼容补列方案。

后续生产环境应引入 Alembic migration 管理表结构升级。
