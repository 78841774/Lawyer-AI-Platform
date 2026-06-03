Experience Package（经验包）规范

一、定位

Experience Package（EP）是律师能力的标准化封装。

平台中：

Training System 不直接服务案件。

Workspace System 不直接训练能力。

二者通过 Experience Package 连接。

因此：

EP 是平台唯一能力交换标准。

⸻

二、目标

实现：

律师经验

↓

结构化能力

↓

标准化封装

↓

快速部署

↓

持续迭代

⸻

三、经验包组成

每个经验包包含：

1 Skill

能力模块

例如：

ConstructionContractSkill

LaborDisputeSkill

DivorceSkill

LoanDisputeSkill

⸻

2 Prompt

推理提示

包括：

事实提取提示

法律分析提示

策略分析提示

报告生成提示

⸻

3 Knowledge

知识库

包括：

法条

司法解释

指导案例

裁判规则

办案经验

⸻

4 Gate

门控体系

包括：

评价规则

风险规则

补强规则

评分规则

⸻

5 Template

输出模板

包括：

分析报告

起诉状

答辩状

代理意见

法律意见书

⸻

四、经验包生命周期

创建

Training System

↓

生成经验

⸻

验证

Gate Evaluation

↓

质量评估

⸻

发布

Package Registry

↓

版本管理

⸻

部署

Workspace

↓

加载运行

⸻

反馈

Gate Feedback

↓

回流训练系统

⸻

五、经验包版本

格式：

Major.Minor.Patch

例如：

1.0.0

1.1.0

2.0.0

⸻

Major

重大能力变更

⸻

Minor

新增能力

⸻

Patch

修复问题

⸻

六、经验包分类

通用经验包

跨案由通用

例如：

事实提取

证据分析

主体识别

⸻

案由经验包

特定案由

例如：

劳动争议

建设工程

离婚纠纷

民间借贷

⸻

场景经验包

特定场景

例如：

起诉阶段

答辩阶段

⸻

七、v2.3 Experience Package Builder

v2.3 在主后端实现 Experience Package Builder。

该 Builder 将已通过评估的 validated skill 导出为标准 Experience Package。

前置条件：

* skill 必须存在
* skill 必须完成 evaluation
* validation_status 必须为 validated

接口：

```text
POST /skills/{skill_id}/packages/build
GET /experience-packages
GET /experience-packages/{package_id}
GET /experience-packages/{package_id}/manifest
```

数据库表：

```text
experience_packages
```

字段：

* package_id
* skill_id
* name
* domain
* version
* status
* manifest_json
* package_path
* created_at

本地导出目录：

```text
Lawyer-AI-Platform-App/experience-packages/{package_id}/
├── package.json
├── skill.json
├── prompts/
│   ├── fact_prompt.txt
│   ├── analysis_prompt.txt
│   └── report_prompt.txt
├── templates/
│   └── report_template.md
└── tests/
    └── test_case.json
```

v2.3 生成的 Experience Package 状态为 built。

built 表示包已构建完成，但尚未进入正式 Package Registry 发布流程。

执行阶段

再审阶段

⸻

七、经验包仓库

平台建立：

Experience Registry

存储：

经验包

版本

发布记录

门控结果

适用范围

⸻

八、经验包部署原则

Workspace 不训练。

Workspace 不修改经验。

Workspace 只加载经验。

经验更新来自：

Training System。

⸻

九、经验包与门控关系

Experience Package：

定义能力。

Gate：

评价能力。

两者保持版本同步。

例如：

Labor-v2.1

对应：

Labor-Gate-v2.1

⸻

十、平台原则

Experience Package 是平台核心资产。

训练系统创造经验。

经验包沉淀经验。

生产系统消费经验。

形成：

Training
↓
Experience Package
↓
Workspace
↓
Feedback
↓
Training

持续演化闭环。
