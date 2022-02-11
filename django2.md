# django 补充

## 路由系统

### name，app_name，namespace

#### name

在 django 中，我们在 `urls.py` 中可能要写很多的 url 路径，然后我们可以在前端模板或后端使用：

urls.py

```python
urlpatterns = [
    path('login/', views.Login.as_view()),
]
```

视图函数：

```python
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        return redirect('/login/')
```

login.html

```html
<form method="post" action="/login/">
    ...
</form>
```

上面我们直接在视图函数中，硬编码了这个url（也就是写死了），以后如果这个 url 有变动，我们不仅要修改 `urls.py` 中，还要修改视图中的这个硬编码。

为了解决上面这个问题，我们可以给这个url设置一个 `name`，以后我们可以在视图中或前端模板中写它的名字，就可以使用名字来指定url。

urls.py

```python
urlpatterns = [
    path('login/', views.Login.as_view(), name="test"),  # name 指定 url 的别名
]
```

视图函数：

```python
from django.urls import reverse

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        return redirect(reverse('test'))  # 通过 reverse()，逆向找到这个名字代表的真实 url

```

login.html

```html
<form method="post" action="{% url 'test' %}">
</form>
```

> `{% url 'name' 参数1 参数2 ... %}` 的格式，可以在模板中使用某个url的名字。并且后面可以加参数，以空格隔开

#### app_name

还有一个问题：我们可以编写多个 app，每个app都可以是独立的：`django-admin startapp app01` 

因此一个项目可以有很多app，这些app中，每个app又可以有自己的路由：`urls.py` 配置，这样的话，可能会有app之间出现 url 重复的问题（譬如两个app中都定义了 `path('login/', views.Login.as_view(), name='login'),` 这样的话，当用户登录：`xxx.xxx/login` 时，我们无法分辨到底应该转到哪个app的 `login` 中。

因此，我们可以在每个 app 的 `urls.py` 中写上一个变量：

```python
app_name = 'app01'
urlpatterns = [
    path('login/', views.Login.as_view(), name="test"),  # name 指定 url 的别名
]
```

这样的话，我们可以指定当前 urls.py 的 app 名称。然后使用时，以这样的格式使用：`app_name:name`

视图：`reverse('test')` -> `reverse('app01:test')`

模板：`action="{% url 'test' %}"` -> `action="{% url 'app01:test' %}"`

#### namespace

下面的例子来自：https://www.cnblogs.com/ZFBG/p/11521842.html

还有一个问题：如果我们有多个 url，指向了同一个 app，我们怎么知道用户是从哪个 url 进来的？

namespace可以指定用户进来时的命名空间。

譬如：

urls.py

```python
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book1/', include('book.urls'),  namespace='book1')),  #变更部分
    path('book2/', include('book.urls'),  namespace='book2')),  #变更部分
]
```

> book1/, book2/ 都指向了同一个 app：book。我们可以给这两个 url 分别指定一个 namespace。

book/urls.py

```python
from django.urls import path
from . import views

app_name = "book"

urlpatterns = [
    path('', views.book_list),
    path('login', views.book_login, name="login"),
]
```

视图函数：

```python
def book_list(request):
        # 获取当前请求的 namespace
    current_namespace = request.resolver_match.namespace
    if request.GET.get("username"):
        return HttpResponse("My book list !!!!")
    else:
        print(current_namespace)
        return redirect(reverse("%s:login"% current_namespace))  # 变更部分

def book_login(request):
    return HttpResponse("Please Login!!!!")
```





## load static

```html
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'common.css' %}"/>
```