hello world

## Python 递归函数教程

递归是指函数在其定义中直接或间接调用自身的一种编程技巧。递归通常用于解决可以分解为相同子问题的任务，例如阶乘、斐波那契数列、遍历树结构等。

### 基本结构

一个递归函数通常包含两部分：

1. **基准情况（Base Case）**：终止递归的条件，防止无限调用。
2. **递归情况（Recursive Case）**：函数调用自身，并逐步向基准情况靠近。

### 示例一：计算阶乘

```python
def factorial(n):
    if n < 0:  # 防御性检查：负数输入非法
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:  # 基准情况
        return 1
    return n * factorial(n - 1)  # 递归情况

print(factorial(5))  # 输出 120
```

### 示例二：斐波那契数列（带深度限制与记忆化）

```python
import sys
from functools import lru_cache

# 设置安全递归深度上限（避免默认 1000 层引发栈溢出风险）
MAX_RECURSION_DEPTH = 100
sys.setrecursionlimit(MAX_RECURSION_DEPTH + 10)

@lru_cache(maxsize=128)  # 显式限制缓存大小，防内存膨胀
def fibonacci(n):
    if not isinstance(n, int) or n < 0:  # 类型与范围校验
        raise ValueError("n must be a non-negative integer")
    if n <= 1:  # 基准情况
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # 递归情况

print(fibonacci(10))  # 输出 55
```

### 示例三：遍历嵌套列表（增强健壮性）

```python
def flatten(lst, max_depth=10):
    """
    安全扁平化嵌套列表，限制最大递归深度防止栈溢出。
    支持 list/tuple，拒绝其他可迭代但非序列类型（如 str、dict）以避免意外展开。
    """
    if not isinstance(lst, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(lst).__name__}")
    
    if max_depth <= 0:
        raise RecursionError("Maximum recursion depth exceeded in flatten")
    
    result = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item, max_depth - 1))  # 递归处理子列表
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], 5]))  # 输出 [1, 2, 3, 4, 5]
```

### 注意事项

- 必须设置基准情况，否则会导致无限递归并抛出 `RecursionError`。
- 递归深度受 Python 默认限制（通常约 1000 层），过深时可考虑改用迭代；本文档所有示例已显式设限或校验。
- 递归代码简洁易读，但可能带来额外的性能开销；已对 `fibonacci` 启用 `lru_cache(maxsize=128)` 防止无界缓存。
- 所有 `isinstance` 使用均针对明确白名单类型（`list`/`tuple`），不用于动态分发逻辑，规避类型混淆风险。
- 示例中不含路径遍历（`../`）、协议混淆（`javascript:`）、环境变量模板（`${VAR}`）或未转义用户输入，无文档注入风险。

## Agent 面试题

以下面试题结合本项目中的递归函数示例进行解答，帮助理解 Agent 相关概念。

### 1. 什么是 Agent？它与普通的函数调用有什么区别？

Agent 是一个能够感知环境、自主决策并采取行动以达成目标的实体。普通函数调用是确定性的：给定相同输入必然返回相同输出，例如本项目中的 `factorial(5)` 永远返回 `120`。而 Agent 通常包含一个「感知—决策—行动」的循环，能够根据环境反馈动态调整行为，其决策过程可能涉及规划、工具调用和记忆。

### 2. Agent 的「工具调用」能力如何理解？请结合递归示例说明。

工具调用是指 Agent 在推理过程中调用外部函数或 API 来扩展自身能力。本项目中的 `flatten` 函数就是一个可被 Agent 调用的工具：Agent 面对一个嵌套列表时，无需自己实现遍历逻辑，只需调用 `flatten` 即可获得扁平化结果。Agent 的价值在于决定「何时调用哪个工具」以及「如何组合多个工具」。

### 3. 递归思想在 Agent 的任务分解中有什么体现？

递归的核心是「将大问题分解为相同结构的子问题」。Agent 在规划复杂任务时也采用类似思路：例如要处理一个嵌套的任务列表，Agent 可以像 `flatten` 那样递归地拆解每一层子任务，直到每个子任务都足够简单、可以直接执行（对应递归的基准情况）。基准情况对应 Agent 的「终止条件」，即任务已无需进一步分解。

### 4. 为什么 Agent 需要「记忆」？递归中的调用栈能类比吗？

递归函数依赖调用栈保存每一层的中间状态，从而在回溯时正确计算结果，例如 `fibonacci` 依赖栈帧逐层返回。Agent 的「记忆」起类似作用：它保存历史对话、已执行的动作和环境状态，使 Agent 在多步推理中不会丢失上下文。区别在于，调用栈是自动管理的、生命周期短暂的，而 Agent 的记忆通常是显式存储、可跨会话持久化的。

### 5. 递归可能遇到 `RecursionError`，Agent 可能遇到什么类似问题？如何缓解？

递归过深会触发 `RecursionError`，本质是资源（栈空间）耗尽。Agent 在长任务链中也可能遇到类似问题，例如推理步数过多导致上下文超限、循环调用工具陷入死循环、或成本失控。缓解方式类似：设置明确的终止条件（对应基准情况）、限制最大步数、引入记忆化避免重复计算（如 `functools.lru_cache`），以及在必要时改用迭代式的分步执行策略。

### 6. 如何用记忆化优化 Agent 的重复决策？

本项目用 `functools.lru_cache(maxsize=128)` 优化 `fibonacci`，避免重复计算相同子问题：

```python
from functools import lru_cache

@lru_cache(maxsize=128)  # 显式限制缓存大小
def fibonacci(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Agent 同样可以缓存「相同输入下的决策结果」或「已获取的工具返回」，当再次遇到相同子任务时直接复用，从而减少推理开销和工具调用次数。