# C++ 教学文档

## 1. 简介

C++ 是一种通用编程语言，由 Bjarne Stroustrup 于 1979 年在贝尔实验室开始开发。它在 C 语言的基础上增加了面向对象、泛型编程和异常处理等特性，广泛应用于系统软件、游戏引擎、嵌入式开发和高性能计算等领域。

## 2. 第一个程序

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

编译与运行（以 g++ 为例）：

```bash
g++ -std=c++17 -Wall -o hello hello.cpp
./hello
```

## 3. 基本语法

### 3.1 变量与类型

```cpp
int age = 25;              // 整数
 double price = 9.99;      // 双精度浮点
char grade = 'A';          // 字符
bool isReady = true;       // 布尔
std::string name = "Tom";  // 字符串（需 #include <string>）
```

### 3.2 常量与自动类型推导

```cpp
const double PI = 3.14159;
auto count = 10;        // 推导为 int
auto ratio = 0.5;       // 推导为 double
```

### 3.3 控制流

```cpp
if (age >= 18) {
    std::cout << "成年人" << std::endl;
} else {
    std::cout << "未成年人" << std::endl;
}

for (int i = 0; i < 5; ++i) {
    std::cout << i << " ";
}

int i = 0;
while (i < 5) {
    ++i;
}
```

## 4. 函数

```cpp
int add(int a, int b) {
    return a + b;
}

// 默认参数
void greet(const std::string& name = "World") {
    std::cout << "Hello, " << name << "!" << std::endl;
}

// 函数重载
int max(int a, int b) { return a > b ? a : b; }
double max(double a, double b) { return a > b ? a : b; }
```

## 5. 面向对象编程

### 5.1 类与对象

```cpp
class Rectangle {
public:
    Rectangle(double w, double h) : width_(w), height_(h) {}

    double area() const {
        return width_ * height_;
    }

    void setWidth(double w) { width_ = w; }
    double width() const { return width_; }

private:
    double width_;
    double height_;
};

int main() {
    Rectangle rect(3.0, 4.0);
    std::cout << rect.area() << std::endl; // 12
    return 0;
}
```

### 5.2 继承与多态

```cpp
class Shape {
public:
    virtual double area() const = 0;   // 纯虚函数
    virtual ~Shape() = default;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius_(r) {}
    double area() const override {
        return 3.14159 * radius_ * radius_;
    }
private:
    double radius_;
};

void printArea(const Shape& s) {
    std::cout << s.area() << std::endl;
}
```

## 6. 标准库常用组件

### 6.1 容器

```cpp
#include <vector>
#include <map>
#include <string>

std::vector<int> nums = {1, 2, 3};
nums.push_back(4);

std::map<std::string, int> scores;
scores["Alice"] = 95;
```

### 6.2 迭代与算法

```cpp
#include <algorithm>

std::sort(nums.begin(), nums.end());
int total = std::accumulate(nums.begin(), nums.end(), 0);
```

### 6.3 智能指针

```cpp
#include <memory>

std::unique_ptr<Rectangle> rect = std::make_unique<Rectangle>(3.0, 4.0);
std::shared_ptr<Shape> shape = std::make_shared<Circle>(2.0);
```

## 7. 现代 C++ 特性（C++11 及以后）

- `auto` 类型推导
- 范围 for 循环：`for (const auto& x : nums) { ... }`
- Lambda 表达式：`auto f = [](int x) { return x * 2; };`
- 移动语义与右值引用（`std::move`）
- `nullptr` 替代 `NULL`
- `constexpr` 编译期计算

## 8. 常见错误与建议

1. 未初始化变量：始终初始化变量。
2. 内存泄漏：优先使用智能指针和标准容器。
3. 数组越界：使用 `std::vector` 与 `.at()` 进行边界检查。
4. 头文件重复包含：使用 `#pragma once` 或 include guard。
5. 编译警告：开启 `-Wall -Wextra` 并认真处理警告。

## 9. 学习路线建议

1. 掌握基本语法与流程控制。
2. 理解函数、引用与指针。
3. 学习类、继承与多态。
4. 熟悉 STL 容器与算法。
5. 学习现代 C++ 特性与内存管理。
6. 通过小项目（如命令行工具、小游戏）巩固实践。

## 10. 参考资源

- cppreference.com：权威的 C++ 标准库与语言参考。
- 《C++ Primer》：系统学习 C++ 的经典教材。
- 《Effective Modern C++》：现代 C++ 最佳实践。
