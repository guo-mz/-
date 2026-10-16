# LangChain 入门教程

LangChain 是一个用于构建大语言模型（LLM）应用的开发框架。它把模型调用、提示词管理、外部数据接入和流程编排抽象成可组合的模块，让开发者能更快地搭建聊天机器人、检索问答、自动化 Agent 等应用。

本教程面向初学者，介绍 LangChain 的核心概念，并给出一个最小可运行示例。

## 一、核心概念

### 1. LLM（大语言模型）

LLM 是 LangChain 的推理核心，负责根据输入文本生成输出文本。LangChain 通过统一的接口封装不同厂商的模型，例如 OpenAI、Anthropic 以及本地部署的模型。

- `LLM`：输入字符串，输出字符串，适合单轮补全。
- `ChatModel`：输入消息列表，输出消息，适合多轮对话。

### 2. Prompt（提示词）

Prompt 是发送给模型的输入。LangChain 提供 `PromptTemplate` 等工具，把变量填充进模板，避免手工拼接字符串。

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("用一句话解释什么是 {topic}。")
print(prompt.format(topic="向量数据库"))
```

### 3. Chain（链）

Chain 把多个组件按顺序连接起来，例如「提示词 → 模型 → 输出解析」。LangChain 表达式语言（LCEL）用管道符 `|` 组合组件，代码直观且支持流式输出。

```python
chain = prompt | model | output_parser
result = chain.invoke({"topic": "LangChain"})
```

### 4. Agent（智能体）

Agent 让模型自行决定调用哪些工具、按什么顺序执行。它适合需要多步推理或访问外部系统的任务，例如查询天气、检索数据库、调用计算器。

## 二、环境准备

建议使用 Python 3.9 及以上版本，并在虚拟环境中安装依赖。

```bash
python -m venv .venv
source .venv/bin/activate   # Windows 使用 .venv\Scripts\activate
pip install langchain langchain-core
```

如果使用在线模型服务，需要配置对应的 API Key 环境变量，例如：

```bash
export OPENAI_API_KEY="你的密钥"
```

> 注意：请勿把密钥写入代码或提交到版本库。

## 三、最小可运行示例

下面示例使用提示词模板和聊天模型，完成一次简单的问答。

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的助手。"),
    ("human", "请用一句话介绍 {topic}。"),
])

# 2. 选择模型（此处以 OpenAI 为例，可按需替换）
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. 组合成链
chain = prompt | model | StrOutputParser()

# 4. 调用
answer = chain.invoke({"topic": "LangChain"})
print(answer)
```

运行后，模型会返回一句关于 LangChain 的简介。你可以把 `topic` 换成其他关键词，观察输出变化。

## 四、常见问题

**Q：必须使用在线模型吗？**

不是。LangChain 也支持本地模型，只要接入对应的封装类即可。

**Q：`langchain` 和 `langchain-core` 有什么区别？**

`langchain-core` 提供基础抽象与接口，`langchain` 提供更高层的组件和集成。入门时两者一起安装即可。

**Q：示例报错找不到模块怎么办？**

确认虚拟环境已激活，并检查依赖是否安装成功。不同模型提供商可能需要额外安装对应的集成包。

## 五、下一步

- 阅读官方文档，了解 LCEL 的更多用法。
- 尝试接入向量数据库，构建检索增强生成（RAG）应用。
- 为 Agent 添加自定义工具，完成更复杂的自动化任务。
