# Gate Specification（门控规范）

## 一、定位

Gate 是 Experience Package 的质量控制系统。

Skill 负责生成结果。

Gate 负责评价结果。

因此：

Skill = Produce

Gate = Evaluate

平台所有关键输出必须经过 Gate。

## 二、Gate的目标

Gate 不负责重做任务。

Gate 负责判断：

是否达到交付标准

输出：

PASS

FAIL

或者：

Score = 0~100

## 三、Gate分类

Experience Package 内包含：

### Fact Gate

评价：

- 事实完整度
- 事实一致性
- 证据覆盖率

### Legal Gate

评价：

- 法律适用正确率
- 法条引用准确率
- 裁判规则匹配度

### Strategy Gate

评价：

- 策略可执行性
- 风险识别能力
- 胜诉路径合理性

### Report Gate

评价：

- 报告结构完整性
- 逻辑连贯性
- 可交付性

## 四、Gate标准结构

每个 Gate 文件必须包含：

- 目标
- 评价维度
- 评分规则
- 通过标准
- 失败原因

## 五、Fact Gate

检查：

- 人物
- 时间
- 地点
- 行为
- 金额
- 结果

是否完整。

检查事实是否互相矛盾。

检查关键事实是否有证据支撑。

## 六、Legal Gate

检查：

- 法律关系识别
- 法律依据正确性
- 裁判规则匹配性

## 七、Strategy Gate

检查：

- 诉讼路径
- 证据策略
- 风险预警

是否可执行。

## 八、Report Gate

检查：

- 事实
- 法律
- 策略
- 结论

是否完整。

检查是否达到客户交付标准。

## 九、评分机制

建议：

Completeness 40%

Accuracy 40%

Consistency 20%

总分100。

## 十、通过标准

90+ 优秀

80+ 通过

60~80 需优化

60以下 失败

## 十一、Gate运行流程

Skill Output

↓

Fact Gate

↓

Legal Gate

↓

Strategy Gate

↓

Report Gate

↓

Final Result

## 十二、平台原则

任何结果未经 Gate 验证：

禁止进入 Workspace 输出层。

Gate 是 Experience Package 的质量保障核心。
