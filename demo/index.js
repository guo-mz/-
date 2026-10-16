// demo/aa.js
// 一个简单的 JavaScript 示例文件

// 变量声明
const greeting = 'Hello, World!';
let counter = 0;

// 函数定义
function greet(name) {
  return `Hello, ${name}!`;
}

// 箭头函数
const add = (a, b) => a + b;

// 控制台输出
console.log(greeting);
console.log(greet('Coding Agent'));
console.log('1 + 2 =', add(1, 2));

// 简单循环
for (let i = 0; i < 3; i++) {
  counter += i;
}
console.log('counter =', counter);

// 数组操作
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map((n) => n * 2);
console.log('doubled =', doubled);

// 导出（便于在其他模块中使用）
module.exports = { greet, add };
