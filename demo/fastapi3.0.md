# FastAPI 进阶文档

本文档面向已经掌握 FastAPI 基础用法的开发者，介绍在实际项目中常用的进阶特性与工程实践。

## 目录

1. [依赖注入进阶](#1-依赖注入进阶)
2. [Pydantic 模型进阶](#2-pydantic-模型进阶)
3. [中间件与生命周期](#3-中间件与生命周期)
4. [异步与并发](#4-异步与并发)
5. [后台任务](#5-后台任务)
6. [WebSocket 与流式响应](#6-websocket-与流式响应)
7. [安全与认证](#7-安全与认证)
8. [错误处理](#8-错误处理)
9. [性能优化](#9-性能优化)
10. [测试策略](#10-测试策略)
11. [项目结构](#11-项目结构)
12. [部署建议](#12-部署建议)

---

## 1. 依赖注入进阶

### 1.1 带参数的依赖

依赖本身可以是一个返回函数的工厂，从而实现参数化：

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def pagination(skip: int = 0, limit: int = 10):
    def _pagination():
        return {"skip": skip, "limit": limit}
    return _pagination

@app.get("/items")
def list_items(page=Depends(pagination(skip=0, limit=20))):
    return page
```

### 1.2 类作为依赖

使用类可以复用状态并支持 `__call__`：

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/search")
def search(commons: CommonQueryParams = Depends()):
    return commons
```

### 1.3 依赖缓存与 `use_cache`

同一请求内，相同依赖默认只执行一次。若需要每次都重新执行，可设置 `use_cache=False`：

```python
from fastapi import Depends

def get_db():
    ...

@app.get("/a")
def a(db=Depends(get_db, use_cache=False)):
    ...
```

### 1.4 全局依赖

```python
app = FastAPI(dependencies=[Depends(verify_token)])
```

---

## 2. Pydantic 模型进阶

### 2.1 字段校验与约束

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)
    email: EmailStr
```

### 2.2 模型配置

```python
class UserOut(BaseModel):
    name: str
    age: int

    model_config = {
        "from_attributes": True,  # 支持从 ORM 对象转换
        "extra": "forbid",        # 禁止多余字段
    }
```

### 2.3 嵌套与泛型模型

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int

class Item(BaseModel):
    id: int
    name: str

@app.get("/items", response_model=Page[Item])
def list_items():
    return {"items": [{"id": 1, "name": "a"}], "total": 1}
```

### 2.4 自定义校验器

```python
from pydantic import field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name 不能为空")
        return v
```

---

## 3. 中间件与生命周期

### 3.1 自定义中间件

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.perf_counter() - start)
    return response
```

### 3.2 生命周期事件

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    app.state.db = await connect_db()
    yield
    # 关闭时
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)
```

---

## 4. 异步与并发

- I/O 密集任务使用 `async def`，避免阻塞事件循环。
- CPU 密集任务应放到线程池或进程池：

```python
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

def cpu_bound(x: int) -> int:
    return sum(i * i for i in range(x))

@app.get("/compute")
async def compute(x: int):
    result = await run_in_threadpool(cpu_bound, x)
    return {"result": result}
```

- 不要在 `async def` 中使用同步阻塞库（如 `requests`、`time.sleep`）。

---

## 5. 后台任务

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/send")
async def send(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "任务已触发")
    return {"message": "已接受"}
```

对于更复杂的任务，建议使用 Celery、RQ 或 Arq 等任务队列。

---

## 6. WebSocket 与流式响应

### 6.1 WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"echo: {data}")
    except WebSocketDisconnect:
        print("客户端断开")
```

### 6.2 流式响应

```python
from fastapi.responses import StreamingResponse

async def fake_stream():
    for i in range(5):
        yield f"chunk-{i}\n"

@app.get("/stream")
def stream():
    return StreamingResponse(fake_stream(), media_type="text/plain")
```

---

## 7. 安全与认证

### 7.1 OAuth2 + JWT

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

### 7.2 权限控制

```python
def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if role not in user.roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return user
    return checker

@app.get("/admin", dependencies=[Depends(require_role("admin"))])
def admin_only():
    return {"ok": True}
```

---

## 8. 错误处理

### 8.1 自定义异常处理器

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class BizError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

@app.exception_handler(BizError)
async def biz_error_handler(request: Request, exc: BizError):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message},
    )
```

### 8.2 覆盖默认校验错误

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"errors": exc.errors()})
```

---

## 9. 性能优化

- 使用 `orjson` 或 `ujson` 作为响应序列化器：

```python
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)
```

- 合理使用 `response_model` 与 `response_model_exclude_unset` 减少冗余字段。
- 数据库连接使用连接池，避免每次请求新建连接。
- 静态资源交给 Nginx 或 CDN，不要由应用进程处理。
- 使用 `gzip` 中间件压缩响应：

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 10. 测试策略

```python
from fastapi.testclient import TestClient
from myapp import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
```

异步测试可使用 `httpx.AsyncClient`：

```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp import app

@pytest.mark.anyio
async def test_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

建议覆盖：正常路径、边界值、鉴权失败、异常分支。

---

## 11. 项目结构

```
app/
├── main.py
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── users.py
│       └── items.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
├── schemas/
├── services/
├── db/
└── tests/
```

使用 `APIRouter` 拆分路由：

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    ...

app.include_router(router, prefix="/api/v1")
```

---

## 12. 部署建议

- 使用 `uvicorn` 或 `gunicorn + uvicorn worker` 运行：

```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000
```

- 生产环境关闭 `--reload`，通过环境变量管理配置。
- 使用 Docker 多阶段构建减小镜像体积。
- 配合 Nginx 做反向代理、TLS 终止与限流。
- 接入日志、指标（Prometheus）与链路追踪（OpenTelemetry）。

---

## 参考

- FastAPI 官方文档：https://fastapi.tiangolo.com/
- Pydantic 官方文档：https://docs.pydantic.dev/
- Starlette 官方文档：https://www.starlette.io/
