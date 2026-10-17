# Java 进阶文档

## 1. 引言：从基础到进阶

Java 不仅是一门编程语言，更是一个庞大而成熟的生态系统。掌握 Java 基础（语法、集合、IO、多线程入门）后，进阶学习聚焦于**理解 JVM 底层机制、写出高性能可维护代码、掌握现代开发范式与工程实践**。本文面向已具备 1–2 年 Java 开发经验的工程师，系统梳理核心进阶主题，兼顾深度与实用性。

> ✅ 推荐环境：JDK 17+（LTS）、Maven 3.8+、IDEA 或 VS Code + Java Extension Pack

---

## 2. JVM 深度解析

### 2.1 内存模型与垃圾回收（GC）

JVM 运行时数据区包括：
- **方法区（Metaspace）**：存储类元信息、常量池、静态变量（JDK 8+ 用本地内存替代永久代）；
- **堆（Heap）**：对象实例分配主区域，划分为新生代（Eden + S0/S1）和老年代；
- **虚拟机栈/本地方法栈**：线程私有，保存局部变量、操作数栈、方法调用帧；
- **程序计数器**：记录当前线程执行字节码指令地址。

#### GC 核心算法与收集器对比
| 收集器 | 适用场景 | 特点 |
|--------|----------|------|
| **Serial / Serial Old** | 单核客户端应用 | 简单高效，STW（Stop-The-World）时间长 |
| **Parallel / Parallel Old** | 吞吐优先服务端 | 多线程并行，关注 `-XX:MaxGCPauseMillis` 和 `-XX:GCTimeRatio` |
| **CMS（已废弃）** | 低延迟旧系统 | 并发标记清除，碎片化严重 |
| **G1（推荐）** | 大堆（≥4GB）、可控停顿 | 分区（Region）设计，可预测停顿（`-XX:MaxGCPauseMillis=200`） |
| **ZGC / Shenandoah** | 超大堆（TB级）、亚毫秒停顿 | 基于着色指针/加载屏障，JDK 11+/12+ 特性 |

✅ **调优建议**：
- 使用 `jstat -gc <pid>` 实时监控 GC 频率与耗时；
- 生产环境启用 GC 日志：`-Xlog:gc*:file=gc.log:time,uptime,level,tags`（JDK 10+）；
- 避免频繁创建短生命周期大对象（触发直接晋升老年代）；
- 合理设置 `-Xms` 与 `-Xmx` 相等，避免堆动态扩容开销。

### 2.2 类加载机制与双亲委派

JVM 类加载流程：**加载 → 验证 → 准备 → 解析 → 初始化**。
- **双亲委派模型**：每个 ClassLoader 先委托父加载器加载，仅当父加载失败时才自行加载（保障 `java.lang.Object` 等核心类唯一性）；
- **打破委派场景**：SPI（如 JDBC Driver）、OSGi、热部署框架（Tomcat 自定义 WebAppClassLoader）；
- **自定义 ClassLoader 示例**：
  ```java
  public class CustomClassLoader extends ClassLoader {
      private final String baseDir;
      public CustomClassLoader(String baseDir) {
          this.baseDir = baseDir;
      }
      @Override
      protected Class<?> findClass(String name) throws ClassNotFoundException {
          byte[] bytes = loadClassBytes(name);
          return defineClass(name, bytes, 0, bytes.length);
      }
      private byte[] loadClassBytes(String name) { /* 从文件/网络读取 .class 字节 */ }
  }
  ```

---

## 3. Java 并发编程进阶

### 3.1 JMM（Java Memory Model）与可见性/有序性

- **happens-before 原则**是 JMM 的核心：
  - 程序顺序规则：前序操作 happens-before 后续操作；
  - volatile 规则：对 volatile 写 happens-before 后续对同一变量的读；
  - 锁规则：解锁 happens-before 后续加锁；
  - 线程启动/终止规则等。
- **volatile 关键字**：保证可见性与禁止指令重排序（但不保证原子性）；
- **synchronized / ReentrantLock**：提供互斥 + happens-before 语义；
- **final 字段安全发布**：构造器内 final 字段赋值后，其他线程可见且不可变。

### 3.2 线程池原理与最佳实践

