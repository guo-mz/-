# Vue 3 组合式 API 教程

本教程介绍 Vue 3 的组合式 API（Composition API），帮助你理解如何在 `<script setup>` 中组织状态、计算属性、副作用与可复用逻辑。

> 说明：本文件已重命名为 `demo/vue.md`，请使用新路径访问。

## 环境准备

如果还没有 Vue 项目，可以使用 Vite 快速初始化：

```bash
npm create vite@latest my-app -- --template vue
cd my-app
npm install
npm run dev
```

## setup 语法糖

`<script setup>` 是组合式 API 的编译时语法糖，顶层声明的变量、函数会自动暴露给模板，无需 `return`。

```vue
<script setup>
import { ref } from 'vue'

const msg = ref('Hello Vue 3')
</script>

<template>
  <p>{{ msg }}</p>
</template>
```

## ref 与 reactive

`ref` 用于定义任意类型的响应式数据，通过 `.value` 访问；`reactive` 用于定义对象类型的响应式数据，直接访问属性。

```vue
<script setup>
import { ref, reactive } from 'vue'

const count = ref(0)
const state = reactive({ name: 'Vue', version: 3 })

function increment() {
  count.value++
}
</script>

<template>
  <p>当前计数：{{ count }}</p>
  <button @click="increment">加一</button>
  <p>{{ state.name }} {{ state.version }}</p>
</template>
```

## computed

`computed` 用于定义计算属性，它会根据依赖自动缓存，只有依赖变化时才重新计算。

```vue
<script setup>
import { ref, computed } from 'vue'

const firstName = ref('三')
const lastName = ref('张')

const fullName = computed(() => lastName.value + firstName.value)
</script>

<template>
  <p>姓名：{{ fullName }}</p>
</template>
```

## watch 与 watchEffect

`watch` 用于监听指定的响应式数据源，`watchEffect` 会自动收集依赖并立即执行。

```vue
<script setup>
import { ref, watch, watchEffect } from 'vue'

const keyword = ref('')
const result = ref('')

watch(keyword, (newVal, oldVal) => {
  console.log(`从 ${oldVal} 变为 ${newVal}`)
})

watchEffect(() => {
  result.value = keyword.value ? `搜索：${keyword.value}` : ''
})
</script>

<template>
  <input v-model="keyword" placeholder="输入关键词" />
  <p>{{ result }}</p>
</template>
```

## 生命周期钩子

组合式 API 提供与选项式 API 对应的生命周期钩子，如 `onMounted`、`onUpdated`、`onUnmounted` 等，需在 `setup` 中同步调用。

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const width = ref(window.innerWidth)

function handleResize() {
  width.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <p>窗口宽度：{{ width }}</p>
</template>
```

## provide 与 inject

`provide` 与 `inject` 用于跨层级传递数据，避免逐层传递 props。

```vue
<script setup>
import { provide, inject, ref } from 'vue'

const theme = ref('light')
provide('theme', theme)
</script>

<template>
  <Child />
</template>
```

```vue
<script setup>
import { inject } from 'vue'

const theme = inject('theme', 'light')
</script>

<template>
  <button :class="theme">按钮</button>
</template>
```

## 模板引用

使用 `ref` 声明模板引用，配合 `useTemplateRef` 或同名变量即可访问 DOM 节点或子组件实例。

```vue
<script setup>
import { ref } from 'vue'

const inputRef = ref(null)

function focusInput() {
  inputRef.value.focus()
}
</script>

<template>
  <input ref="inputRef" type="text" />
  <button @click="focusInput">聚焦输入框</button>
</template>
```

## 自定义组合函数（Composables）

组合函数是以 `use` 开头的函数，用于复用组件之间的状态逻辑。

```js
import { ref, onMounted, onUnmounted } from 'vue'

export function useWindowWidth() {
  const width = ref(window.innerWidth)

  function handleResize() {
    width.value = window.innerWidth
  }

  onMounted(() => window.addEventListener('resize', handleResize))
  onUnmounted(() => window.removeEventListener('resize', handleResize))

  return width
}
```

在组件中使用：

```vue
<script setup>
import { useWindowWidth } from './composables/useWindowWidth'

const width = useWindowWidth()
</script>

<template>
  <p>窗口宽度：{{ width }}</p>
</template>
```

## 小结

- `setup` 语法糖：组织组件逻辑，自动暴露顶层绑定。
- `ref` / `reactive`：定义响应式数据。
- `computed`：定义带缓存的计算属性。
- `watch` / `watchEffect`：监听响应式数据变化。
- 生命周期钩子：在 `setup` 中注册 `onMounted` 等钩子。
- `provide` / `inject`：跨层级传递数据。
- 模板引用：访问 DOM 节点或子组件实例。
- 自定义组合函数：复用状态逻辑。
