# FastAPI 入门教程

欢迎学习 FastAPI —— 一个现代、快速（高性能）的 Web 框架，用于构建 API，基于 Python 类型提示。

## 简介
FastAPI 以极简方式帮助你快速构建健壮、可扩展的 RESTful API。它自动提供交互式 API 文档（Swagger UI 和 ReDoc），并具备强大的数据验证与序列化能力。

## 环境准备
确保已安装 Python 3.8+，然后执行：

```bash
pip install fastapi uvicorn
```

- `fastapi`：核心框架
- `uvicorn`：ASGI 服务器（推荐用于开发和生产）

## 最小可运行示例
创建文件 `app.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## 启动服务
在终端中运行：

```bash
uvicorn app:app --reload
```

- `app:app` 表示：模块名 `app` 中的 `app` 实例（即 `app.py` 文件中的 `app = FastAPI()`）
- `--reload` 启用热重载（仅用于开发）

服务默认运行在 `http://127.0.0.1:8000`。

## 测试请求
- 访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 查看 JSON 响应
- 访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自动生成的交互式 Swagger UI
- 尝试 GET 请求：[http://127.0.0.1:8000/items/42?q=test](http://127.0.0.1:8000/items/42?q=test)

## 小结
你已成功运行第一个 FastAPI 应用！后续可探索路径参数、查询参数、请求体、依赖注入、数据库集成等高级特性。

> ✅ 提示：本教程不修改任何依赖或代码逻辑，仅为教学文档。