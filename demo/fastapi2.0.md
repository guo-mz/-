# FastAPI 进阶指南

本文档面向已经掌握 FastAPI 基础用法的开发者，介绍在实际项目中常用的进阶特性与最佳实践。

## 目录

1. [依赖注入进阶](#依赖注入进阶)
2. [Pydantic 模型进阶](#pydantic-模型进阶)
3. [中间件与生命周期](#中间件与生命周期)
4. [后台任务与异步](#后台任务与异步)
5. [安全与认证](#安全与认证)
6. [数据库集成](#数据库集成)
7. [性能优化](#性能优化)
8. [测试与部署](#测试与部署)

---

## 依赖注入进阶

### 带 yield 的依赖

使用 `yield` 可以在请求结束后执行清理逻辑，适合数据库会话、文件句柄等资源管理。

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### 依赖的缓存与复用

同一个请求内，默认情况下相同依赖只会被调用一次（`use_cache=True`）。若需要每次重新执行，可设置 `use_cache=False`。

```python
from fastapi import Depends

def get_value():
    return expensive_computation()

@app.get("/a")
def a(v=Depends(get_value, use_cache=False)):
    return v
```

### 类作为依赖

类依赖可以携带配置参数，便于复用。

```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/users")
def list_users(p: Pagination = Depends()):
    return query_users(p.skip, p.limit)
```

---

## Pydantic 模型进阶

### 字段校验与约束

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(ge=0, le=150)
```

### 模型配置

```python
class UserOut(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True,  # 支持从 ORM 对象转换
        "extra": "forbid",        # 禁止额外字段
    }
```

### 嵌套与泛型模型

```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int

class ItemOut(BaseModel):
    id: int
    name: str

@app.get("/items", response_model=Page[ItemOut])
def list_items():
    ...
```

---

## 中间件与生命周期

### 自定义中间件

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

### 生命周期事件

推荐使用 `lifespan` 替代已废弃的 `@app.on_event`。

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_resources()
    yield
    # 关闭时执行
    await close_resources()

app = FastAPI(lifespan=lifespan)
```

---

## 后台任务与异步

### BackgroundTasks

```python
from fastapi import BackgroundTasks

def send_email(to: str):
    ...

@app.post("/register")
def register(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_email, email)
    return {"message": "registered"}
```

### 异步与同步的选择

- I/O 密集型任务使用 `async def`，配合异步库（如 `httpx`、`asyncpg`）。
- CPU 密集型任务使用普通 `def`，FastAPI 会将其放入线程池执行，避免阻塞事件循环。

```python
@app.get("/async")
async def async_endpoint():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://example.com")
    return r.json()
```

---

## 安全与认证

### OAuth2 + JWT

```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

@app.get("/me")
def me(user=Depends(get_current_user)):
    return user
```

### 权限依赖

```python
def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker

@app.delete("/admin", dependencies=[Depends(require_role("admin"))])
def admin_only():
    return {"ok": True}
```

---

## 数据库集成

### 异步 SQLAlchemy

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

### 事务管理

```python
@app.post("/transfer")
async def transfer(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        ...
```

---

## 性能优化

- 使用 `response_model` 限制返回字段，减少序列化开销。
- 对高频只读接口使用缓存（如 Redis）。
- 使用 `ORJSONResponse` 提升 JSON 序列化速度。
- 合理使用连接池，避免频繁创建连接。

```python
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)
```

---

## 测试与部署

### 使用 TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read():
    response = client.get("/")
    assert response.status_code == 200
```

### 异步测试

```python
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/")
    assert r.status_code == 200
```

### 部署建议

- 使用 `uvicorn` 或 `gunicorn` + `uvicorn.workers.UvicornWorker`。
- 通过环境变量管理配置，避免硬编码密钥。
- 使用 Docker 容器化，配合反向代理（Nginx）与健康检查。

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 小结

掌握以上进阶特性后，可以构建结构清晰、性能良好、易于维护的 FastAPI 应用。建议结合官方文档持续跟进新版本特性。
