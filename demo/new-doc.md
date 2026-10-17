# Python 画图入门文档

## 1. 简介

Python 是数据可视化和科学计算的首选语言之一，其简洁语法与丰富生态（如 Matplotlib、Seaborn、Plotly）让绘图变得直观高效。本文档面向已掌握 Python 基础语法的读者，聚焦常用二维图表绘制方法。

> ✅ 推荐环境：Python ≥ 3.8，安装 `matplotlib`, `seaborn`, `numpy`：
> ```bash
> pip install matplotlib seaborn numpy pandas
> ```

## 2. 快速开始：Matplotlib 基础

### 2.1 折线图（Line Plot）

```python
import matplotlib.pyplot as plt
import numpy as np

# 示例数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='sin(x)', color='blue', linewidth=2)
plt.title('正弦函数图像')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
```

### 2.2 散点图（Scatter Plot）

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.randn(200)
y = 2 * x + np.random.randn(200) * 0.5

plt.figure(figsize=(8, 5))
plt.scatter(x, y, c=y, cmap='viridis', alpha=0.7, s=30)
plt.colorbar(label='y value')
plt.title('散点图：y ≈ 2x + noise')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

## 3. 多子图与布局

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle('2×2 子图示例', fontsize=16)

# 左上：柱状图
axes[0, 0].bar(['A', 'B', 'C'], [3, 7, 5])
axes[0, 0].set_title('柱状图')

# 右上：直方图
data = np.random.normal(0, 1, 1000)
axes[0, 1].hist(data, bins=30, alpha=0.7, color='skyblue')
axes[0, 1].set_title('直方图')

# 左下：饼图
axes[1, 0].pie([40, 30, 20, 10], labels=['Apples', 'Bananas', 'Cherries', 'Dates'], autopct='%1.1f%%')
axes[1, 0].set_title('饼图')

# 右下：箱线图
axes[1, 1].boxplot([np.random.normal(0, 1, 50), np.random.normal(2, 1.5, 50)])
axes[1, 1].set_title('箱线图')
axes[1, 1].set_xticks([1, 2])
axes[1, 1].set_xticklabels(['Group A', 'Group B'])

plt.tight_layout()
plt.show()
```

## 4. 使用 Seaborn 提升美观度

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 加载内置数据集
tips = sns.load_dataset('tips')

plt.figure(figsize=(10, 6))

# 热力图（相关性）
plt.subplot(2, 2, 1)
corr = tips.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('数值列相关性热力图')

# 小提琴图
plt.subplot(2, 2, 2)
sns.violinplot(data=tips, x='day', y='total_bill')
plt.title('按星期分布的账单金额')

# 分类散点图
plt.subplot(2, 2, 3)
sns.stripplot(data=tips, x='sex', y='tip', hue='time')
plt.title('小费 vs 性别（分时段）')

# 回归图
plt.subplot(2, 2, 4)
sns.regplot(data=tips, x='total_bill', y='tip', scatter_kws={'alpha': 0.5})
plt.title('账单总额与小费的线性关系')

plt.tight_layout()
plt.show()
```

## 5. 保存图像

```python
plt.figure(figsize=(6, 4))
plt.plot([1, 2, 3], [1, 4, 2])
plt.title('示例图')

# 保存为高清 PNG（推荐）
plt.savefig('demo_plot.png', dpi=300, bbox_inches='tight')

# 或保存为 PDF（矢量图，适合论文）
plt.savefig('demo_plot.pdf', bbox_inches='tight')

plt.show()
```

## 6. 最佳实践提示

- ✅ 使用 `plt.tight_layout()` 避免标签重叠；
- ✅ 设置 `figsize` 控制画布尺寸；
- ✅ 用 `cmap` 和 `alpha` 提升视觉层次；
- ❌ 避免在循环中反复调用 `plt.show()`；
- ❌ 不要混用 `pylab`（已弃用），始终用 `import matplotlib.pyplot as plt`；
- 📌 中文显示问题？添加：
  ```python
  plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
  plt.rcParams['axes.unicode_minus'] = False
  ```

## 7. 进阶方向

- 动态交互图：`Plotly` / `Bokeh`
- 地理空间图：`geopandas` + `contextily`
- 3D 图：`mpl_toolkits.mplot3d`
- 动画：`matplotlib.animation`
- Web 集成：`Dash` / `Streamlit`

## 8. 参考资源

- [Matplotlib 官方文档](https://matplotlib.org/stable/contents.html)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)
- 《Python 数据分析实战》（Peter Harrington）
- Real Python: *Matplotlib Tutorial*
- Kaggle Learn: *Data Visualization*