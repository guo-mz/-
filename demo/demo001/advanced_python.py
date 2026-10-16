"""Python 高级特性示例集合。

本模块演示若干 Python 高级主题，每个主题都提供可直接运行的示例。
运行方式：
    python advanced_python.py
"""

from __future__ import annotations

import asyncio
import functools
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, Iterable, Iterator, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. 装饰器（Decorator）
# ---------------------------------------------------------------------------
def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """测量函数执行耗时的装饰器。"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"[timer] {func.__name__} 耗时 {elapsed:.6f}s")

    return wrapper


def repeat(times: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """带参数的装饰器：将函数重复执行指定次数。"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result: Any = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@timer
@repeat(3)
def greet(name: str) -> str:
    """被装饰的函数：重复打印问候语。"""
    print(f"Hello, {name}!")
    return name


# ---------------------------------------------------------------------------
# 2. 生成器（Generator）
# ---------------------------------------------------------------------------
def fibonacci(limit: int) -> Iterator[int]:
    """惰性生成斐波那契数列，最多 limit 个元素。"""
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b


def read_in_chunks(data: Iterable[T], size: int) -> Generator[list[T], None, None]:
    """将可迭代对象按固定大小分块。"""
    chunk: list[T] = []
    for item in data:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


# ---------------------------------------------------------------------------
# 3. 上下文管理器（Context Manager）
# ---------------------------------------------------------------------------
@contextmanager
+def managed_resource(name: str) -> Generator[str, None, None]:
    """基于生成器的上下文管理器，模拟资源的获取与释放。"""
    print(f"[resource] 获取 {name}")
    try:
        yield name
    finally:
        print(f"[resource] 释放 {name}")


class Timer:
    """基于类的上下文管理器，用于代码块计时。"""

    def __init__(self, label: str = "block") -> None:
        self.label = label
        self.elapsed = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        self.elapsed = time.perf_counter() - self._start
        print(f"[Timer] {self.label} 耗时 {self.elapsed:.6f}s")
        return False  # 不吞掉异常


# ---------------------------------------------------------------------------
# 4. 数据类（dataclass）
# ---------------------------------------------------------------------------
@dataclass(order=True)
class Point:
    """支持比较与排序的二维点。"""

    x: float
    y: float
    tags: list[str] = field(default_factory=list, compare=False)

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ---------------------------------------------------------------------------
# 5. 异步基础（asyncio）
# ---------------------------------------------------------------------------
async def fetch(name: str, delay: float) -> str:
    """模拟异步 I/O 操作。"""
    await asyncio.sleep(delay)
    return f"{name} 完成（延迟 {delay}s）"


async def run_async_demo() -> list[str]:
    """并发执行多个异步任务。"""
    tasks = [fetch("任务A", 0.2), fetch("任务B", 0.1), fetch("任务C", 0.3)]
    return await asyncio.gather(*tasks)


# ---------------------------------------------------------------------------
# 6. 类型注解与泛型工具
# ---------------------------------------------------------------------------
def first_or_default(items: Iterable[T], default: T | None = None) -> T | None:
    """返回可迭代对象的第一个元素，为空时返回默认值。"""
    for item in items:
        return item
    return default


# ---------------------------------------------------------------------------
# 演示入口
# ---------------------------------------------------------------------------
def demo_decorators() -> None:
    print("=== 装饰器 ===")
    greet("Python")


def demo_generators() -> None:
    print("\n=== 生成器 ===")
    print("斐波那契前 10 项:", list(fibonacci(10)))
    print("分块结果:", list(read_in_chunks(range(7), 3)))


def demo_context_managers() -> None:
    print("\n=== 上下文管理器 ===")
    with managed_resource("数据库连接") as res:
        print(f"使用资源: {res}")
    with Timer("计算 1..100000 求和") as t:
        total = sum(range(100_000))
    print(f"求和结果: {total}, 记录耗时: {t.elapsed:.6f}s")


def demo_dataclass() -> None:
    print("\n=== dataclass ===")
    p1 = Point(0.0, 0.0, ["origin"])
    p2 = Point(3.0, 4.0, ["target"])
    print(p1)
    print(p2)
    print(f"两点距离: {p1.distance_to(p2)}")
    print("排序结果:", sorted([p2, p1]))


def demo_async() -> None:
    print("\n=== 异步基础 ===")
    results = asyncio.run(run_async_demo())
    for line in results:
        print(line)


def demo_typing() -> None:
    print("\n=== 类型注解 ===")
    print("first_or_default([]):", first_or_default([], "默认值"))
    print("first_or_default([1, 2, 3]):", first_or_default([1, 2, 3]))


def main() -> None:
    demo_decorators()
    demo_generators()
    demo_context_managers()
    demo_dataclass()
    demo_async()
    demo_typing()


if __name__ == "__main__":
    main()
