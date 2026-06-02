# Workspace Architecture（工作空间架构）

## 一、定位

Workspace System 是 Lawyer AI Platform 的案件执行系统。

负责：

- 接收案件
- 管理材料
- 抽取事实
- 分析法律问题
- 生成策略
- 生成法律文书
- 支持律师协作

Workspace 不负责能力训练。

所有能力来自 Experience Package。

---

## 二、总体架构

案件

↓

Material System

↓

Fact Extraction

↓

Fact Layer

↓

Legal Analysis

↓

Strategy Generation

↓

Document Generation

↓

Lawyer Review

↓

Delivery

---

## 三、核心模块

### 1 Material System

负责：

- 材料上传
- 材料管理
- 材料检索
- 材料版本控制

输出：

案件材料库

---

### 2 Fact Extraction

负责：

- 事实识别
- 事实归类
- 证据关联
- Fact Graph 构建

输出：

Fact Layer

---

### 3 Legal Analysis

负责：

- 法律问题识别
- 法条匹配
- 案例匹配
- 风险分析

输出：

Legal Layer

---

### 4 Strategy Engine

负责：

- 诉讼策略
- 谈判策略
- 证据策略
- 风险策略

输出：

Strategy Package

---

### 5 Document Engine

负责：

- 起诉状生成
- 答辩状生成
- 法律意见书生成
- 合同生成

输出：

法律文书

---

## 四、设计原则

- Fact First
- Legal Second
- Strategy Third
- Human Review Required

律师始终保留最终决策权。
