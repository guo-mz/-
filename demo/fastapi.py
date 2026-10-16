"""
FastAPI 入门教学示例（详细讲解版）
====================================

本文件用一个可运行的小项目，带你系统了解 FastAPI 的核心知识点：

1. 应用实例与路由（路径操作）
2. HTTP 方法（GET / POST / PUT / DELETE）
3. 路径参数与查询参数
4. 请求体与 Pydantic 数据模型（校验、类型转换）
5. 响应模型（response_model）与状态码
6. 依赖注入（Depends）
7. 错误处理（HTTPException）
8. 自动生成的交互式文档（Swagger UI / ReDoc）
9. 启动方式（uvicorn 命令行 与 python 直接运行）

--------------------------------------------------------------------
安装依赖
--------------------------------------------------------------------

    pip install fastapi uvicorn

（如果要用到 Pydantic 的高级校验，可一并安装 pydantic，FastAPI 会自动带上。）

--------------------------------------------------------------------
运行方式
--------------------------------------------------------------------

方式一（推荐，开发时热重载）：

    uvicorn fastapi:app --reload

    说明：`fastapi:app` 表示「模块名:应用实例名」。
    因为本文件名为 fastapi.py，所以模块名就是 fastapi。

方式二（直接运行本文件）：

    python fastapi.py

    文件末尾的 `if __name__ == "__main__":` 会调用 uvicorn.run(...)。

启动后打开浏览器访问：

    http://127.0.0.1:8000/docs      # Swagger UI，可直接点按钮调试接口
    http://127.0.0.1:8000/redoc     # ReDoc，更适合阅读的文档

--------------------------------------------------------------------
重要提醒：文件名与库名同名的问题
--------------------------------------------------------------------

本文件叫 fastapi.py，而我们要导入的第三方库也叫 fastapi。
在 Python 中，当前目录的模块优先级较高，直接写 `import fastapi`
有可能导入到「本文件自己」，从而出现奇怪的错误（例如找不到 app）。

因此本文件采用如下写法规避冲突：

    from fastapi import FastAPI

这种「从包里导入具体对象」的写法，在大多数情况下能正确导入第三方库。
但最稳妥的做法是：**不要把教学文件命名为 fastapi.py**，
建议改成 main.py、app.py 或 fastapi_demo.py。
这里保留 fastapi.py 只是为了满足教学命名需求，请知悉该注意事项。
"""

# ---------------------------------------------------------------------------
# 1. 导入依赖
# ---------------------------------------------------------------------------
# FastAPI：核心类，用来创建应用实例。
from fastapi import FastAPI, HTTPException, Depends, Query, Path, status

# BaseModel：Pydantic 的基类，用来定义请求体 / 响应体的数据结构。
# Field：为字段添加额外约束与说明（如最小值、描述、示例）。
from pydantic import BaseModel, Field

# typing 用于类型标注，FastAPI 会读取这些标注来做参数校验和文档生成。
from typing import Optional, List


# ---------------------------------------------------------------------------
# 2. 创建应用实例
# ---------------------------------------------------------------------------
# title / description / version 会显示在自动生成的文档页面上。
app = FastAPI(
    title="FastAPI 教学示例",
    description="一个用于学习 FastAPI 核心概念的示例项目",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# 3. 数据模型（Pydantic BaseModel）
# ---------------------------------------------------------------------------
# 作用：
#   - 定义请求体的结构，FastAPI 会自动解析 JSON 并做类型校验；
#   - 定义响应体的结构，配合 response_model 过滤多余字段；
#   - 自动生成接口文档中的字段说明。
class Item(BaseModel):
    """商品数据模型。"""

    # ... 表示该字段必填；Field 可补充约束与文档说明。
    name: str = Field(..., description="商品名称", min_length=1, max_length=50)
    price: float = Field(..., gt=0, description="商品价格，必须大于 0")
    # Optional + 默认值 None 表示该字段可选。
    description: Optional[str] = Field(None, description="商品描述，可选")
    tags: List[str] = Field(default_factory=list, description="标签列表，可选")

    # 通过 model_config 提供示例，会显示在文档中。
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "机械键盘",
                "price": 399.0,
                "description": "87 键，青轴",
                "tags": ["数码", "外设"],
            }
        }
    }


class ItemOut(BaseModel):
    """商品响应模型：只暴露给客户端的字段。"""

    id: int
    name: str
    price: float
    description: Optional[str] = None


# ---------------------------------------------------------------------------
# 4. 内存数据库（仅用于演示，真实项目请使用真正的数据库）
# ---------------------------------------------------------------------------
# 用字典模拟存储，key 为商品 id，value 为商品数据。
fake_db: dict[int, dict] = {
    1: {"id": 1, "name": "机械键盘", "price": 399.0, "description": "87 键，青轴"},
    2: {"id": 2, "name": "无线鼠标", "price": 129.0, "description": "静音款"},
}

# 自增 id 计数器。
_next_id = 3


# ---------------------------------------------------------------------------
# 5. 依赖注入（Depends）
# ---------------------------------------------------------------------------
# 依赖是一个普通函数，FastAPI 会在调用路径操作函数前自动执行它，
# 并把返回值作为参数注入。常用于：数据库连接、鉴权、公共参数解析等。
def get_db() -> dict[int, dict]:
    """模拟获取数据库连接。

    真实项目中这里可能是 yield 一个数据库会话，并在请求结束后关闭。
    """
    return fake_db


