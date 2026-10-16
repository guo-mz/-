# Spring Boot 详细教程

> 本教程基于 **Spring Boot 3.2.x**（Java 17+）编写，示例代码可直接复制运行。
> 阅读前建议具备 Java 基础与 Maven 基本使用经验。

## 目录

1. [Spring Boot 是什么](#1-spring-boot-是什么)
2. [环境准备](#2-环境准备)
3. [创建第一个项目](#3-创建第一个项目)
4. [项目结构解析](#4-项目结构解析)
5. [核心概念](#5-核心概念)
6. [编写 REST 接口](#6-编写-rest-接口)
7. [配置管理](#7-配置管理)
8. [数据访问](#8-数据访问)
9. [参数校验与异常处理](#9-参数校验与异常处理)
10. [测试](#10-测试)
11. [打包与部署](#11-打包与部署)
12. [进阶主题](#12-进阶主题)
13. [常见问题](#13-常见问题)

---

## 1. Spring Boot 是什么

Spring Boot 是 Spring 生态的脚手架框架，目标是**让 Spring 应用开箱即用**。它的核心能力：

- **自动配置（Auto-configuration）**：根据 classpath 上的依赖自动装配 Bean。
- **起步依赖（Starter）**：一组约定好的依赖集合，如 `spring-boot-starter-web`。
- **内嵌容器**：内置 Tomcat / Jetty / Undertow，打成 jar 即可运行。
- **外部化配置**：通过 `application.yml`、环境变量、命令行参数覆盖配置。
- **生产级特性**：健康检查、指标、日志等（Actuator）。

### 与原生 Spring 的对比

| 维度 | 原生 Spring | Spring Boot |
| --- | --- | --- |
| 配置方式 | 大量 XML / Java Config | 自动配置 + 少量属性 |
| 部署 | 打 war 部署到容器 | 内嵌容器，`java -jar` |
| 依赖管理 | 手动指定版本 | Starter 统一版本 |
| 上手成本 | 较高 | 较低 |

---

## 2. 环境准备

| 工具 | 版本要求 |
| --- | --- |
| JDK | 17 或更高（Spring Boot 3.x 最低 17） |
| Maven | 3.6+ 或 Gradle 7.5+ |
| IDE | IntelliJ IDEA / VS Code + Java 插件 |

验证环境：

```bash
java -version
mvn -v
```

---

## 3. 创建第一个项目

### 3.1 使用 Spring Initializr

访问 <https://start.spring.io>，选择：

- Project：Maven
- Language：Java
- Spring Boot：3.2.x
- Java：17
- Dependencies：Spring Web、Spring Boot DevTools

下载解压后即可导入 IDE。

### 3.2 使用命令行

```bash
curl https://start.spring.io/starter.zip \
  -d dependencies=web,devtools \
  -d type=maven-project \
  -d javaVersion=17 \
  -d bootVersion=3.2.5 \
  -o demo.zip
unzip demo.zip -d demo
```

### 3.3 手动编写 pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.5</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### 3.4 启动类

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

运行 `main` 方法，控制台出现 `Started DemoApplication` 即启动成功，默认端口 `8080`。

---

## 4. 项目结构解析

```
demo/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── DemoApplication.java      # 启动类
│   │   │   ├── controller/               # 接口层
│   │   │   ├── service/                  # 业务层
│   │   │   ├── repository/               # 数据访问层
│   │   │   └── entity/                   # 实体类
│   │   └── resources/
│   │       ├── application.yml           # 配置文件
│   │       ├── static/                   # 静态资源
│   │       └── templates/                # 模板文件
│   └── test/java/com/example/demo/       # 测试代码
└── target/                               # 构建产物
```

**约定优于配置**：`@SpringBootApplication` 所在包及其子包会被自动扫描。

---

## 5. 核心概念

### 5.1 依赖注入（DI）

```java
@Service
public class GreetingService {
    public String greet(String name) {
        return "Hello, " + name + "!";
    }
}

@RestController
public class GreetingController {

    private final GreetingService greetingService;

    // 构造器注入（推荐）
    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }
}
```

### 5.2 常用注解

| 注解 | 作用 |
| --- | --- |
| `@SpringBootApplication` | 启动类组合注解 |
| `@Component` | 通用组件 |
| `@Service` | 业务层组件 |
| `@Repository` | 数据访问层组件 |
| `@RestController` | REST 控制器 |
| `@Configuration` | 配置类 |
| `@Bean` | 声明 Bean |
| `@Value` | 注入配置值 |
| `@ConfigurationProperties` | 批量绑定配置 |

### 5.3 Bean 作用域

- `singleton`（默认）：容器内单例。
- `prototype`：每次获取创建新实例。
- `request` / `session`：Web 场景。

```java
@Component
@Scope("prototype")
public class Task { }
```

---

## 6. 编写 REST 接口

### 6.1 基础接口

```java
package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public List<Map<String, Object>> list() {
        return List.of(
            Map.of("id", 1, "name", "Alice"),
            Map.of("id", 2, "name", "Bob")
        );
    }

    @GetMapping("/{id}")
    public Map<String, Object> getById(@PathVariable Long id) {
        return Map.of("id", id, "name", "User-" + id);
    }

    @PostMapping
    public Map<String, Object> create(@RequestBody Map<String, Object> body) {
        return Map.of("id", 100, "name", body.get("name"));
    }

    @PutMapping("/{id}")
    public Map<String, Object> update(@PathVariable Long id,
                                      @RequestBody Map<String, Object> body) {
        return Map.of("id", id, "name", body.get("name"));
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        // 删除逻辑
    }
}
```

### 6.2 请求参数

```java
@GetMapping("/search")
public List<String> search(@RequestParam(defaultValue = "") String keyword,
                           @RequestParam(defaultValue = "1") int page) {
    return List.of("keyword=" + keyword, "page=" + page);
}
```

### 6.3 返回统一响应体

```java
public record ApiResponse<T>(int code, String message, T data) {

    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(0, "success", data);
    }

    public static <T> ApiResponse<T> fail(String message) {
        return new ApiResponse<>(-1, message, null);
    }
}
```

---

## 7. 配置管理

### 7.1 application.yml

```yaml
server:
  port: 8080
  servlet:
    context-path: /

spring:
  application:
    name: demo
  profiles:
    active: dev

app:
  name: MyApp
  max-connections: 100
```

### 7.2 多环境配置

- `application-dev.yml`
- `application-prod.yml`

通过 `spring.profiles.active` 或启动参数切换：

```bash
java -jar demo.jar --spring.profiles.active=prod
```

### 7.3 读取配置

方式一：`@Value`

```java
@Component
public class AppInfo {

    @Value("${app.name}")
    private String name;

    @Value("${app.max-connections:50}")
    private int maxConnections;
}
```

方式二：`@ConfigurationProperties`（推荐）

```java
@Component
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private String name;
    private int maxConnections = 50;

    // getter / setter 省略
}
```

---

## 8. 数据访问

### 8.1 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

### 8.2 实体类

```java
package com.example.demo.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    // getter / setter 省略
}
```

### 8.3 Repository

```java
package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByName(String name);
}
```

### 8.4 配置数据源

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

### 8.5 Service 层

```java
@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public User save(User user) {
        return userRepository.save(user);
    }

    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }
}
```

---

## 9. 参数校验与异常处理

### 9.1 参数校验

引入依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

```java
public record CreateUserRequest(
        @NotBlank(message = "name 不能为空") String name,
        @Email(message = "email 格式不正确") String email) {
}

@PostMapping
public ApiResponse<String> create(@Valid @RequestBody CreateUserRequest req) {
    return ApiResponse.ok("created: " + req.name());
}
```

### 9.2 全局异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ApiResponse<Void> handleValidation(MethodArgumentNotValidException ex) {
        String msg = ex.getBindingResult().getFieldErrors().stream()
                .map(e -> e.getField() + ": " + e.getDefaultMessage())
                .findFirst()
                .orElse("参数错误");
        return ApiResponse.fail(msg);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ApiResponse<Void> handleOther(Exception ex) {
        return ApiResponse.fail(ex.getMessage());
    }
}
```

---

## 10. 测试

### 10.1 单元测试

```java
@SpringBootTest
class UserServiceTest {

    @Autowired
    private UserService userService;

    @Test
    void saveAndFind() {
        User user = new User();
        user.setName("Alice");
        user.setEmail("alice@example.com");
        userService.save(user);

        assertTrue(userService.findByEmail("alice@example.com").isPresent());
    }
}
```

### 10.2 接口测试

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void listUsers() throws Exception {
        mockMvc.perform(get("/api/users"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Alice"));
    }
}
```

运行测试：

```bash
mvn test
```

---

## 11. 打包与部署

### 11.1 打包

```bash
mvn clean package
```

产物位于 `target/demo-0.0.1-SNAPSHOT.jar`。

### 11.2 运行

```bash
java -jar target/demo-0.0.1-SNAPSHOT.jar
```

### 11.3 常用启动参数

```bash
java -jar demo.jar \
  --server.port=9090 \
  --spring.profiles.active=prod
```

### 11.4 Docker 部署

```dockerfile
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY target/demo-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

```bash
docker build -t demo:1.0 .
docker run -p 8080:8080 demo:1.0
```

---

## 12. 进阶主题

### 12.1 拦截器

```java
@Component
public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        String token = request.getHeader("Authorization");
        return token != null && !token.isBlank();
    }
}

@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final AuthInterceptor authInterceptor;

    public WebConfig(AuthInterceptor authInterceptor) {
        this.authInterceptor = authInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/public/**");
    }
}
```

### 12.2 定时任务

```java
@EnableScheduling
@Configuration
public class ScheduleConfig { }

@Component
public class ReportTask {

    @Scheduled(cron = "0 0 2 * * ?")
    public void generateDailyReport() {
        System.out.println("生成日报...");
    }
}
```

### 12.3 异步任务

```java
@EnableAsync
@Configuration
public class AsyncConfig { }

@Service
public class MailService {

    @Async
    public void send(String to) {
        // 耗时操作
    }
}
```

### 12.4 Actuator 健康检查

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

访问 `http://localhost:8080/actuator/health` 查看健康状态。

### 12.5 日志配置

```yaml
logging:
  level:
    root: INFO
    com.example.demo: DEBUG
  file:
    name: logs/app.log
```

---

## 13. 常见问题

**Q1：端口被占用怎么办？**

```yaml
server:
  port: 8081
```

或启动时指定 `--server.port=8081`。

**Q2：如何热更新？**

引入 `spring-boot-devtools`，修改代码后重新编译即可自动重启。

**Q3：`@Autowired` 注入为 null？**

检查该类是否被 Spring 管理（是否加了 `@Component` / `@Service` 等注解），以及是否在扫描包范围内。

**Q4：如何自定义自动配置？**

在 `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 中声明配置类全限定名。

**Q5：Spring Boot 2.x 升级到 3.x 需要注意什么？**

- JDK 最低 17。
- `javax.*` 迁移到 `jakarta.*`。
- 部分配置项 key 变更，参考官方迁移指南。

---

## 参考资源

- 官方文档：<https://docs.spring.io/spring-boot/docs/current/reference/html/>
- Spring Initializr：<https://start.spring.io>
- Spring Guides：<https://spring.io/guides>
