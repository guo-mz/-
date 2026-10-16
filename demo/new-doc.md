# Java 进阶教学文档

## 1. 简介

Java 是一种面向对象的通用编程语言，由 James Gosling 于 1995 年在 Sun Microsystems（现属 Oracle）发布。它遵循「一次编写，到处运行」的理念，通过 JVM（Java 虚拟机）实现跨平台，广泛应用于企业级后端、Android 开发、大数据与云计算等领域。

本文档面向已掌握 Java 基础语法的读者，重点讲解进阶主题。

## 2. 环境与工具链

```bash
# 查看版本
java -version
javac -version

# 编译与运行
javac -d out src/com/example/Main.java
java -cp out com.example.Main
```

常用工具：

- 构建工具：Maven、Gradle
- IDE：IntelliJ IDEA、Eclipse、VS Code
- 诊断工具：jps、jstack、jmap、jconsole、VisualVM

## 3. 面向对象进阶

### 3.1 抽象类与接口

```java
public abstract class Shape {
    protected String name;

    public Shape(String name) {
        this.name = name;
    }

    public abstract double area();

    public String getName() {
        return name;
    }
}

public interface Drawable {
    void draw();

    // Java 8+ 默认方法
    default void describe() {
        System.out.println("这是一个可绘制对象");
    }
}

public class Circle extends Shape implements Drawable {
    private final double radius;

    public Circle(double radius) {
        super("Circle");
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }

    @Override
    public void draw() {
        System.out.println("绘制圆形，半径 " + radius);
    }
}
```

### 3.2 内部类与枚举

```java
public class Outer {
    private int value = 10;

    // 成员内部类
    class Inner {
        int getValue() {
            return value;
        }
    }

    // 静态嵌套类
    static class Nested {
        void hello() {
            System.out.println("Nested");
        }
    }
}

public enum Status {
    PENDING("待处理"),
    RUNNING("运行中"),
    DONE("已完成");

    private final String label;

    Status(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
```

## 4. 泛型

```java
public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

// 泛型方法
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

// 通配符
public static void printAll(List<? extends Number> list) {
    for (Number n : list) {
        System.out.println(n);
    }
}
```

要点：

- 类型擦除：泛型信息在运行时被擦除，无法 `new T[]`。
- `? extends T` 用于读取（生产者），`? super T` 用于写入（消费者）。
- 泛型不支持基本类型，需使用包装类。

## 5. 集合框架

### 5.1 常用集合

```java
List<String> list = new ArrayList<>();
list.add("Java");
list.add("Kotlin");

Set<Integer> set = new HashSet<>();
set.add(1);
set.add(1); // 重复元素不会被加入

Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.putIfAbsent("Bob", 88);
```

### 5.2 选择建议

| 需求 | 推荐实现 |
| --- | --- |
| 随机访问多 | ArrayList |
| 频繁头尾插入删除 | ArrayDeque |
| 去重 | HashSet |
| 有序去重 | TreeSet |
| 键值查找 | HashMap |
| 有序键值 | TreeMap |
| 线程安全 | ConcurrentHashMap |

### 5.3 遍历与 Stream

```java
List<String> names = List.of("Alice", "Bob", "Charlie");

// 增强 for
for (String name : names) {
    System.out.println(name);
}

// Stream
List<String> upper = names.stream()
        .filter(n -> n.length() > 3)
        .map(String::toUpperCase)
        .sorted()
        .collect(Collectors.toList());
```

## 6. 异常处理

```java
try (BufferedReader reader = new BufferedReader(new FileReader("data.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.err.println("读取失败: " + e.getMessage());
} finally {
    System.out.println("处理结束");
}
```

- 受检异常（checked）必须处理或声明抛出。
- 运行时异常（unchecked）通常表示编程错误。
- 自定义异常应继承 `Exception` 或 `RuntimeException`。
- 不要吞掉异常，避免空的 catch 块。

## 7. 并发编程

### 7.1 线程基础

```java
Thread t = new Thread(() -> System.out.println("运行中: " + Thread.currentThread().getName()));
t.start();
t.join();
```

### 7.2 线程池

```java
ExecutorService pool = Executors.newFixedThreadPool(4);

Future<Integer> future = pool.submit(() -> {
    Thread.sleep(100);
    return 42;
});

System.out.println(future.get());
pool.shutdown();
```

### 7.3 同步与锁

