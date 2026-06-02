# Experience Package Build（EP 构建）规范

## 一、定位

EP Build 是连接 Training System 与 Workspace System 的桥梁，用于将通过 SkillOpt 优化后的 Skill 封装成可复用的 Experience Package。

- Training System 输出经过 Gate 验证的 Skill
- EP Build 将 Skill 封装、增加元数据并发布
- Workspace System 使用 EP 来直接应用能力

---

## 二、构建流程

### 1. 收集 Skill

- 收集所有通过 Gate 验证的 Skill
- 确认 Skill 类型：Fact、Legal、Strategy、Report
- 验证 Skill Score 达到最低标准

### 2. 封装 Skill

- 将 Skill 按功能模块分类
- 生成 Skill Manifest，描述 Skill 功能、输入/输出、版本信息
- 保证 Skill 与平台接口兼容

### 3. 生成 EP Metadata

- EP 名称、版本号
- 作者、创建日期
- 依赖 Skill 列表
- Gate 验证信息
- EP 类型（案件、合同、咨询等）

### 4. EP 构建与打包

- 将 Skill、Manifest、Metadata 打包成 EP 文件
- 支持版本管理
- 确保可在 Workspace System 中直接加载

### 5. 发布至 Experience Registry

- EP 上传至 Experience Registry
- 生成唯一 EP ID
- 可供 Workspace System 检索和使用

---

## 三、原则

- 保持 EP 与平台独立性
- EP 应可重复构建，保证一致性
- 遵循版本管理规范
- 所有 Skill 必须经过 Gate 验证

