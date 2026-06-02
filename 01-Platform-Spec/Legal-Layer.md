º# Legal Layer（法律层）规范

## 一、定位

Legal Layer 建立在 Fact Layer 之上。

职责：

- 识别法律问题
- 匹配法律规则
- 匹配司法解释
- 匹配案例
- 构建法律推理链

原则：

没有事实，不做法律分析。

Fact First，Legal Second。

---

## 二、目标

Legal Layer 不负责生成结论。

Legal Layer 负责建立：

事实 → 法律规则 → 推理过程

确保法律分析可解释、可追踪、可验证。

---

## 三、核心结构

### Legal Issue

法律问题。例如：

- 合同是否成立
- 是否构成违约
- 是否产生损害赔偿责任

### Legal Rule

法律规则。来源：

- 法律
- 行政法规
- 司法解释
- 指导案例

### Legal Reasoning

法律推理链。结构：

Fact

↓

Rule

↓

Application

↓

Conclusion

---

## 四、输出格式

```json
{
  "issue": "合同是否成立",
  "rule": "民法典合同编",
  "facts": ["F001","F002"],
  "reasoning": "双方已达成合意",
  "conclusion": "合同成立"
}
