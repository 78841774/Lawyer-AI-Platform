# Runtime Design（运行时设计）规范

## 一、定位

Runtime 是 Workspace 的执行引擎。

负责：

- 调度 Fact Layer
- 调度 Legal Layer
- 调度 Experience Package
- 调度 Agent

因此：

Runtime = Workspace Brain

---

## 二、运行流程

案件进入

↓

材料导入

↓

Fact Extraction

↓

Fact Graph

↓

Legal Analysis

↓

Strategy Generation

↓

Document Generation

↓

律师审核

↓

交付

---

## 三、核心模块

### 1 Fact Runtime

负责：

- 事实抽取
- 事实归类
- Fact Graph构建

输出：

```json
{
  "fact_id":"F001",
  "fact":"合同签订",
  "evidence":["A1"]
}
# Runtime Design（运行时设计）规范

## 一、定位
Runtime Design 模块定义 Workspace System 的运行架构、接口规范和调度逻辑，保证各模块协同高效运行。

---

## 二、核心模块
1. 任务调度
   - 管理 Fact Extraction、Legal Analysis 的执行顺序
   - 支持异步任务队列和优先级调度

2. 接口设计
   - 模块间通信使用标准 API
   - 支持 JSON/REST/GraphQL 等协议

3. 异常处理
   - 自动捕获错误并记录日志
   - 支持重试机制和人工干预

4. 监控与日志
   - 运行状态监控
   - 操作日志和分析日志统一存储，便于审计和优化

---

## 三、原则
- 模块解耦、接口标准化
- 高可用性和可扩展性
- 支持自动化和人工复核结合