```java
public class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public int get() {
        return count;
    }
}
```

### 7.4 并发工具类

- `AtomicInteger`：无锁原子操作
- `CountDownLatch`：等待多个任务完成
- `CyclicBarrier`：多线程互相等待
- `ConcurrentHashMap`：高并发映射
- `CompletableFuture`：异步编排

```java
CompletableFuture<String> cf = CompletableFuture
        .supplyAsync(() -> "hello")
        .thenApply(String::toUpperCase)
        .thenApply(s -> s + " world");

System.out.println(cf.get());
```

## 8. JVM 与内存管理

### 8.1 运行时数据区

- 堆（Heap）：对象实例，线程共享，是 GC 主要区域。
- 虚拟机栈（Stack）：方法调用栈帧，线程私有。
- 方法区 / 元空间（Metaspace）：类元信息。
- 程序计数器：当前执行字节码位置。
- 本地方法栈：native 方法调用。

### 8.2 垃圾回收

常见收集器：Serial、Parallel、CMS、G1、ZGC。

```bash
# 常用 JVM 参数
java -Xms512m -Xmx2g -XX:+UseG1GC -XX:+PrintGCDetails -jar app.jar
```

### 8.3 类加载

加载 → 验证 → 准备 → 解析 → 初始化，由双亲委派模型保证核心类安全。

## 9. 反射与注解

```java
Class<?> clazz = Class.forName("com.example.Circle");
Object instance = clazz.getDeclaredConstructor(double.class).newInstance(2.0);
Method area = clazz.getMethod("area");
System.out.println(area.invoke(instance));
```

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Loggable {
    String value() default "";
}
```

反射灵活但性能较低，且破坏封装，应谨慎使用。

## 10. I/O 与 NIO

```java
// 传统 I/O
Files.writeString(Path.of("out.txt"), "hello", StandardCharsets.UTF_8);
String content = Files.readString(Path.of("out.txt"));

// NIO 通道
try (FileChannel channel = FileChannel.open(Path.of("out.txt"), StandardOpenOption.READ)) {
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    while (channel.read(buffer) > 0) {
        buffer.flip();
        while (buffer.hasRemaining()) {
            System.out.print((char) buffer.get());
        }
        buffer.clear();
    }
}
```

## 11. 现代 Java 特性

- Java 8：Lambda、Stream、Optional、默认方法
- Java 9：模块系统（JPMS）、`var` 之前的集合工厂方法
- Java 10：局部变量类型推断 `var`
- Java 11：`HttpClient`、`String` 新方法
- Java 14+：`switch` 表达式、`record`
- Java 17：密封类（sealed）、模式匹配 `instanceof`
- Java 21：虚拟线程、模式匹配 `switch`

```java
public record Point(int x, int y) {}

sealed interface Vehicle permits Car, Bike {}
record Car(String model) implements Vehicle {}
record Bike(String model) implements Vehicle {}

// 虚拟线程（Java 21）
Thread vt = Thread.ofVirtual().start(() -> System.out.println("virtual thread"));
vt.join();
```

## 12. 常见错误与最佳实践

1. 使用 `equals` 比较对象，而非 `==`。
2. 重写 `equals` 时必须同时重写 `hashCode`。
3. 优先使用接口类型声明变量，如 `List<String>` 而非 `ArrayList<String>`。
4. 避免在循环中拼接字符串，使用 `StringBuilder`。
5. 及时关闭资源，使用 try-with-resources。
6. 避免过度同步，缩小锁的粒度。
7. 使用 `Optional` 表达可能为空的值，减少 NPE。
8. 遵循命名规范：类名大驼峰，方法与变量小驼峰，常量全大写。

## 13. 学习路线建议

1. 巩固语法、集合与异常处理。
2. 深入泛型与函数式编程（Lambda、Stream）。
3. 掌握并发编程与线程池。
4. 理解 JVM 内存模型与 GC 调优。
5. 学习反射、注解与动态代理。
6. 熟悉构建工具与单元测试（JUnit、Mockito）。
7. 通过项目实践：REST 服务、缓存、消息队列。

## 14. 参考资源

- Oracle 官方 Java 文档与教程
- 《Effective Java》（Joshua Bloch）
- 《Java 并发编程实战》
- 《深入理解 Java 虚拟机》（周志明）
- Baeldung、Jenkov 等技术博客
