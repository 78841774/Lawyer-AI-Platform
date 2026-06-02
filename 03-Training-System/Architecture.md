# Training System Architecture

## 一、定位

Training System 是律师 AI 平台能力生产系统。

职责：

从案件中提炼经验。

将经验封装为 Experience Package。

持续优化平台能力。

Training System 不处理线上案件。

Training System 只负责生产能力。

---

## 二、系统目标

目标：

建立律师能力工厂。

实现：

案件

↓

经验

↓

经验包

↓

能力升级

↓

案件

的闭环。

---

## 三、核心架构

Training System 包含：

### Material Layer

训练材料层

---

### Fact Layer

事实抽取层

---

### Legal Layer

法律分析层

---

### Strategy Layer

策略层

---

### Skill Layer

技能构建层

---

### Gate Layer

质量验证层

---

### Package Layer

经验包生成层

---

## 四、训练流程

案件材料

↓

事实抽取

↓

法律分析

↓

策略提炼

↓

经验总结

↓

Skill生成

↓

Gate验证

↓

EP生成

↓

入库

---

## 五、训练材料来源

来源：

### 历史案件

律所案件

---

### 裁判文书

判决书

裁定书

调解书

---

### 法律意见

律师意见书

尽调报告

专项报告

---

### 优秀模板

起诉状

答辩状

代理词

法律意见书

---

## 六、训练原则

原则一：

真实案件优先。

原则二：

结果可验证。

原则三：

经验必须复用。

原则四：

能力必须量化。

---

## 七、经验提炼目标

训练系统不记录案件。

训练系统记录：

为什么赢

为什么输

如何优化

最佳策略

风险控制

---

## 八、Skill Factory

Skill Factory职责：

自动生成：

Fact Skill

Legal Skill

Strategy Skill

Draft Skill

Review Skill

---

## 九、Gate Factory

Gate Factory职责：

自动生成：

Fact Gate

Legal Gate

Strategy Gate

Report Gate

---

## 十、Experience Package Factory

负责：

自动封装：

Skill

Gate

Prompt

Workflow

Metadata

Version

形成标准EP。

---

## 十一、版本管理

经验包必须版本化。

示例：

EP-Contract-v1.0

EP-Contract-v1.1

EP-Contract-v2.0

---

## 十二、训练系统价值

Training System 本质：

把律师经验资产化。

把律师能力产品化。

把律师知识持续复利化。