def verify_token(token: Optional[str] = None) -> str:
    """模拟鉴权依赖：校验请求头或查询参数中的 token。

    这里为了演示简单，只要求 token 等于 "secret"。
    真实项目应使用 OAuth2 / JWT 等方案。
    """
    if token != "secret":
        # 鉴权失败时抛出 HTTPException，FastAPI 会返回对应状态码和错误信息。
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 token，请传入 token=secret",
        )
    return token


# ---------------------------------------------------------------------------
# 6. 路径操作：GET 请求
# ---------------------------------------------------------------------------
# @app.get("/") 是「装饰器」，把下面的函数注册为处理 GET / 的路径操作函数。
# 函数名 hello 会作为文档中的操作名称（operationId）。
@app.get("/", summary="根路径", tags=["基础"])
def hello() -> dict:
    """最简单的接口：访问根路径返回一句问候。"""
    return {"message": "Hello, FastAPI!"}


# ---------------------------------------------------------------------------
# 7. 路径参数（Path Parameter）
# ---------------------------------------------------------------------------
# 路径中的 {item_id} 是路径参数，函数同名参数会自动接收它。
# 类型标注 int 会让 FastAPI 自动做类型转换与校验：
#   - 传入非整数会返回 422 校验错误；
#   - Path(..., ge=1) 进一步限制必须 >= 1。
@app.get("/items/{item_id}", response_model=ItemOut, tags=["商品"])
def get_item(
    item_id: int = Path(..., ge=1, description="商品 ID，必须大于等于 1"),
    db: dict = Depends(get_db),
):
    """根据 ID 获取单个商品。"""
    item = db.get(item_id)
    if item is None:
        # 找不到资源时返回 404。
        raise HTTPException(status_code=404, detail=f"商品 {item_id} 不存在")
    return item


# ---------------------------------------------------------------------------
# 8. 查询参数（Query Parameter）
# ---------------------------------------------------------------------------
# 函数中「不是路径参数、也不是 Pydantic 模型」的参数，会被当作查询参数。
# 例如 /items?skip=0&limit=10&keyword=键盘
@app.get("/items", response_model=List[ItemOut], tags=["商品"])
def list_items(
    skip: int = Query(0, ge=0, description="跳过多少条"),
    limit: int = Query(10, ge=1, le=100, description="返回多少条，最多 100"),
    keyword: Optional[str] = Query(None, description="按名称模糊搜索，可选"),
    db: dict = Depends(get_db),
):
    """获取商品列表，支持分页与关键字搜索。"""
    items = list(db.values())
    if keyword:
        items = [i for i in items if keyword in i["name"]]
    return items[skip : skip + limit]


# ---------------------------------------------------------------------------
# 9. 请求体（Request Body）：POST 请求
# ---------------------------------------------------------------------------
# 参数类型是 Pydantic 模型（Item）时，FastAPI 会把它当作请求体，
# 自动从 JSON 中解析并校验。
# status_code=201 表示创建成功，会体现在响应状态码和文档中。
@app.post(
    "/items",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    tags=["商品"],
)
def create_item(item: Item, db: dict = Depends(get_db)) -> dict:
    """创建一个新商品。"""
    global _next_id
    new_item = {
        "id": _next_id,
        "name": item.name,
        "price": item.price,
        "description": item.description,
    }
    db[_next_id] = new_item
    _next_id += 1
    return new_item


# ---------------------------------------------------------------------------
# 10. PUT 请求：更新资源
# ---------------------------------------------------------------------------
@app.put("/items/{item_id}", response_model=ItemOut, tags=["商品"])
def update_item(
    item_id: int = Path(..., ge=1),
    item: Item = ...,  # 请求体
    db: dict = Depends(get_db),
) -> dict:
    """整体更新一个商品。"""
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"商品 {item_id} 不存在")
    db[item_id] = {
        "id": item_id,
        "name": item.name,
        "price": item.price,
        "description": item.description,
    }
    return db[item_id]


# ---------------------------------------------------------------------------
# 11. DELETE 请求：删除资源
# ---------------------------------------------------------------------------
@app.delete("/items/{item_id}", tags=["商品"])
def delete_item(
    item_id: int = Path(..., ge=1),
    db: dict = Depends(get_db),
    _token: str = Depends(verify_token),  # 删除操作需要鉴权
) -> dict:
    """删除一个商品（需要 token=secret）。"""
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"商品 {item_id} 不存在")
    del db[item_id]
    return {"message": f"商品 {item_id} 已删除"}


# ---------------------------------------------------------------------------
# 12. 启动入口
# ---------------------------------------------------------------------------
# 直接运行 `python fastapi.py` 时，会启动 uvicorn 服务器。
# 使用 `uvicorn fastapi:app --reload` 时，这段代码不会执行。
if __name__ == "__main__":
    import uvicorn

    # host="127.0.0.1" 只允许本机访问；改成 "0.0.0.0" 可被局域网访问。
    # reload=True 表示代码改动后自动重启，仅建议开发环境使用。
    uvicorn.run("fastapi:app", host="127.0.0.1", port=8000, reload=True)
