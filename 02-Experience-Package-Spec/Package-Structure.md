Experience Package 目录结构规范

一、定位

Package Structure 定义 Experience Package 的标准文件结构。

Training System 必须按照本规范产出经验包。

Workspace System 必须按照本规范加载经验包。

⸻

二、标准目录结构

experience-package/
├── package.yaml
├── skills/
│   ├── fact-skill.md
│   ├── legal-skill.md
│   ├── strategy-skill.md
│   └── report-skill.md
├── gates/
│   ├── fact-gate.md
│   ├── legal-gate.md
│   ├── strategy-gate.md
│   └── report-gate.md
├── knowledge/
│   ├── law.md
│   ├── cases.md
│   ├── judicial-rules.md
│   └── practice-experience.md
├── schemas/
│   ├── fact.schema.json
│   ├── legal.schema.json
│   ├── strategy.schema.json
│   └── report.schema.json
├── templates/
│   ├── fact-report.md
│   ├── legal-analysis.md
│   ├── litigation-strategy.md
│   └── final-report.md
└── tests/
    ├── sample-cases/
    ├── expected-output/
    └── gate-results/

⸻

三、package.yaml

package.yaml 是经验包入口文件。

必须包含：

name: loan-dispute-package
version: 1.0.0
type: cause-of-action-package
cause_of_action:
  - 民间借贷纠纷
supported_models:
  - deepseek-v4-flash
  - gpt
  - claude
entry:
  fact_skill: skills/fact-skill.md
  legal_skill: skills/legal-skill.md
  fact_gate: gates/fact-gate.md
  legal_gate: gates/legal-gate.md

⸻

四、skills目录

skills 目录存放能力文件。

包括：

* fact-skill.md
* legal-skill.md
* strategy-skill.md
* report-skill.md

Skill 文件定义如何完成任务。

⸻

五、gates目录

gates 目录存放门控规则。

包括：

* fact-gate.md
* legal-gate.md
* strategy-gate.md
* report-gate.md

Gate 文件定义如何评价结果质量。

⸻

六、knowledge目录

knowledge 目录存放知识文件。

包括：

* 法条
* 司法解释
* 指导案例
* 裁判规则
* 办案经验

Knowledge 不直接执行任务。

Knowledge 供 Skill 引用。

⸻

七、schemas目录

schemas 目录定义结构化输出格式。

Workspace 通过 Schema 校验输出结果。

⸻

八、templates目录

templates 目录存放报告模板。

用于最终成果输出。

⸻

九、tests目录

tests 目录用于研发系统验证经验包。

Workspace 可忽略 tests 目录。

Training System 必须维护 tests 目录。

⸻

十、部署原则

Experience Package 必须作为整体部署。

禁止只部署单个 Skill。

禁止生产系统临时修改经验包内容。

更新经验包必须通过版本升级完成。

⸻

十一、兼容性原则

Patch 版本必须向后兼容。

Minor 版本允许新增能力。

Major 版本允许破坏性变更。

⸻

十二、平台原则

Training System 负责生成 Package。

Workspace System 负责加载 Package。

Package Structure 是两系统之间的稳定协议。