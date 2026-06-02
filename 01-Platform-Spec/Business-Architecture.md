Lawyer AI Platform 业务架构总纲

一、项目定位

Lawyer AI Platform 是面向律师行业的能力研发与案件生产一体化平台。

平台由两套独立但关联的系统组成：

1. 律师能力研发系统（Training System）
2. 案件分析生产系统（Workspace System）

两套系统相互独立运行，但通过统一标准实现成果流转。

⸻

二、平台总体架构

律师经验
    ↓
Training System
    ↓
Experience Package
    ↓
Workspace System
    ↓
案件分析成果

Experience Package 是两套系统之间唯一标准接口。

⸻

三、Training System定位

目标

将律师经验转化为可复用AI能力。

输入

* 律师经验
* 典型案例
* 裁判规则
* Skill
* Prompt

输出

Experience Package

职责

* Skill设计
* Skill训练
* Skill验证
* 经验沉淀
* 经验升级
* 版本管理

不负责

* 案件管理
* 案件分析
* 客户交付

⸻

四、Workspace System定位

目标

利用Experience Package完成案件分析与成果交付。

输入

* 案件材料
* Experience Package

输出

* 事实分析成果
* 法律分析成果
* 策略成果
* 文书成果

职责

* 案件管理
* 材料管理
* 事实提炼
* 法律分析
* 门控评价
* 成果输出

⸻

五、Experience Package定位

Experience Package（EP）是平台统一能力载体。

Training System只能输出EP。

Workspace System只能消费EP。

EP组成

* Skill
* Gate
* Prompt
* Knowledge
* Output Standard
* Version

⸻

六、平台核心原则

1. 法律分析是最终目标。
2. 事实提炼是法律分析基础。
3. 事实不完整不得进入正式法律分析。
4. 所有能力均来源于Experience Package。
5. 生产系统不得修改训练成果。
6. 训练系统不得直接介入案件生产。

⸻

七、双系统关系

独立

* 独立开发
* 独立部署
* 独立升级

统一

* 统一EP规范
* 统一版本体系
* 统一变更机制

⸻

八、变更治理

变更分为：

* A类：Training变更
* B类：Workspace变更
* C类：EP规范变更
* D类：平台架构变更

所有变更必须评估：

* Training影响
* Workspace影响
* EP影响
* 兼容性影响

⸻

九、长期目标

构建律师行业经验研发体系。

构建律师行业经验资产库。

构建律师案件智能分析生产体系。

实现经验持续沉淀、持续训练、持续生产、持续迭代。