```java
// 推荐创建方式（避免 Executors 工厂方法隐藏风险）
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                // corePoolSize
    16,               // maxPoolSize
    60L, TimeUnit.SECONDS, // keepAliveTime
    new LinkedBlockingQueue<>(100), // workQueue
    new ThreadFactoryBuilder().setNameFormat("biz-task-%d").build(),
    new ThreadPoolExecutor.CallerRunsPolicy() // 拒绝策略
);
```

⚠️ **关键陷阱**：
- `Executors.newFixedThreadPool()` 使用无界队列 → OOM 风险；
- `Executors.newCachedThreadPool()` 无限创建线程 → CPU 耗尽；
- 线程池未 `shutdown()` → JVM 无法退出；
- 任务抛异常未捕获 → 线程 silently 终止。

### 3.3 并发工具类实战

| 工具类 | 场景 | 注意事项 |
|--------|------|-----------|
| `CountDownLatch` | 主线程等待 N 个子任务完成 | 一次性使用，不可重置 |
| `CyclicBarrier` | 多线程互相等待到达栅栏点 | 可重用，支持 barrierAction |
| `Phaser` | 动态注册/注销参与者 | 替代 CountDownLatch/CyclicBarrier 的高级方案 |
| `StampedLock` | 高频读 + 低频写场景 | 支持乐观读（`tryOptimisticRead()`），避免写饥饿 |
| `CompletableFuture` | 异步编排、组合、异常处理 | 避免在 `thenApply` 中阻塞（用 `thenCompose` 替代嵌套） |

---

## 4. Java 8+ 新特性精讲

### 4.1 Lambda 表达式与函数式接口

- **函数式接口**：仅含一个抽象方法（`@FunctionalInterface` 注解）；
- **常见内置接口**：`Predicate<T>`, `Function<T,R>`, `Consumer<T>`, `Supplier<T>`；
- **Lambda 捕获变量**：只能访问 `final` 或事实上的 final 变量；
- **方法引用**：`String::length`, `System.out::println`, `HashMap::new`。

### 4.2 Stream API 高效处理集合

```java
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .distinct()
    .sorted(Comparator.reverseOrder())
    .limit(10)
    .collect(Collectors.toList());

// 并行流慎用：仅适用于计算密集型、无状态操作
long count = numbers.parallelStream().filter(n -> n % 2 == 0).count();
```

✅ **性能提示**：
- 避免在 `map` 中做 IO 或数据库调用；
- `collect(Collectors.groupingBy())` 默认使用 `HashMap`，若需有序请指定 `TreeMap::new`；
- `Collectors.toConcurrentMap()` 用于并发收集（注意 key 冲突处理）。

### 4.3 Optional 与空安全

```java
// ❌ 错误：Optional 不能作为字段或参数类型（违反设计初衷）
public class User { private Optional<String> name; } // 不推荐

// ✅ 正确：仅用于返回值，链式处理
Optional<User> userOpt = userRepository.findById(123);
String name = userOpt.map(User::getName)
    .filter(n -> n.length() > 2)
    .orElse("Anonymous");
```

---

## 5. Spring Boot 进阶实践

### 5.1 自动配置原理（@SpringBootApplication）

- `@SpringBootApplication = @Configuration + @EnableAutoConfiguration + @ComponentScan`；
- `@EnableAutoConfiguration` 通过 `spring.factories` 加载 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（Spring Boot 2.7+）；
- 条件化装配：`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`；
- 自定义 Starter 示例：
  ```java
  // 定义自动配置类
  @Configuration(proxyBeanMethods = false)
  @ConditionalOnClass(MyService.class)
  public class MyAutoConfiguration {
      @Bean
      @ConditionalOnMissingBean
      public MyService myService() { return new MyService(); }
  }
  // 在 resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports 中添加全限定名
  ```

### 5.2 Spring AOP 与代理机制

