# Redis 入门教程

Redis（Remote Dictionary Server）是一个开源的高性能键值（Key-Value）数据库，常被用作缓存、消息队列和会话存储。本教程将带你从零开始了解 Redis 的核心概念与常用操作。

## 一、Redis 简介

- **内存存储**：数据主要保存在内存中，读写速度极快（可达每秒数十万次操作）。
- **丰富的数据结构**：支持字符串、哈希、列表、集合、有序集合等。
- **持久化**：支持 RDB 快照和 AOF 日志两种方式，重启后可恢复数据。
- **高可用与分布式**：支持主从复制、哨兵（Sentinel）和集群（Cluster）。

## 二、安装与启动

### 1. 使用 Docker 快速启动

```bash
docker run -d --name redis -p 6379:6379 redis:7
```

### 2. 本地安装（以 Ubuntu 为例）

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 3. 连接测试

```bash
redis-cli ping
# 返回 PONG 表示连接成功
```

## 三、常用数据类型与命令

### 1. 字符串（String）

```bash
SET name "redis"
GET name            # 返回 "redis"
INCR counter        # 自增 1
SETEX token 60 abc  # 60 秒后过期
```

### 2. 哈希（Hash）

适合存储对象。

```bash
HSET user:1 name "Alice" age 30
HGET user:1 name    # 返回 "Alice"
HGETALL user:1
```

### 3. 列表（List）

可用于消息队列。

```bash
LPUSH queue task1
RPUSH queue task2
LRANGE queue 0 -1   # 查看全部元素
LPOP queue          # 从左侧弹出
```

### 4. 集合（Set）

无序且不重复。

```bash
SADD tags redis cache
SMEMBERS tags
SISMEMBER tags redis  # 判断是否存在
```

### 5. 有序集合（Sorted Set）

带分数排序，适合排行榜。

```bash
ZADD rank 100 alice
ZADD rank 200 bob
ZRANGE rank 0 -1 WITHSCORES  # 按分数升序
ZREVRANGE rank 0 -1 WITHSCORES  # 按分数降序
```

## 四、键（Key）管理

```bash
KEYS pattern     # 查找键（生产环境慎用）
EXISTS name      # 判断键是否存在
EXPIRE name 60   # 设置过期时间（秒）
TTL name         # 查看剩余过期时间
DEL name         # 删除键
TYPE name        # 查看键的类型
```

## 五、持久化配置

### RDB（快照）

在 `redis.conf` 中配置：

```
save 900 1
save 300 10
save 60 10000
```

### AOF（追加日志）

```
appendonly yes
appendfsync everysec
```

## 六、使用示例（Python）

```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 字符串
r.set("name", "redis")
print(r.get("name"))

# 哈希
r.hset("user:1", mapping={"name": "Alice", "age": 30})
print(r.hgetall("user:1"))

# 列表
r.lpush("queue", "task1", "task2")
print(r.lrange("queue", 0, -1))
```

## 七、最佳实践

1. **合理设置过期时间**：缓存数据应设置 TTL，避免内存无限增长。
2. **避免使用 KEYS**：生产环境用 `SCAN` 代替，防止阻塞。
3. **使用连接池**：减少频繁建立连接的开销。
4. **监控内存**：通过 `INFO memory` 查看内存使用情况。
5. **设置最大内存策略**：如 `maxmemory-policy allkeys-lru`。

## 八、小结

本教程介绍了 Redis 的基本概念、安装方式、常用数据类型与命令、持久化配置以及实践建议。掌握这些内容后，你可以进一步学习 Redis 的事务、发布订阅、Lua 脚本和集群部署。

> 官方文档：https://redis.io/docs/
