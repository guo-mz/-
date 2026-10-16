# Python 爬虫教程

本教程面向 Python 初学者，介绍网络爬虫的基本概念、常用工具库、静态页面抓取流程、数据解析与保存方法，以及反爬机制与合规注意事项。

> 说明：本教程中的示例仅用于学习目的，请遵守目标网站的 robots.txt 与服务条款，不要对真实站点进行高频或大规模抓取。

## 目录

- [1. 什么是网络爬虫](#1-什么是网络爬虫)
- [2. 环境准备](#2-环境准备)
- [3. HTTP 基础](#3-http-基础)
- [4. 使用 requests 发送请求](#4-使用-requests-发送请求)
- [5. 使用 BeautifulSoup 解析 HTML](#5-使用-beautifulsoup-解析-html)
- [6. 使用 lxml 与 XPath 解析](#6-使用-lxml-与-xpath-解析)
- [7. 数据保存](#7-数据保存)
- [8. 反爬机制与应对思路](#8-反爬机制与应对思路)
- [9. 合规与道德注意事项](#9-合规与道德注意事项)
- [10. 进阶方向](#10-进阶方向)

## 1. 什么是网络爬虫

网络爬虫（Web Crawler）是一种按照一定规则自动抓取互联网信息的程序。它通常包含以下步骤：

1. 发送 HTTP 请求获取网页内容；
2. 解析网页，提取所需数据；
3. 保存数据（文件、数据库等）；
4. 根据链接继续抓取其他页面（可选）。

常见应用场景包括：数据采集、价格监控、舆情分析、搜索引擎索引等。

## 2. 环境准备

建议使用 Python 3.8 及以上版本，并创建独立的虚拟环境：

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

安装常用依赖：

```bash
pip install requests beautifulsoup4 lxml
```

- `requests`：简洁易用的 HTTP 客户端库；
- `beautifulsoup4`：HTML/XML 解析库，支持多种解析器；
- `lxml`：高性能解析器，支持 XPath。

## 3. HTTP 基础

爬虫与网站交互依赖 HTTP 协议，需要了解以下概念：

- **请求方法**：GET 用于获取资源，POST 用于提交数据；
- **请求头（Headers）**：如 `User-Agent`、`Referer`、`Cookie`；
- **状态码**：`200` 成功，`301/302` 重定向，`403` 禁止访问，`404` 未找到，`500` 服务器错误；
- **响应内容**：HTML、JSON、XML 等。

## 4. 使用 requests 发送请求

### 4.1 基本 GET 请求

```python
import requests

url = "https://example.com"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()  # 非 2xx 状态码时抛出异常
response.encoding = response.apparent_encoding  # 自动推断编码
print(response.text[:500])
```

### 4.2 带参数的请求

```python
params = {"q": "python", "page": 1}
response = requests.get("https://example.com/search", params=params, timeout=10)
print(response.url)
```

### 4.3 POST 请求

```python
data = {"username": "demo", "password": "secret"}
response = requests.post("https://example.com/login", data=data, timeout=10)
print(response.status_code)
```

### 4.4 使用 Session 保持会话

```python
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

session.get("https://example.com/login", timeout=10)
response = session.get("https://example.com/profile", timeout=10)
print(response.text[:200])
```

## 5. 使用 BeautifulSoup 解析 HTML

```python
from bs4 import BeautifulSoup

html = """
<html>
  <body>
    <h1 class="title">示例标题</h1>
    <ul class="list">
      <li><a href="/item/1">条目一</a></li>
      <li><a href="/item/2">条目二</a></li>
    </ul>
  </body>
</html>
"""

soup = BeautifulSoup(html, "lxml")

# 获取标题文本
print(soup.h1.get_text(strip=True))

# 遍历列表项
for li in soup.select("ul.list li a"):
    print(li.get_text(strip=True), li.get("href"))
```

常用方法：

- `soup.find(name, attrs)`：查找第一个匹配元素；
- `soup.find_all(name, attrs)`：查找所有匹配元素；
- `soup.select(css_selector)`：使用 CSS 选择器；
- `tag.get_text(strip=True)`：获取文本并去除空白；
- `tag.get("href")`：获取属性值。

## 6. 使用 lxml 与 XPath 解析

```python
from lxml import etree

html = """
<html>
  <body>
    <div class="item">
      <span class="name">商品 A</span>
      <span class="price">19.9</span>
    </div>
    <div class="item">
      <span class="name">商品 B</span>
      <span class="price">29.9</span>
    </div>
  </body>
</html>
"""

tree = etree.HTML(html)
for item in tree.xpath("//div[@class='item']"):
    name = item.xpath("./span[@class='name']/text()")[0]
    price = item.xpath("./span[@class='price']/text()")[0]
    print(name, price)
```

XPath 常用语法：

- `//div`：选取所有 `div` 元素；
- `//div[@class='item']`：按属性筛选；
- `./span/text()`：选取当前节点下的文本；
- `//a/@href`：选取属性值。

## 7. 数据保存

### 7.1 保存为 CSV

```python
import csv

rows = [
    {"name": "商品 A", "price": "19.9"},
    {"name": "商品 B", "price": "29.9"},
]

with open("items.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price"])
    writer.writeheader()
    writer.writerows(rows)
```

### 7.2 保存为 JSON

```python
import json

with open("items.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
```

### 7.3 保存到 SQLite

```python
import sqlite3

conn = sqlite3.connect("items.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS items (name TEXT, price TEXT)"
)
cursor.executemany(
    "INSERT INTO items (name, price) VALUES (?, ?)",
    [(row["name"], row["price"]) for row in rows],
)
conn.commit()
conn.close()
```

## 8. 反爬机制与应对思路

常见反爬手段：

- **User-Agent 校验**：设置合理的请求头；
- **IP 频率限制**：降低请求频率，使用 `time.sleep()` 或限速；
- **Cookie / 登录校验**：使用 `requests.Session` 维持会话；
- **验证码**：需人工处理或使用合规的识别服务；
- **动态渲染**：页面内容由 JavaScript 生成，可使用 Selenium、Playwright 等工具。

示例：控制请求频率

```python
import time
import requests

urls = ["https://example.com/page/1", "https://example.com/page/2"]

for url in urls:
    response = requests.get(url, timeout=10)
    print(response.status_code)
    time.sleep(1)  # 每次请求间隔 1 秒
```

## 9. 合规与道德注意事项

- 遵守目标网站的 `robots.txt` 与服务条款；
- 不抓取个人隐私、版权受限或明确禁止抓取的内容；
- 控制请求频率，避免对目标服务器造成压力；
- 不将抓取数据用于非法用途；
- 如网站提供官方 API，优先使用 API。

## 10. 进阶方向

- **Scrapy**：功能完善的爬虫框架，支持调度、去重、中间件；
- **异步爬虫**：使用 `aiohttp` + `asyncio` 提升并发效率；
- **动态页面**：Selenium、Playwright 处理 JavaScript 渲染；
- **分布式爬虫**：结合 Redis、消息队列实现大规模抓取；
- **数据清洗与分析**：结合 pandas、数据库进行后续处理。

## 参考链接

- requests 官方文档：<https://requests.readthedocs.io/>
- BeautifulSoup 官方文档：<https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
- lxml 官方文档：<https://lxml.de/>
- Scrapy 官方文档：<https://scrapy.org/>