- **JDK 动态代理**：基于接口，生成 `Proxy` 子类；
- **CGLIB 代理**：基于类，生成子类（需 `@EnableAspectJAutoProxy(proxyTargetClass=true)`）；
- **切点表达式**：`execution(* com.example.service..*.*(..))`；
- **事务传播行为**：`REQUIRED`（默认）、`REQUIRES_NEW`（新建事务）、`NESTED`（嵌套事务）；
- **事务失效场景**：
  - 自调用（this.method()）；
  - 非 public 方法；
  - 异常被 try-catch 吞没；
  - 未配置 `@Transactional` 或事务管理器未生效。

---

## 6. 性能优化与诊断

### 6.1 火焰图（Flame Graph）分析 CPU 热点

1. 使用 `async-profiler` 采集：
   ```bash
   ./profiler.sh -e cpu -d 30 -f profile.html <pid>
   ```
2. 分析 `profile.html`：定位 `HashMap.get()`、`String.substring()` 等高频调用栈；
3. 优化方向：缓存、算法降维（如用布隆过滤器预判）、减少对象创建。

### 6.2 内存泄漏排查（MAT / JProfiler）

- **常见泄漏源**：
  - 静态集合持有对象引用（如 `static Map<String, Object>`）；
  - 未关闭的资源（`InputStream`, `Connection`, `ThreadLocal`）；
  - 内部类隐式持有外部类引用（改用静态内部类 + WeakReference）；
- **MAT 快速定位**：
  - `Leak Suspects Report` 自动生成可疑点；
  - `Dominator Tree` 查看谁占用了最多内存；
  - `Path to GC Roots` 追踪强引用链。

---

## 7. 微服务与云原生进阶

- **Spring Cloud Alibaba**：Nacos（服务发现/配置中心）、Sentinel（流量控制）、Seata（分布式事务）；
- **Reactive 编程**：WebFlux + Project Reactor（`Mono`, `Flux`），适合高并发 IO 密集型场景；
- **GraalVM Native Image**：将 Spring Boot 应用编译为本地可执行文件，启动时间 < 100ms，内存占用降低 50%；
- **Kubernetes 部署要点**：
  - JVM 参数适配容器：`-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0`；
  - Liveness/Readiness Probe 设置合理超时；
  - 使用 `ConfigMap`/`Secret` 管理配置，禁用 `application.properties` 硬编码。

---

## 8. 安全与最佳实践

- ✅ **输入校验**：`@Valid` + `@NotBlank` + 自定义约束注解；
- ✅ **SQL 注入防护**：永远使用 `PreparedStatement`（MyBatis `#{}`、JPA `@Param`）；
- ✅ **XSS 防护**：模板引擎自动转义（Thymeleaf `th:text`）、富文本使用 `jsoup` 清洗；
- ✅ **敏感信息加密**：`@Encrypt` 自定义注解 + AOP 加密存储（AES/GCM）；
- ✅ **依赖安全扫描**：`mvn org.owasp:dependency-check-maven:check`；
- ❌ **禁止**：`Runtime.exec()` 执行用户输入命令、`ObjectInputStream` 反序列化不可信数据、硬编码密码/Token。

---

## 9. 常用工具速查

| 工具 | 用途 | 命令示例 |
|------|------|-----------|
| `jps` | 列出 JVM 进程 | `jps -l` |
| `jstack` | 线程快照 | `jstack -l <pid> > thread.log` |
| `jmap` | 堆内存分析 | `jmap -histo:live <pid>` |
| `jcmd` | JVM 命令行诊断 | `jcmd <pid> VM.native_memory summary` |
| `arthas` | 在线诊断神器 | `curl -O https://arthas.aliyun.com/arthas-boot.jar && java -jar arthas-boot.jar` |
| `jfr` (JDK Flight Recorder) | 低开销性能监控 | `java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp` |

---

## 10. 进阶学习路径

1. **底层深入**：《深入理解 Java 虚拟机》（周志明）、《Java 并发编程实战》；
2. **源码阅读**：JDK `java.util.concurrent` 包、Spring Framework 核心模块（`context`, `aop`, `transaction`）；
3. **架构演进**：单体 → 模块化（DDD）→ 微服务 → Service Mesh（Istio）→ Serverless；
4. **技术广度**：Rust（系统编程）、Go（云原生基建）、Python（AI/数据分析）；
5. **软技能**：技术方案设计文档（PRD/ADR）、跨团队协作、技术影响力（分享/开源）。