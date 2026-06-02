# Training Pipeline 训练流水线规范

## 一、定位

Training Pipeline 是律师 AI 平台的能力生产流水线。

目标：

将案件材料、律师经验、裁判规则转化为可部署的 Experience Package。

---

## 二、总体流程

案件样本

↓

事实提炼

↓

法律分析

↓

策略总结

↓

Skill 生成

↓

Gate 验证

↓

Experience Package 构建

↓

发布

---

## 三、输入

### 案件材料

包括：

- 起诉状
- 答辩状
- 证据材料
- 判决书
- 庭审笔录
- 律师意见

### 律师经验

包括：

- 办案思路
- 成败原因
- 关键证据
- 诉讼策略
- 风险控制

### 裁判规则

包括：

- 法条
- 司法解释
- 指导案例
- 类案裁判规则

---

## 四、事实训练阶段

目标：

训练 Fact Skill。

任务：

- 主体识别
- 时间线抽取
- 事实链构建
- 证据映射
- 缺失事实识别

输出：

Fact Skill Candidate

Fact Gate Candidate

---

## 五、法律训练阶段

目标：

训练 Legal Skill。

任务：

- 法律关系识别
- 争议焦点识别
- 法条匹配
- 裁判规则匹配
- 风险识别

输出：

Legal Skill Candidate

Legal Gate Candidate

---

## 六、策略训练阶段

目标：

训练 Strategy Skill。

任务：

- 原告策略
- 被告策略
- 举证策略
- 调解策略
- 执行策略

输出：

Strategy Skill Candidate

Strategy Gate Candidate

---

## 七、报告训练阶段

目标：

训练 Report Skill。

任务：

- 事实报告
- 法律分析报告
- 诉讼策略报告
- 客户交付报告

输出：

Report Skill Candidate

Report Gate Candidate

---

## 八、Gate 验证阶段

每个候选 Skill 必须通过 Gate 验证。

验证内容：

- 完整性
- 准确性
- 一致性
- 可交付性

验证不通过：

返回训练阶段继续优化。

---

## 九、Experience Package 构建阶段

通过验证的 Skill 与 Gate 被封装为 EP。

EP 包含：

- Skills
- Gates
- Knowledge
- Schemas
- Templates
- Metadata

---

## 十、发布阶段

EP 发布至 Experience Registry。

Workspace 只能加载已发布 EP。

未发布 EP 不得进入生产系统。

---

## 十一、反馈闭环

Workspace 运行产生：

- Gate 评分
- 用户反馈
- 律师修改记录
- 失败案例
- 补充材料记录

这些反馈进入下一轮训练。

---

## 十二、平台原则

训练系统负责能力生产。

生产系统负责能力消费。

Training Pipeline 是二者之间的经验生产线。
