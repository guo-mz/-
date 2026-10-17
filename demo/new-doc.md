# Django 讲解文档

## 1. Django 简介

Django 是一个基于 Python 的高级 Web 框架，遵循「开箱即用」和「不要重复自己（DRY）」的设计哲学。它内置了 ORM、模板引擎、表单、认证、管理后台、路由、缓存、国际化等常用组件，适合快速构建安全、可维护的 Web 应用。

> ✅ 推荐环境：Python ≥ 3.8，安装 Django：
> ```bash
> pip install django
> ```

## 2. 项目与应用结构

### 2.1 创建项目

```bash
django-admin startproject mysite
cd mysite
python manage.py startapp blog
```

典型目录结构：

```text
mysite/
├── manage.py
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── blog/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    └── migrations/
```

### 2.2 注册应用

在 `mysite/settings.py` 的 `INSTALLED_APPS` 中加入：

```python
INSTALLED_APPS = [
    # ...
    'blog',
]
```

## 3. 模型（Model）与 ORM

Django 的 ORM 让开发者用 Python 类描述数据库表，无需手写 SQL。

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
```

生成并执行迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

常用查询示例：

```python
# 创建
Article.objects.create(title='Hello', content='Django ORM', category_id=1)

# 查询
Article.objects.filter(is_published=True).order_by('-published_at')[:10]
Article.objects.get(pk=1)

# 更新
Article.objects.filter(pk=1).update(title='New Title')

# 删除
Article.objects.filter(pk=1).delete()
```

## 4. 视图（View）与 URL 路由

### 4.1 函数视图

```python
from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/article_detail.html', {'article': article})
```

### 4.2 URL 配置

`blog/urls.py`：

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
]
```

`mysite/urls.py`：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

## 5. 模板（Template）

在 `blog/templates/blog/article_list.html` 中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>文章列表</title>
</head>
<body>
  <h1>文章列表</h1>
  <ul>
    {% for article in articles %}
      <li>
        <a href="{% url 'blog:article_detail' article.pk %}">{{ article.title }}</a>
        <small>{{ article.published_at|date:"Y-m-d" }}</small>
      </li>
    {% empty %}
      <li>暂无文章</li>
    {% endfor %}
  </ul>
</body>
</html>
```

模板常用语法：

- 变量：`{{ variable }}`
- 标签：`{% if %}`, `{% for %}`, `{% url %}`, `{% csrf_token %}`
- 过滤器：`{{ value|date:"Y-m-d" }}`, `{{ text|truncatechars:50 }}`
- 模板继承：`{% extends "base.html" %}` 与 `{% block content %}{% endblock %}`

## 6. 表单（Form）

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
```

视图中处理表单：

```python
from django.shortcuts import redirect
from .forms import ArticleForm

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})
```

模板中渲染表单并携带 CSRF 令牌：

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">保存</button>
</form>
```

## 7. 管理后台（Admin）

```python
from django.contrib import admin
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'published_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')

admin.site.register(Category)
```

创建超级用户并启动：

```bash
python manage.py createsuperuser
python manage.py runserver
```

访问 `http://127.0.0.1:8000/admin/` 即可管理数据。

## 8. 中间件与请求生命周期

Django 请求处理大致流程：

1. WSGI/ASGI 服务器接收请求；
2. 中间件链依次处理请求（`process_request` / `__call__`）；
3. URL 解析匹配视图；
4. 视图执行（可能访问 ORM、模板、缓存）；
5. 中间件链处理响应（`process_response`）；
6. 返回 HTTP 响应。

自定义中间件示例：

```python
class SimpleLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f'[REQ] {request.method} {request.path}')
        response = self.get_response(request)
        print(f'[RES] {response.status_code}')
        return response
```

在 `settings.py` 的 `MIDDLEWARE` 中注册即可。

## 9. 安全与最佳实践

- ✅ 生产环境设置 `DEBUG = False`，并配置 `ALLOWED_HOSTS`；
- ✅ 使用 `django.contrib.auth` 做认证与权限控制；
- ✅ 表单与 POST 请求必须包含 `{% csrf_token %}`；
- ✅ 使用 ORM 参数化查询，避免 SQL 注入；
- ✅ 模板默认自动转义，避免 XSS；
- ✅ 敏感配置（`SECRET_KEY`、数据库密码）通过环境变量注入；
- ✅ 使用 `python manage.py check --deploy` 做部署检查；
- ❌ 不要把 `SECRET_KEY` 提交到版本库；
- ❌ 不要在视图中直接拼接 SQL 字符串。

## 10. 常用命令速查

```bash
python manage.py runserver          # 启动开发服务器
python manage.py makemigrations     # 生成迁移文件
python manage.py migrate            # 执行迁移
python manage.py createsuperuser    # 创建管理员
python manage.py shell              # 进入交互式 shell
python manage.py collectstatic      # 收集静态文件
python manage.py test               # 运行测试
```

## 11. 进阶方向

- REST API：`djangorestframework`
- 异步视图：Django 3.1+ 的 `async def` 视图与 ASGI
- 任务队列：`Celery` + `Redis`
- 缓存：`django.core.cache`（Redis / Memcached）
- 部署：`Gunicorn` / `uWSGI` + `Nginx`，或容器化部署
- 测试：`pytest-django`、`factory_boy`

## 12. 参考资源

- [Django 官方文档](https://docs.djangoproject.com/zh-hans/stable/)
- [Django Tutorial](https://docs.djangoproject.com/zh-hans/stable/intro/tutorial01/)
- [Django REST framework](https://www.django-rest-framework.org/)
- 《Django 企业开发实战》（胡阳）
- Django Girls Tutorial
