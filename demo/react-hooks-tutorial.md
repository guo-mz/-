# React Hooks 教程

本教程介绍 React 的核心 Hooks，帮助你理解函数组件中状态管理与副作用处理的方式。

## 环境准备

如果还没有 React 项目，可以使用 Vite 快速初始化：

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

## useState

`useState` 用于在函数组件中添加状态。

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>当前计数：{count}</p>
      <button onClick={() => setCount(count + 1)}>加一</button>
    </div>
  );
}
```

## useEffect

`useEffect` 用于处理副作用，例如数据请求、订阅和手动修改 DOM。

```jsx
import { useEffect, useState } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then((res) => res.json())
      .then((data) => setUsers(data));
  }, []);

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## useContext

`useContext` 用于读取 React Context 的值，避免逐层传递 props。

```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

function Button() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>按钮</button>;
}
```

## useReducer

`useReducer` 适合管理包含多个子值的复杂状态逻辑。

```jsx
import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>计数：{state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>加一</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>减一</button>
    </div>
  );
}
```

## useRef

`useRef` 返回一个可变的 ref 对象，常用于访问 DOM 节点或保存不触发渲染的值。

```jsx
import { useRef } from 'react';

function TextInput() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>聚焦输入框</button>
    </div>
  );
}
```

## useMemo

`useMemo` 用于缓存计算结果，避免在每次渲染时重复执行昂贵的计算。

```jsx
import { useMemo, useState } from 'react';

function ExpensiveList({ items }) {
  const [filter, setFilter] = useState('');

  const filteredItems = useMemo(() => {
    return items.filter((item) => item.includes(filter));
  }, [items, filter]);

  return (
    <div>
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      <ul>
        {filteredItems.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

## useCallback

`useCallback` 用于缓存函数引用，常与 `React.memo` 配合优化子组件渲染。

```jsx
import { useCallback, useState } from 'react';

function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  return <Child onClick={handleClick} count={count} />;
}

function Child({ onClick, count }) {
  return <button onClick={onClick}>点击次数：{count}</button>;
}
```

## 自定义 Hook

自定义 Hook 是以 `use` 开头的函数，可以复用组件之间的状态逻辑。

```jsx
import { useState, useEffect } from 'react';

function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return width;
}
```

## 小结

- `useState`：管理组件状态。
- `useEffect`：处理副作用。
- `useContext`：读取上下文。
- `useReducer`：管理复杂状态逻辑。
- `useRef`：保存可变引用。
- `useMemo`：缓存计算结果。
- `useCallback`：缓存函数引用。
- 自定义 Hook：复用状态逻辑。
