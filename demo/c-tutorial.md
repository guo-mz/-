# C 语言教程

## 1. 简介

C 语言是一种通用的、过程式的编程语言，由 Dennis Ritchie 于 1972 年在贝尔实验室开发。它兼具高级语言的可读性与低级语言的内存操作能力，是操作系统、嵌入式系统和高性能软件的核心语言之一。

## 2. 第一个程序

```c
#include <stdio.h>

int main(void) {
    printf("Hello, World!\n");
    return 0;
}
```

编译与运行：

```bash
gcc hello.c -o hello
./hello
```

## 3. 基本数据类型

| 类型 | 说明 | 典型大小 |
| --- | --- | --- |
| `char` | 字符/小整数 | 1 字节 |
| `int` | 整数 | 4 字节 |
| `float` | 单精度浮点数 | 4 字节 |
| `double` | 双精度浮点数 | 8 字节 |
| `void` | 无类型 | — |

修饰符：`short`、`long`、`signed`、`unsigned`。

## 4. 变量与常量

```c
int count = 10;          // 变量
const double PI = 3.14159; // 常量
#define MAX 100          // 宏常量
```

## 5. 运算符

- 算术：`+ - * / %`
- 关系：`== != > < >= <=`
- 逻辑：`&& || !`
- 位运算：`& | ^ ~ << >>`
- 赋值：`= += -= *= /= %=`
- 自增自减：`++ --`

## 6. 控制结构

### 条件语句

```c
if (score >= 60) {
    printf("及格\n");
} else {
    printf("不及格\n");
}

switch (grade) {
    case 'A': printf("优秀\n"); break;
    case 'B': printf("良好\n"); break;
    default:  printf("其他\n"); break;
}
```

### 循环语句

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}

int n = 0;
while (n < 5) {
    n++;
}

do {
    n--;
} while (n > 0);
```

## 7. 函数

```c
int add(int a, int b) {
    return a + b;
}

int main(void) {
    printf("%d\n", add(3, 4));
    return 0;
}
```

函数声明（原型）可放在头文件或使用之前：

```c
int add(int a, int b);
```

## 8. 数组与字符串

```c
int nums[5] = {1, 2, 3, 4, 5};
char name[] = "Alice"; // 以 '\0' 结尾
```

字符串常用函数（`<string.h>`）：`strlen`、`strcpy`、`strcmp`、`strcat`。

## 9. 指针

指针保存变量的内存地址。

```c
int x = 42;
int *p = &x;
printf("%d\n", *p); // 解引用，输出 42
*p = 100;            // 通过指针修改 x
```

指针与数组关系密切：`nums[i]` 等价于 `*(nums + i)`。

## 10. 结构体

```c
struct Point {
    int x;
    int y;
};

struct Point p = {3, 4};
printf("%d, %d\n", p.x, p.y);
```

## 11. 动态内存管理

```c
#include <stdlib.h>

int *arr = malloc(10 * sizeof(int));
if (arr == NULL) {
    return 1;
}
// 使用 arr ...
free(arr);
```

常用函数：`malloc`、`calloc`、`realloc`、`free`。务必成对释放，避免内存泄漏。

## 12. 文件操作

```c
#include <stdio.h>

FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("fopen");
    return 1;
}

char buf[256];
while (fgets(buf, sizeof(buf), fp) != NULL) {
    printf("%s", buf);
}
fclose(fp);
```

## 13. 预处理器

```c
#include <stdio.h>
#define SQUARE(x) ((x) * (x))

#ifdef DEBUG
    printf("debug mode\n");
#endif
```

## 14. 编译与调试

```bash
gcc -Wall -Wextra -g main.c -o main   # 编译并生成调试信息
gdb ./main                            # 使用 GDB 调试
valgrind ./main                       # 检查内存问题
```

## 15. 常见陷阱

- 数组越界访问导致未定义行为。
- 忘记初始化指针就解引用。
- `malloc` 后未检查返回值或未 `free`。
- 字符串未以 `'\0'` 结尾。
- `scanf` 读取字符串时未限制长度（应使用 `%ns`）。

## 16. 学习建议

1. 多动手写代码，从简单程序开始。
2. 理解内存模型与指针，这是 C 语言的核心。
3. 阅读经典书籍，如《C 程序设计语言》（K&R）。
4. 使用 `-Wall -Wextra` 编译选项，养成良好习惯。
5. 学习使用调试器与内存检查工具。
