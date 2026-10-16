# demo001 — Python 高级特性示例

本目录用于演示 Python 的高级语言特性，代码集中在 `advanced_python.py` 中，可直接运行。

## 目录结构

```
demo/demo001/
├── advanced_python.py   # 高级特性示例代码
└── README.md            # 本说明文档
```

## 示例主题

| 主题 | 说明 |
| --- | --- |
| 装饰器 | 无参装饰器、带参装饰器、`functools.wraps` 保留元信息 |
| 生成器 | `yield` 惰性求值、分块读取可迭代对象 |
| 上下文管理器 | `@contextmanager` 与基于类的 `__enter__` / `__exit__` |
| dataclass | `@dataclass(order=True)`、`field(default_factory=...)` |
| 异步基础 | `async` / `await`、`asyncio.gather` 并发执行 |
| 类型注解 | 泛型 `TypeVar`、`Iterable`、`T | None` 联合类型 |

## 运行方式

需要 Python 3.10 及以上版本（使用了 `X | None` 联合类型语法）。

```bash
cd demo/demo001
python advanced_python.py
```

## 预期输出（节选）

```
=== 装饰器 ===
Hello, Python!
Hello, Python!
Hello, Python!
[timer] greet 耗时 0.0000xx s

=== 生成器 ===
斐波那契前 10 项: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
分块结果: [[0, 1, 2], [3, 4, 5], [6]]
...
```

## 说明

- 所有示例均为自包含代码，不依赖第三方库。
- 异步示例使用 `asyncio.run()` 作为入口，便于直接运行。
- 如需扩展，可在 `advanced_python.py` 中新增 `demo_*` 函数，并在 `main()` 中调用。
