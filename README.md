hello world
 ###手写一个
## Python 递归函数教程

递归是指函数在其定义中直接或间接调用自身的一种编程技巧。递归通常用于解决可以分解为相同子问题的任务，例如阶乘、斐波那契数列、遍历树结构等。

### 基本结构

一个递归函数通常包含两部分：

1. **基准情况（Base Case）**：终止递归的条件，防止无限调用。
2. **递归情况（Recursive Case）**：函数调用自身，并逐步向基准情况靠近。

### 示例一：计算阶乘

```python
def factorial(n):
    if n == 0 or n == 1:  # 基准情况
        return 1
    return n * factorial(n - 1)  # 递归情况

print(factorial(5))  # 输出 120
```

### 示例二：斐波那契数列

```python
def fibonacci(n):
    if n <= 1:  # 基准情况
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # 递归情况

print(fibonacci(10))  # 输出 55
```

### 示例三：遍历嵌套列表

```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))  # 递归处理子列表
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], 5]))  # 输出 [1, 2, 3, 4, 5]
```

### 注意事项

- 必须设置基准情况，否则会导致无限递归并抛出 `RecursionError`。
- 递归深度受 Python 默认限制（通常约 1000 层），过深时可考虑改用迭代。
- 递归代码简洁易读，但可能带来额外的性能开销，必要时可使用记忆化（如 `functools.lru_cache`）优化。
