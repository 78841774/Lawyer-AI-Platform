# Skill Optimization Workflow（技能优化流程）

## 一、定位

SkillOpt Workflow 是律师 AI 平台训练系统中的技能优化流程，用于生成高质量、可复用的 Skill。

目标：

- 提升 Skill 的准确性和可交付性
- 形成标准化训练方法，便于能力复用
- 不绑定平台特定算法，实现参考性训练流程

---

## 二、总体流程

Candidate Skill 生成

↓

Skill 测试与评分

↓

优化策略选择

↓

Skill 修正与再训练

↓

Gate 验证

↓

EP 构建

---

## 三、Candidate Skill 生成

- 由 Training Pipeline 生成初步 Skill
- 包含 Fact Skill、Legal Skill、Strategy Skill、Report Skill
- 输出 Candidate Skill Pool

---

## 四、Skill 测试与评分

- 使用历史案件和验证案例进行测试
- 评估指标：
  - 准确性
  - 完整性
  - 一致性
  - 可复用性
- 输出 Skill Score

---

## 五、优化策略选择

- 根据评分结果选择优化策略：
  - 数据增强
  - 模板优化
  - Prompt 调整
  - 规则修正
- 输出优化方案

---

## 六、Skill 修正与再训练

- 应用优化方案修正 Candidate Skill
- 重新训练 Skill
- 更新 Skill Score

---

## 七、Gate 验证

- 所有优化后的 Skill 必须通过 Gate 验证
- 验证内容：
  - 完整性
  - 可交付性
  - 适用性
- 验证失败的 Skill 返回再训练阶段

---

## 八、EP 构建

- 通过 Gate 验证的 Skill 封装到 Experience Package
- EP 包含：
  - Skills
  - Gates
  - Metadata
- 发布至 Experience Registry，供 Workspace 使用

---

## 九、原则

- SkillOpt Workflow 参考 Microsoft SkillOpt 思路
- 平台保持算法独立性，不绑定具体优化方法
- 保持训练闭环：反馈 → 优化 → 验证 → 发布

