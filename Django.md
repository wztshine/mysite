# Django

django版本4.0

前言：

针对一个web服务框架，需要的内容并不多：

1. 建立socket，等待用户连接 （ django 中 wsgi.py 干的活）
2. 对用户的请求进行处理（一个网站，有许多url，将这些url写到一个 urls.py 里面，方便管理）
3. urls.py 中不仅写了 url，还有每个 url 对应的函数，让这些函数来处理 url的请求
4. 第3步的函数写在了 view.py 中，每个函数对请求进行处理，然后返回响应（第5步）
5. 文件渲染：render()。服务器做出的响应，其实就是字符串，返回给用户；但是一旦用户需要一些动态信息（如查询一些东西，需要到数据库查询，并返回给页面），那就只能将 数据 和页面模板拼接起来（在模板中写特殊的语法规则，render进行匹配替换），然后再返回给用户，这个过程叫做渲染。



数据库迁移：

在django中，有两个命令：

```shell
# 1. 创建迁移文件，目的是在你对model（ORM数据库类）进行更改后，创建一个迁移文件，记录这些更新（并没有写入数据库，只是记录在django自己的一个文件里）
python manage.py makemigrations
# 2. 将上述记录的更新，应用到数据库中（写入数据库）
python manage.py migrate
```



## 环境搭建和项目结构

### 创建项目：

`django-admin startproject <projectName>` project名称可以随意。

```shell
pip install django
django-admin startproject mysite  # 需要事先将 django-admin 路径加入环境变量，位于python的 Scripts 里。
```

### 项目结构：

开启一个项目后，django 会自动帮你创建一个项目结构。项目的文件夹名就是你的项目名字。

```
mysite:          # 这只是个文件夹名，django 自动帮你创建的，无所谓，可以随便改
 mysite:         # 这是python的包名（里面包含一个 __init__.py)
     settings.py  # 配置文件
     urls.py      # 每个url对应一个函数，函数处理 url 的请求;函数放在相关的 view 文件里
     wsgi.py      # Web服务网关接口
     asgi.py      # 异步服务网关接口
 manage.py        # 项目管理文件，通过它可以对项目进行管理
```

### 启动项目：

可以通过以下命令启动服务，IP：port是可选项，默认是：127.0.0.1:8000

项目启动后，在浏览器输入 ip:port 后，就能看到默认的 jdango 页面了。

```shell
python manage.py runserver [ip:port]  # ip:port is optional
```

### 项目配置：

**静态文件**

`settings.py` 中找到 `STATIC_URL` ，在它的下面添加如下变量，用来放置静态文件。

`STATIC_URL` 用来配置访问静态文件时的 url 前缀，譬如：127.0.0.1:8000/static/common.css

`STATICFILES_DIRS` 用来配置真实的静态文件的存放路径。

这两个变量的区别是：只要你访问 `ip:port/STATIC_URL/xxx.css` ，它就会自动去 `STATICFILES_DIRS` 里面去找你的 xxx.css 文件。

```python
STATIC_URL = '/static/'   # url 代表我们访问网站时，从这个url可以访问我们本地的静态文件
# STATIC_ROOT = BASE_DIR / 'collect_static'  # 项目部署时才会用到（debug=false)，这个目录用来存放所有的静态文件(debug=True时，django会自动收集所有app下面的static文件夹下的静态文件，但是真正生产环境部署项目时，就不能自动收集了，所以需要把所有静态文件收集放在这个目录下)。收集命令 `python manage.py collectstatic`
STATICFILES_DIRS=(
    os.path.join(BASE_DIR, 'static'),  # 末尾加',' 配置额外的静态文件存放地址（上面说过，django通常会自动收集各个app下static文件夹下的静态文件，这里我们可以指定去找某些文件夹里面的静态文件）
)
```

**CSRF**

`settings.py` 中暂时将 `MIDDLEWARE` 变量的 `MIDDLEWARE Csrf` 注释掉（防止跨站请求伪造攻击的）,如果不注释，则以后的 HTML 模板中，每个 `<form>` 表单中，都要加上 `{% csrf_token %}` 

```python
    # 'django.middleware.csrf.CsrfViewMiddleware',
```

**模板路径**

settings.py 中配置模板路径

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],  # 用来存放模板文件的路径
```

上述配置完成后，项目结构：

注意创建了两个文件夹：`static, templates` 。这两个文件夹就是上面配置的存放静态文件和模板的地方。

```
mysite:      # 这个文件夹名无所谓
  mysite:    # 这个是项目的包名
      settings.py  # 配置文件
      urls.py      # 路由配置：每个url对应一个函数，在函数里处理此url相关的请求
      asgi.py      # 
      wsgi.py      # socket类型
  manage.py        # 项目管理文件，通过它可以对项目进行管理
  static           # 放置静态文件，如css，js，以后使用时，用"/static/***.js"路径
  templates        # 放置网页模板 html 文件
```

## 创建视图层

### 响应字符串

**添加 url 路由**

在 `urls.py` 文件中，修改如下：

```python
from django.contrib import admin
from django.urls import path
from .views import hello  # 从 views 文件中，引入一个函数(暂未创建，请看下面)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello)  # 用户请求 hello/ 这个 url 时，我们用 hello 这个函数来处理请求。
]
```

**编写 url 请求的处理函数**

在内层的 `mysite` 这个文件夹下面，创建一个 `views.py` 

里面添加如下内容：

```python
from django.http import HttpResponse  # 导入 HttpResponse

def hello(request):  # 必须带一个参数，这个参数封装了用户所有的请求信息
    return HttpResponse('Hello world')  # 返回一个 HttpResponse 对象
```

启动项目：`python manage.py runserver`

至此，浏览器访问：`127.0.0.1:8000/hello`, 就能看到网页显示一个字符串：hello world

### 渲染 HTML 模板

**编写静态文件**

在 `static` 文件夹中，添加一个 `common.css` 文件，内容如下：

```css
h1{
    color: crimson;
    font-size: 20px;
}
```

**编写网页模板**

在 `templates` 文件夹下创建一个 `login.html` ，内容如下方代码。

注意下方的 `<link>` 标签的 `href='/static/common.css'` , 这个 `static` 其实是我们 `settings.py` 里面的 `STATIC_URL`变量的值 ，并不是 `STATICFILES_DIRS` 中定义的值。`STATIC_URL` 会自动去 `STATICFILES_DIRS` 定义的文件夹中，去找到真实的 xxx 文件。

假如你让 `STATIC_URL="sss"` ，尽管你的 `common.css` 文件可能真的存放在 **`static` 文件夹**，但下方的 href，你依然要改成：`href="/sss/common.css"`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- 注意这里：href='/static/common.css' -->
    <link rel="stylesheet" href="/static/common.css"></link>
</head>
<body>
    <h1>用户登陆</h1>
    <form>
        用户名：<input type="text" name="user" />
        <br/>
        密码：<input type="password" name="pwd" />
        <br/>
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

**编写 url**

修改 `urls.py` 文件如下：新增一个 url 路由地址

```python
from django.contrib import admin
from django.urls import path
from .views import hello, login  # here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('login/', login),  # here
]
```

**编写视图**

在 `views.py` 中添加如下函数：

```python
from django.shortcuts import render  # 导入 render

def login(request):
    return render(request, 'login.html')
```

> render 接受三个参数：用户的请求，模板相对地址(templates这个文件夹已经添加进settings.py了，所以它能识别出来)，要传递给模板的数据(此例没有涉及)
>
> render 会自动将模板渲染好，响应给用户。
>
> 此时启动项目，然后访问：ip:port/login 

### 提交数据，后台获取数据

**修改网页模板**

我们给模板的 `<form>` 表单添加了提交数据的 url 地址：`/login/` 和提交的方式：`post` 

`login.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/common.css"></link>
</head>
<body>
    <h1>用户登陆</h1>
    <form action="/login/" method="post">  <!-- 给 form 表单添加动作，点击提交按钮，会以 post 的方式提交到 /login/这个地址 -->
        {% csrf_token %}                   <!-- 之前说过，如果 settings.py 中不注释掉 CSRF 这种中间件，就要在 form 表单中加上这个 -->
        <!-- name属性的值，是关键字，我们后台可以通过这个关键字获取提交的数据 -->
        用户名：<input type="text" name="user" />
        <br/>
        密码：<input type="password" name="pwd" />
        <br/>
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

**修改 login 函数**

我们导入了一个 `HttpResponseRedirect` ，它可以让我们进行 url 的重定向。

视图函数 `login` 中， `request` 对象封装了所有的用户请求信息，通过 `request.method` 我们可以获取用户的请求类型。`get ` 方法就直接返回 html 模板；`post` 方式我们就可以通过 `request.POST` 获取用户提交的数据，数据是字典类型的，字典的键就是 html 模板中标签的 `name` 属性的值，键对应的值是用户输入的内容。

`views.py`

```python
from django.http import HttpResponse, HttpResponseRedirect  # here
from django.shortcuts import render


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = request.POST.get('user')  # user 是html模板中标签 name 属性的值。
        pwd = request.POST.get("pwd")
        if user == 'root' and pwd == 'root':  # 假设用户名和密码都是 root，重定向到百度。
            return HttpResponseRedirect('https://www.baidu.com')
            # return HttpResponseRedirect('/login/')   # 也可以跳转到自身链接
        else:
            return HttpResponse("Error!")  # 否则返回一个 Error
```

> 此时启动项目，打开 ip:port/login，用户名和密码全部输入: root，点击提交，就会跳转到百度。输入错误，就只会显示一个字符串：Error！

注意：其实不仅仅 `post `方法可以传递数据。`get `方法一样可以，只不过` get` 方法的数据，会以明文的方式放到 url 中传递，譬如：

views.py

```python
def login(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        age = request.GET.get('age')
        print(name, age)
        if name and age:
            return HttpResponse(f"{name}: {age}")
        else:
            return render(request, 'login.html')
```

login.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <!-- 以 get 方式传递2个参数: name,age；参数和 url 以？隔开，多个参数之间用 &-->
    <a href="/app01/login?name='wang'&age=18">点我</a>
</body>
</html>
```



### CBV 基于类的视图

上面我们写的视图，都是视图函数（FBV，基于函数），django也支持以类的形式，写的视图。

`urls.py`:

```python
from django.contrib import admin
from django.urls import path
from .views import Hello  # 导入类视图

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', Hello.as_view())  # 一定要加上 as_view()
]
```

`views.py`:

```python
from django.views import View
from django.http import HttpResponse


class Hello(View):  # 继承自 View
    def get(self, request):  # 以 get 方式发来的请求，自动调用 get 方法
        return HttpResponse('You visit from get.')

    def post(self, request):  # 以 post 方式发来的请求， 自动调用 post 方法
        return HttpResponse("You visit from post")
```

> 原理其实很简单，就是类里面有个 dispatch 方法，来进行请求的分发，发现是什么请求，就传递给哪个函数去处理。





### 模板语言

上面我们实现了用户的简单登陆跳转，但是当用户登陆失败时，我们直接返回的是一个字符串，这样很难看。

解决办法就是我们返回一个错误信息，让这个信息嵌套在 html 模板中，这样就稍微好看一些了。

**修改 login 视图**

`views.py`: login 函数修改如下

> render 函数接受三个参数(用户请求，模板，模板上下文信息)
>
> 模板上下文信息是一个 `context` 对象，类似于字典。我们可以直接传递给它一个字典类型的值。它的键名可以在模板中以 `{{ key }}` 的形式被调用，会将键对应的值显示在模板中。

```python
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get("pwd")
        if user == 'root' and pwd == 'root':
            return HttpResponseRedirect('https://www.baidu.com')
            # return HttpResponseRedirect('/login/')
        else:
            # return HttpResponse("Error!")
            return render(request, 'login.html', {'error': "用户名或密码错误"})
        	# 注意这里的 error 这个键，模板中会通过它获取值。
```

**修改网页模板**

`login.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/common.css"></link>
</head>
<body>
    <h1>用户登陆</h1>
    <form action="/login/" method="post">
        {% csrf_token %}
        用户名：<input type="text" name="user" />
        <br/>
        密码：<input type="password" name="pwd" />
        <br/>
        <div style="color: red;">{{ error }}</div>  <!-- error 是传递过来的字典的键名 -->
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

> 此时启动项目，打开 ip:port/login，用户名和密码全部输入: root，点击提交，就会跳转到百度。输入错误，就会在下方显示一个：用户名或密码错误。这是因为我们后台发送的数据，渲染后，嵌套在网页中了。





## 路由

我们之前也在 urls.py 中写了一些匹配规则，可以让用户发来的请求映射到某个函数来处理，但是之前的 url 规则都是写死的。其实 url 规则中，还可以写正则表达式。

### 正则表达式匹配

#### 普通正则表达式

我们知道正则表达式可以命名一个组，如：`(?P<value>\d+)`，value就是它的组名。不带组名的正则表达式，**它匹配成功的部分，会作为 “位置参数”，传递给视图函数**。

`urls.py`:

```python
from django.contrib import admin
from django.urls import path, re_path
from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('hello/(\d+)?', hello),  # (\d+)? 这就是一个正则表达式，它可以匹配数字，匹配成功的部分会作为位置参数，传递给视图函数。
]
```

`views.py`:

```python
from django.http import HttpResponse, HttpResponseRedirect


def hello(request, num):  # num 用来接受 正则表达式 匹配成功的字符。
    return HttpResponse('hello %s' %num)
```

#### 带组名的正则

带有组名的正则，会将正则表达式匹配成功的部分，作为**关键字参数**传递给视图函数，因此**视图函数中的参数名和正则表达式中的组名要一致**。

`urls.py`:

```python
from django.contrib import admin
from django.urls import path, re_path
from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('hello/(?P<page>\d+)?', hello),  # ?P<page>(\d+)? 匹配成功的部分，会作为关键字参数：page=xx 传递给视图函数
]
```

`views.py`:

```python
from django.http import HttpResponse, HttpResponseRedirect


def hello(request, page):  # page 这个参数要和正则表达式的组名一致
    return HttpResponse('hello %s' %page)
```

> 注意：上面的正则表达式可以匹配上：`hello/2`; 这种，也可以匹配: `hello/2/sljd/djido` ，这是因为我们没有给它设置结尾，只要前面能匹配上，后面有再多东西也无所谓。如果想要严格的只匹配写的内容，可以加上`$` ，如：`re_path('hello/(?P<page>\d+)?$', hello)`

### 路由分发 include

如果一个网站路由太多了，我们可以将不同功能的 url 写在不同的文件里，然后在总文件里将其囊括收集进来，就行了。

譬如我们新建了一个 app01 的 app （见下一节的 App）。我们可以在 app01 这个文件夹下，创建一个 `app01/urls.py`:

```python
from django.contrib import admin
from django.urls import path, re_path
from .views import users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', users),
]
```

> 这就是一个常规的 url 配置

然后，我们在项目的 `mysite/urls.py` 中配置：

```python
from django.contrib import admin
from django.urls import path, re_path, include  # 导入 include
from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('app01.urls'))  # 包含了 app01 下的 urls.py 中的设置
]
```

这样配置以后，我们所有向 `app01/`  的请求，都会从 `app01/` 截断，将**剩余部分**转发到 `app01.urls.py` 中的配置。譬如：

`http://127.0.0.1:8000/app01/users/` 会将 `users/` 转发到 `app01.urls.py` 中的 `path('users/', users)`

### 反向查找 url

#### 普通路径

**给 url 命名**

譬如我们写了一个 path，可以给它添加一个 `name` 属性来指定它的名称：

urls.py

```python
from django.contrib import admin
from django.urls import path
from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello, name='hello_name')  # name
]
```

**通过 url 的名字，获取url真实路径**

views.py

```python
from django.http import HttpResponse
from django.urls import reverse  # 导入 reverse


def hello(request):
    real_path = reverse('hello_name')  # 这个 hello 就是我们 urls.py 中定义的 name 属性；这里会查找出真实的路径：/hello/
    return HttpResponse('path is: %s' %real_path)
```

#### 正则表达式

**无组名正则**

urls.py

```python
from django.contrib import admin
from django.urls import path, re_path, include
from .views import hello, hello2, hello3

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('hello/(\d+)/', hello2, name='hello2'),
]
```

views.py

```python
from django.http import HttpResponse
from django.urls import reverse  # 导入 reverse


def hello2(request, arg1):
    real_path = reverse('hello2', args=(arg1, ))  # 反向查找 url时，要加上传递的参数
    return HttpResponse('path is: %s' %real_path)
```

> 因为正则表达式会传递一个额外的位置参数给视图函数，所以反向查找时，也要把这个位置参数传递给 `reverse()` 的 `args` 参数。

**带组名正则**

```python
from django.contrib import admin
from django.urls import path, re_path, include
from .views import hello, hello2, hello3

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('hello/(?P<page>\d+)/', hello3, name='hello3')
]
```

views.py

```python
def hello3(request, page):
    real_path = reverse('hello3', kwargs={"page": page})  # 这个 hello 就是我们 urls.py 中定义的 name 属性
    return HttpResponse('path is: %s' %real_path)
```

> 和不带组名的类似，要给 `reverse()` 的 `kwargs` 参数传递参数。

#### 模板中使用 url 名字

使用关键字 `{% url 'name' path1 path2 %}` 。 name 代表了我们给url的命名，path1，path2代表了后续的路径，譬如：`{% url 'hello2' 1 3 %}` 会解析成： `/hello2/1/3` 这条路径。

Todo：app_name, namespace,



## 使用 App

### 创建和安装

如果一个项目非常大，可能包含多个不同的功能模块，我们就可以将这些互相没有什么关联的功能模块独立开来，每个模块当成一个 App，这样可以更让项目结构更加清晰。

**创建命令：**

```shell
python manage.py startapp app01  # app01 是自定义的名字
```

**目录结构**

```
migrations/  # 数据库迁移相关文件
admin.py	 # 后台管理配置
apps.py		 # app 相关配置
models.py    # 数据库模型ORM 
tests.py     # 测试文件
views.py     # 视图
```

**注册App**

打开 `settings.py`，找到 `INSTALLED_APPS` ，在里面添加我们自己创建的 `app01`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
]
```

### 使用模型 ORM

django 规定，如果想要用自带的 ORM ，必须创建一个App，然后才能使用。django 自带的 ORM 可以创建表，修改表等，但是不能创建数据库，**配置 mysql 数据库，请参考后面的 ‘配置mysql’ 小结**。

**创建表**

在 `app01/models.py` 中，我们可以编写很多类，每一个类都相当于一个数据库中的表，类的属性相当于表中的字段，每个类的实例对象，就相当于表中的一条数据。

`app01/models.py`:

```python
from django.db import models


class User(models.Model):  # 继承自 Model
    username = models.CharField(max_length=30)  # username 字段
    password = models.CharField(max_length=30)  # password 字段
 
# 更多字段类型，看附录部分。
```

> 注意：我们没有创建 `id` 字段，django ORM 会自动创建一个自增的 `id` 字段。

运行命令：

```shell
python .\manage.py makemigrations
python .\manage.py migrate
```

> makemigrations 这个命令，仅仅是将我们注册的app，都生成一个数据库记录文件(位于`app01/migrations/xxx.py`)，此时并没有真的在数据库中创建表。
>
> migrate 这个命令，是将我们上面生成的数据路记录文件，真的写入我们的数据库中。

**修改表**

想要修改表，譬如某个字段的名字，或者添加一个字段，直接修改 `models.py` 中的字段就行：

```python
class User(models.Model):
    user = models.CharField(max_length=30)  # username 字段改成 user
    password = models.CharField(max_length=30)
    age = models.IntegerField(default=18)  # 添加新字段
```

然后重新运行一下：

```shell
python .\manage.py makemigrations
python .\manage.py migrate
```

**外键**

为了创建外键，我们先创建一个新的表：用户分组

```python
class UserGroup(models.Model):
    title = models.CharField(max_length=20)
```

我们给 `User` 表创建一个 `UserGroup` 表的外键：

```python
class User(models.Model):
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    age = models.IntegerField(default=18)
	# 创建外键
    group = models.ForeignKey("UserGroup", on_delete=models.SET_NULL, null=True)
```

> 注意：我们创建的外键字段是 `group`, 但是 django 会自动给它加个后缀，变成：`group_id`， `group_id` 绑定的是 UserGroup 中的 `id` 字段。



#### 增删查改

API 大全: [官方网址](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/)

通过如下命令激活交互式命令行：

```shell
python .\manage.py shell
```

我们可以通过 `class.objects` 获取一个表的管理器。我们之前说过，一个类就代表了一个表，类的属性就代表了表中的字段，类的实例就代表了表中的一条数据。

通过这个管理器，我们可以查询/过滤/修改表中的数据，在 ORM 中，通常有这么几种对象：

`QuerySet` 查询数据的集合，类似于列表，里面的每个元素都是一行数据（类的对象）

`类的 object` 类的实例对象，代表一个数据。表中的每个字段都是这个对象的属性。

```python
>>> from app01.models import User, UserGroup
# 添加
>>> UserGroup.objects.create(title='t1')
<UserGroup: UserGroup object (1)>

# 过滤查询
>>> UserGroup.objects.filter(id=1)
<QuerySet [<UserGroup: UserGroup object (1)>]>

# __lt 是特殊的方法，django中特殊的方法都是以 __ 开头的，它可以查找id<1的数据
>>> UserGroup.objects.filter(id__lt=1)
<QuerySet []>

# id>1 的数据
>>> UserGroup.objects.filter(id__gt=1)
<QuerySet []>

# 更新 id=1 那条数据的 title
>>> UserGroup.objects.filter(id=1).update(title='t2')
1

# 查询某条记录的 title；通过索引获取 QuerySet 中的某个对象
>>> UserGroup.objects.filter(id=1)[0].title
't2'

# 删除
>>> UserGroup.objects.filter(id=1).delete()
(1, {'app01.UserGroup': 1})

# 查询全部数据
>>> UserGroup.objects.all()
<QuerySet []>

# 查询 user != 'ss' 的数据
>>> User.objects.exclude(user='ss')
<QuerySet [<User: asdf>, <User: wzt>]>



# ----------------------------- 重要 ------------------------

# 获取外键id,注意和下面 .group 的区别
>>> User.objects.filter(id=1)[0].group_id
2

# 注意！！！通过我们定义的 group 外键字段(没加'_id')，获取外键的数据对象
>>> User.objects.filter(id=1)[0].group
<UserGroup: UserGroup object (2)>  # 这是 UserGroup 表中的一个数据对象。

# 获取和id=1这条记录相关联的UserGroup中的数据的 title
>>> User.objects.filter(id=1)[0].group.title
't1'
```

> filter(condition1, condition2,...) 可以查询多个条件同时满足的数据，类似于 `con1 and con2`
>
> update(), delete() 不仅可以作用于单独的数据对象，也可以作用于 QuerySet，即可以批量删除或更新一组数据。
>
> **重要**：我们之前说过，创建外键时，django 会自动给外键字段加上 `_id` 后缀，我们可以通过`xx_id` 获取外键的 id，但是如果我们对外键**不加 `_id`** ,我们查询出来的是外键中的那个数据对象。



我们还可以给一个类添加一些方法，譬如：

```python
class UserGroup(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title  # 这样我们打印数据时，会打印出对象的 title
```

运行：`python manage.py shell` 进入交互式命令：

```python
>>> from app01.models import User, UserGroup

# 实例化一个类，实现数据的创建，但是需要手动调用 .save() 方法，否则不会保存到数据库。
>>> g = UserGroup(title='title_1')
>>> g.save()

# 查询一下这个数据对象
>>> g
<UserGroup: title_1>  # 打印的是 title 字段。我们定义的 __str__ 方法生效了。
    
# 重要！！！见下方注解
>>> g.user_set
<django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x0000018F9E39B940>

# 查询 User 表中有哪些人关联了当前 g 这个数据
>>> g.user_set.all()
<QuerySet []>

# 在 User 表中创建一条和当前 g 这条数据相关联的用户
>>> g.user_set.create(user='wzt',password='132',age=20)
<User: wzt>

# 查询
>>> User.objects.filter(user='wzt')
<QuerySet [<User: wzt>]>  # 通过 g 确实创建成功了。
    
# 查询和 g 相关联的 User。
>>> g.user_set.all()
<QuerySet [<User: wzt>]>


```

> 注解：上面的例子中， `g` 是一个 `UserGroup` 数据对象。`UserGroup` 表的 `id` 字段是 `User` 表的外键。因此，UserGroup 表便和 User 表有了关联。作为 `User` 表的外键，`UserGroup` 表有个隐藏的字段：`lower(fk)_set` ，也就是 `小写的外键表名_set`， 通过这个字段，`UserGroup` 的数据对象就可以得到关联表的一个管理器，通过这个管理器，就可以查询出和自身相关联的数据。

补充一下 ForeignKey 正向反向，有外键的表主动查询外键视为正向，没有外键的表查询以它为外键的表视为反向：

```
正向：
	当使用 filter(), all(), values(), values_list() 等查询外键表： fk__xxx(双下划线)
	e.g.  
		User.objects.filter(group__title="title_1")
		User.objects.all().values('id','user','group__title')
	
	当使用单独的对象，使用： fk.xxx
	e.g.
		obj = User.objects.all()[0]
		obj.group.title
		
反向：
	当使用 filter(), all(), values(), values_list() 等查询： 小写表名__xxx(双下划线)
	e.g.
		UserGroup.objects.filter(user__age__lt=30)
		
	当使用单独的对象，使用：小写表名_set (单下划线)
	e.g.
		obj = UserGroup.objects.filter(user__age__lt=30)[0]
		obj.user_set.all()

```



**QuerySet -->字典, 列表**

我们通过 `filter()` , `all()` 查询出来的数据，都是 `QuerySet` 对象，也就是数据对象的集合。我们也可以将其转换成字典或列表的集合。

**字典：**

```python
>>> User.objects.all().values('id','user')
<QuerySet [{'id': 1, 'user': 'ss'}, {'id': 2, 'user': 'asdf'}]>
```

> .values(字段名) 可以获取将其转换成字段的字典。

获取和 User 表关联的 UserGroup 的信息：

```python
>>> User.objects.all().values('id','user','group__title')
<QuerySet [{'id': 3, 'user': 'wzt', 'group__title': 'title_1'}]>
```

> 注意这里的 “group__title"。从 User 表中想要查询出 UserGroup 中的数据，我们之前是用这样的：`User.objects.filter(id=1)[0].group.title` ，但是在 `values()` 中，我们要把 `.` 写成 `__`

**列表**

```python
>>> User.objects.all().values_list('id','user')
<QuerySet [(1, 'ss'), (2, 'asdf'), (3, 'wzt')]>


>>> User.objects.all().values_list('id','user','group__title')
<QuerySet [(1, 'ss', 't1'), (2, 'asdf', 't1'), (3, 'wzt', 'title_1')]>

```

#### 排序

```python
>>> User.objects.order_by('id')
<QuerySet [<User: 1-ss>, <User: 2-asdf>, <User: 3-wzt>]>

# 加上 `-` 可以倒叙排序
>>> User.objects.order_by('-id')
<QuerySet [<User: 3-wzt>, <User: 2-asdf>, <User: 1-ss>]>

```

> ”-“ 可以实现倒叙排序，多个字段排序，可以使用逗号隔开：`order_by("id", "user")`

#### 分组

参考自：[这里](https://hakibenita.com/django-group-by-sql)

```python
from django.db.models import Count

>>> User.objects.values('group_id').annotate(total=Count('id'))
<QuerySet [{'group_id': 2, 'total': 2}, {'group_id': 3, 'total': 1}]>



"""
等同于上面的：

SELECT
    group_id,
    COUNT(id) AS total
FROM
    User
GROUP BY
    group_id
"""
```

> values('xxx','xxxx') 按照什么分组
>
> annotate 按照什么聚合

**带上 having**

```python
>>> User.objects.values('group_id').annotate(total=Count('id')).filter(total__gt=1)
<QuerySet [{'group_id': 2, 'total': 2}]>


"""
等同于上面：

SELECT
    group_id,
    COUNT(id) AS total
FROM
    User
GROUP BY
    group_id
HAVING
	Count(id) > 1
"""
```



#### F(), Q(), extra()

**F**

F() 表达式可以让你从数据库获取数据的情况下，对一个数值进行更改。譬如：

```python
reporter = Reporters.objects.get(name='Tintin')  # 获取一个数据
reporter.stories_filed += 1  # 对这个数据的 stories_filed +1
reporter.save()  # 保存回数据库
```

> 这个操作首先是将数据从数据库中取出来，然后放到 python 中+1，再放回数据库。

使用F：

```python
from django.db.models import F

reporter = Reporters.objects.get(name='Tintin')
reporter.stories_filed = F('stories_filed') + 1
reporter.save()
# 想要重新访问这个更新后的值，必须重新加载
reporter.refresh_from_db()
```

> 好处是，django 会自动将 F 表达式转换成 SQL 语句，让字段自加1的操作在**数据库级别**执行。所以python根本就不知道 stories_filed 这个字段的值。

update 时也能用 F：

```python
Reporter.objects.all().update(stories_filed=F('stories_filed') + 1)
```

**Q**

更高级的条件组合，如多个条件之间的 `or`, `and`, 取反

`or`:

```python
from django.db.models import Q
qs = User.objects.filter(Q(user__startswith='R')|Q(user__startswith='D'))
```

`and`:

多个条件是 `and`, 也可以手动合并：`Q() & Q()`

```python
from django.db.models import Q
qs = User.objects.filter(Q(user__startswith='R'), Q(user__startswith='D'))
```

多个条件：

```python
User.objects.filter(Q(user__startswith='R'), Q(user__startswith='D')|Q(id__lt=3))
```

> 相当于：`select * from User where user like "R%" and (user like "D%" or id < 3)`

取反：

```python
>>> User.objects.filter(~Q(user__startswith="w"))  # ~ 取反。也就是不以 w 开头的数据
<QuerySet [<User: 1-ss>, <User: 2-asdf>]>
```

如果有关键字参数，要将 Q() 放到前面：

```python
>>> User.objects.filter(~Q(user__startswith="w"), id__lt=3)
```

**extra()**

4.0 文档上说这个 API 未来可能会废弃。

```
extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
```

- select： 可以做子查询。它需要一个字典作为参数，键为子查询的别名，值为子查询的内容。
- select_params： 接受列表作为参数，和 select 参数搭配，列表中的值是 select 参数中子查询的关键字
- where：sql语句中的 wehre 筛选条件
- params：和 where 参数搭配，放置 筛选条件中的关键字
- tables：和某个表连接（默认笛卡尔积）
- order_by: 排序方式

示例一：select, select_params

```python
User.objects.extra(select={"adult":"age > %s"},select_params=[18,])

"""
select 
	*, (age > 18) as adult 
from 
	app01_user;
	
写原生 SQL 的时候注意，django 建表的时候，会自动以”App名_小写表名" 的格式创建表名。
"""
```

> 之所以使用 %s ,然后将 %s 的值放到 select_params 里面，是为了防止 SQL 注入。

示例二：where，params

```python
User.objects.extra(select={"adult":"age > %s"},select_params=[18,], 
                   where=["id=%s OR id=%s", "user=%s"], params=[3, 2,'wzt'])


"""
select 
	*, (age > 18) as adult 
from 
	app01_user
where
	(id=3 or id=2) and user='wzt'; 
"""
    
```

示例三：order_by

```python
User.objects.extra(select={"adult":"age > %s"},select_params=[18,], 
                   where=["id=%s OR id=%s", "user=%s"], params=[3, 2,'wzt'], 
                   order_by=['id', '-user'])


"""
select 
	*, (age > 18) as adult 
from 
	app01_user
where
	(id=3 or id=2) and user='wzt'
order by
	id asc, user desc;
"""
```

tables:

```python
>>> qs = User.objects.extra(select={"adult":"age > %s"},select_params=[18,], where=["app01_user.id=%s OR app01_usergroup.id=%s", "user=%s"], params=[3, 2,'wzt'], o
rder_by=['app01_user.id', '-user'], tables=['app01_usergroup'])

>>> print(qs.query)
SELECT 
	(age > 18) AS `adult`, `app01_user`.`id`, 		`app01_user`.`user`,`app01_user`.`password`, `app01_user`.`age`, `app01_user`.`group_id` 
FROM 
	`app01_user` , `app01_usergroup` 
WHERE 
	(app01_user.id=3 OR app01_usergroup.id=2) AND (user=wzt) 
ORDER BY 
	(`app01_user`.id) ASC, `app01_user`.`user` DESC
```



#### 原生SQL语句

```python
from django.db import connection, connections
cursor = connections['default'].cursor()  # 指定连接 settings.py 中定义的 DATABASES 的 default 数据库
# cursor = connection.cursor()  # 连接默认的数据库，等同于上一行
cursor.execute('select * from mydatabase')
row = cursor.fetchone()
```

#### 性能提升

在上面我们曾经提到过，如果一个表拥有外键，我们可以直接通过外键名(不加`_id`) 获取相关联的数据(见上面 **增删查改** 这一小节使用的模型):

```python
>>> User.objects.filter(id=1)[0].group
<UserGroup: UserGroup object (2)>
```

其实这样做数据库查询了2次。第一次先查询 id=1 的 User 对象。然后通过 `group` 这个外键字段，又查询一次数据库，获取了与这个对象相关联的用户群组的信息。这样其实耗费了性能，django 提高了两个方法，可以提升性能：

**select_related**

这个方法，可以让先让数据库的多个表进行连表，然后将连表后的数据查询出来，实现一次性查询出想要的数据。

举例：

```python
>>> q = User.objects.select_related('group').all()  # group是外键名

>>> print(q.query)  # 上一条命令，django 会自动生成的查询语句
SELECT `app01_user`.`id`, `app01_user`.`user`, `app01_user`.`password`, `app01_user`.`age`, `app01_user`.`group_id`, `app01_usergroup`.`id`, `app01_usergroup`.`title` 
FROM `app01_user` LEFT OUTER JOIN `app01_usergroup` 
ON (`app01_user`.`group_id` = `app01_usergroup`.`id`)
```

> group 是外键名。all()和select_related() 函数的顺序无所谓，谁前谁后都行。

**prefetch_related**

和 select_related 类似，都可以提升性能，但略有不同。select_related 只能进行一对一和外键这种关系。而 prefetch_related 可以进行多对多和多对一。

select_related 是先连表，然后查询一次，而 prefetch_related 是针对两个有关系的表，在对第一个表查询时，根据表中和第二个表相关的字段，预查询一次第二个表，这样当你需要第二个表的数据时，从缓存中找就行了。

官方例子：

models.py

```python
from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=30)

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)  # 披萨和配料是多对多关系

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )  # 打印披萨对象时，会查询一次当前披萨的所有配料
```

传统的查询：

```python
>>> Pizza.objects.all()
["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)"...
```

> 打印披萨对象时，针对每个对象，都查询一次配料。

改成这样：

```python
>>> Pizza.objects.all().prefetch_related('toppings')
```

> 就像上面说的，在查询披萨表时，会预查询一下配料表，然后当打印每一个披萨对象时，就不会去数据库查询配料了，而是在预查询的缓存中查找配料。

#### 一对多关系

ForeignKey 可以创建一对多关系，我们上面也提到了，ForeignKey 其实也可以自关联：

models.py

```python
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    gender_choice = (
        (1, "man"),
        (0, "woman")
    )
    gender = models.IntegerField(choices=gender_choice, default=1)
    # 和自身创建外键关系，我们假设每个用户关联的都是自己的老公或老婆
    f = models.ForeignKey("User", null=True, on_delete=models.CASCADE)
```

查询：python manage.py shell:

```python
>>> g = User.objects.filter(id=1).first()  # 查询到某个女生
>>> g.f		# 查询一下这个女生的外键：她老公
<User: User object (3)>

>>> h = User.objects.filter(id=3).first()  # 查询某个男生
>>> h.f		# 查询一下他有没有老婆
<User: User object (1)>
>>> h.user_set.all()   # 也可以通过 表名_set 查询
<QuerySet [<User: User object (1)>]>
```

通过这种外键的自关联，我们可以实现评论系统：一条评论可以是另一个评论的回复。比如将一个评论的外键写入另一个评论的id，这样就有了评论之间的从属关系。



#### 多对多关系

**ManyToManyField**

上面我们提到过 `ForeignKey` , 它可以将两个表建立一对多的关系。django 中还可以建立多对多关系：`ManyToManyField`

app01/models.py

```python
class Girls(models.Model):
    name = models.CharField(max_length=20)

class Boys(models.Model):
    name = models.CharField(max_length=20)
    girl = models.ManyToManyField(Girls)  # 建立外键关系，但是并不会在 app01_boys 表中创建这个字段！！！
```

> 上面的 Boys 模型中，`girl `关键字创建了一个多对多关系。但是并没有在 `app01_boys `中创建这个字段，django 会自动创建一个**额外的关系表**：`app01_boys_girl ` (`应用名_表名_外间名`)。
>
> 这个自动创建的 `app01_boys_girl` 表，里面有三个字段：`id, boys_id, girls_id` ,也就是自动将 boys 表和 girls 表的主键都放到这个表。

`python manage.py shell: `

```python
>>> from app01.models import Boys, Girls

# 创建几条数据
>>> Girls.objects.create(name='g1')
>>> Girls.objects.create(name='g2')
>>> Girls.objects.create(name='g3')
>>> Boys.objects.create(name='b1')
>>> Boys.objects.create(name='b2')
>>> Boys.objects.create(name='b3')



>>> boy = Boys.objects.all().first()

>>> boy.girl.all()  # 通过 boy 对象调用它的外键 girl，可以查询出和这个 boy 对象相关联的所有女孩数据对象
<QuerySet []>

# 添加
>>> boy.girl.add(1,2)  # 对当前这个 boy 对象，在django自动创建的 app01_boys_girl 表中，添加两条和女孩id=1, id=2 相关联的数据

# 查询
>>> boy.girl.all()  # 对当前boy，逆向找出所有和他相关的女孩们
<QuerySet [<Girls: Girls object (1)>, <Girls: Girls object (2)>]>

# 删除
>>> boy.girl.remove(1,2)  # 在关系表中，删除当前boy相关联的 id=1,id=2 的女孩数据。
>>> boy.girl.all()
<QuerySet []>  # 已经删掉了

# 重置boy数据（原有的数据会清空重置）
>>> boy.girl.set([2,])  # 参数必须是可迭代对象
>>> boy.girl.all()
<QuerySet [<Girls: Girls object (2)>]>

# 清空当前boy的数据
>>> boy.girl.clear()
>>> boy.girl.all()
<QuerySet []>

```

> 上面都是从 boys 表中查询和他相关联的女孩数据。其实从女孩数据中也可以查询出男孩数据：
>
> ```python
> >>> girl = Girls.objects.all().first()
> >>> girl.boys_set.all()  # 通过相关联的 “小写表名_set” 查询关联的男孩数据
> <QuerySet [<Boys: Boys object (1)>]>
> 
> # 其他的 add(), set(), remove()... 也是通用的。
> # girl.boys_set.add()
> # girl.boys_set.remove()
> # ......
> ```



注意：ManyToManyField() 可以用来**关联自身**：

modesls.py

```python
from django.db import models

# 一个用户表，存放了男女信息
class User(models.Model):
    username = models.CharField(max_length=30)
    gender_choice = (
        (1, "man"),
        (0, "woman")
    )
    gender = models.IntegerField(choices=gender_choice, default=1)
    many = models.ManyToManyField("User")  # 关联自身这个表
```

> 假设我们想要创建 `男，女` 两个性别的人群，并且想要将他们产生联系：譬如约会信息。我们通常可以创建三个表：`女生表`， `男生表`, `关系表`，也就是这一小节开头实现的方式。
>
> 但是其实女生和男生，都是用户，他们其实可以放到一张表中。这种情况下，我们可以让这个用户表和自身进行关联，也就是创建了一个多对多的关系（django 会默认帮我们创建一个表: app_user_many)
>
> app_user_many 这个表，有三个字段：`id, from_user_id, to_user_id`. 假设我们规定：`from_user_id `用来存放女生id，`to_user_id` 存放男生id，这样我们就能创建男女生关系了。
>
> 如何查询？
>
> from_user_id 查询关联的 to_user_id，使用：obj.foreignkey.xxx()
>
> to_user_id 查询关联的 from_user_id, 使用：obj.表名_set.xxx()
>
> ```python
> >>> from app01.models import User
> 
> 
> >>> girl = User.objects.filter(id=1)[0]  # 笔者数据库里 id=1 这条数据是个女生
> >>> girl.many.all()  # 女生查询关联的男生：obj.many.xxx()
> <QuerySet [<User: User object (2)>, <User: User object (3)>]>
> >>>
> >>>
> >>> boy = User.objects.filter(id=3)[0]  # 这条数据是男生
> >>> boy.many.all()  # 男生无法通过:obj.many.xx() 查询女生
> <QuerySet []>
> >>> boy.user_set.all()  # 只能通过： obj.表名_set.xxx() 查询所关联的女生
> <QuerySet [<User: User object (1)>]>
> ```







**自定义方式**

上面的 `ManyToManyField` 自动生成的表，只能包含三个字段：`id, table1_id, table2_id`，想要生成多个字段，只能自己定义表了。

app01/models.py

```python
class Girls(models.Model):
    name = models.CharField(max_length=20)

class Boys(models.Model):
    name = models.CharField(max_length=20)

class Relation(models.Model):
    girl = models.ForeignKey(Girls, on_delete=models.SET_NULL)
    boy = models.ForeignKey(Boys, on_delete=models.SET_NULL)
    # ... other field
    class Meta:
        unique_together = [  # girl，boy 字段进行联合唯一索引
            ('girl', 'boy')
        ]
```

`python manage.py shell:`

```python
>>> Relation.objects.create(girl_id=1,boy_id=2)  # 创建关系
<Relation: Relation object (1)>

# 选择和名字为 b2 的 boy 相关联的女孩
>>> g = Relation.objects.filter(boy__name='b2').select_related("girl")

```

**ManyToManyField + 自定义**

```python
class Girls(models.Model):
    name = models.CharField(max_length=20)


class Boys(models.Model):
    name = models.CharField(max_length=20)
    girl = models.ManyToManyField(Girls, through="Relation")


class Relation(models.Model):
    girl = models.ForeignKey(Girls, on_delete=models.CASCADE)
    boy = models.ForeignKey(Boys, on_delete=models.CASCADE)
    # ... other field
    class Meta:
        unique_together = [  # girl，boy 字段进行联合唯一索引
            ('girl', 'boy')
        ]
```

可以两者结合，`through` 参数指定了关系表，这样的话，可以使用`ManyToManyField` 部分的查询功能和清空功能(`all(),filter(), clear()` 等，但不能`add(), remove(), set()`



[Django ORM Cookbook](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query_relatedtool.html)



## Ajax实现登录模态对话框

ajax 的好处就是在不刷新页面的情况下，实现对服务器后台发送数据。

首先，urls.py 添加相关的记录和对应函数

```python
from django.contrib import admin
from django.urls import path
from mysite.app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index ),
    path('login/', views.login ),
]
```

编写 templates/login.html ，导入jquery:  `static/jquery-3.6.0.js`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
    <style>
        .hide{
            display: none;
        }
        .shadow{
            position: fixed;
            background-color: black;
            opacity: 0.4;
            top: 0;
            left:0;
            right:0;
            bottom:0;
            z-index: 9;
        }
        .modal{
            z-index:10;
            background-color: white;
            position:fixed;
            height: 300px;
            width: 400px;
            top:50%;
            left:50%;
            margin-left:-200px;
            margin-top:-150px;
        }
    </style>
</head>
<body>
    <div>
        <input type="button" value="登录" onclick="show()" />
    </div>
    <div id="shadow" class="shadow hide"></div>
    <div id="window" class="modal hide">    <!-- 注意这里没有用 from表单，因为 form 表单提交数据会自动刷新 -->
            <p>用户名：<input id="uname" type="text" name="username" /></p>
            <p>密码：<input id="upasswd" type="text" name="password" /></p>
            <input type="button" value="提交" onclick="AjaxSend()" /><span id="errmsg"></span>
            <input type="button" value="取消" onclick="hide()"/>
    </div>

    <script src="/static/jquery-3.6.0.js"></script>
     <script>
        function show(){
            // 删掉class的值，显示隐藏的标签
            document.getElementById("window").classList.remove("hide");
            document.getElementById("shadow").classList.remove("hide");
        }

        function hide(){
            // 用来隐藏标签
            document.getElementById("window").classList.add("hide");
            document.getElementById("shadow").classList.add("hide");
        }
		// 调用 ajax，实现不刷新的提交数据。这里用到了 jquery 的语法规则，譬如：$("#uname").val() 是查找id='uname' 的标签的值
        function AjaxSend(){
            $.ajax({
                url: '/login/',  // 和form表单的action一样，即递交给哪个url处理
                type: 'POST',    // 方法Post
                data: {'username':$("#uname").val(),'password':$("#upasswd").val()}, //给服务器传递数据
                success: function(data){
                    // function 等服务器返回数据时才执行
                    // data 就是服务器返回的数据，假设成功时返回 OK
                    if (data=='OK'){
                        // location.href 可以设置刷新或跳转，跳转到外部网站
                        location.href='https://www.baidu.com'
                    }
                    else{
                        $('#errmsg').text(data);  // 显示错误信息
                    }
                }
            })
        }
    </script>
</body>
</html>
```

编写 url 的处理函数：views.login

```python
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('username')  # 获取ajax传递过来的数据
        password = request.POST.get('password')
        if name == 'root' and password == 'root':
            return HttpResponse('OK')    # 返回信息给ajax，交给ajax处理（此处无法重定向，如果重定向html，也只是将html作为字符串给交ajax而已）
        else:
            return HttpResponse('用户名或密码错误！')
```

### Ajax 小结

ajax 常见的设置：

```js
$.ajax({
    url : '/xxx/',  // 请求的 url 地址
    type: "POST",  // 请求方式：post，get
    data: {"key": value},  // 传递给后台服务器的值
    traditional:true, // 当data中的值含有列表时，需要加traditional，后台才能获取到值。
    dataType:'JSON', // 将服务器返回的数据处理成json格式
    success: function(arg){  // 请求成功后的回调函数。arg 是服务器返回的数据
        // code
    }
})
```

1. 编写 urls.py，指定视图函数

2. 编写相关html页面

   1. 禁用form表单（会自动刷新）

   2. 给按钮绑定事件

   3. 编写事件触发时的函数或 ajax

      ```javascript
      function AjaxSend(){
          $.ajax({
              url: '/login/',  // 和form表单的action一样，即递交给那个url处理
              type: 'POST',    // 方法：POST，GET
              data: {'username':$("#uname").val(),'password':$("#upasswd").val()}, //给服务器传递数据
              success: function(arg){
                  // function 等服务器返回数据时才执行
                  // arg = 服务器返回的数据
                  if (arg=='OK'){
                      location.href='https://www.baidu.com'; // 对服务端的信息判断，跳转到外部网站
                      location.reload(); // 刷新当前页面
                  }
                  else{
                      ...
                  }
              }
          })
      }
      ```

3. 编写函数，处理数据，并返回数据给Ajax（只能返回字符串，无法重定向，只能将数据给ajax，在ajax中用` location`重定向。

```html
<script src="/static/jquery-3.6.0.js"></script>
<script>
    $(function () {     // 当整个页面（DOM）加载完成后调用的方法
        $('.edit_id').click(function (){   // $()取值,#代表id，.代表class,$(this)代表当前容器。click方法是点击此容器时触发的方法.
            $("#shadow,#edit_modal").removeClass("hide");  // 清除shadow,edit_modal两个id容器的的class属性 hide
            var v = $(this).parent().prevAll();  // 查找当前容器的父容器前面所有的容器（同一级别,倒序）
            var cid = $(v[1]).attr('class');   // var[1]使用索引取值，也就是当前容器前面的第二个容器，.attr是获取此容器的属性的值
            var stuname = $(v[2]).text();  // .text()获取容器的文本内容
            var stuid = $(v[3]).text();
            $('#edit_stuid').val(stuid); // .val()可以用来取值，也可以.val(content)来赋值。
            $('#edit_name').val(stuname);
            $('#edit_classid').val(cid);
        });  
        
        
        $('#edit_butt').click(function () {
            $.ajax({                                // ajax
                url:'/edit_modal_student/',   // 请求发送给谁
                type:"POST",                   // 发送方法: POST/GET
                data:{'stuid':$('#edit_stuid').val(),'stuname': $("#edit_name").val(),'classid':$('#edit_classid').val()}, // data是发送给服务器的数据，字典类型。字典的键自定义，值从html容器中取值。
                traditional:true, // 当data含有列表时，需要加traditional，后台才能获取到值。
                dataType:'JSON', // 将服务器返回的数据处理成json格式
                success:function (args) {   // success后面是服务器返回数据时执行的回调函数，args接收服务器返回的数据
                    if (args.status){
                        location.reload();     // location.reload()是刷新页面. location.href='www.baidu.com' 是重定向
                    }
                    else{
                        $('#error').text(args.msg)
                    }
                }
            })
        });
        
        bindAdd();
    });
</script>    
    
```

### 原生 ajax

**GET 方式**

上面说的是使用 `JQuery` 实现的 ajax。我们可以使用原生的 JavaScript 实现ajax。

app01/urls.py

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('calculate/', views.calculate),
    path('add/', views.add)
]
```

app01/views.py

```python
from django.shortcuts import render, HttpResponse


def calculate(request):
    if request.method == 'GET':
        return render(request, 'add.html')


def add(request):
    if request.method == 'GET':
        v1 = request.GET.get('first')
        v2 = request.GET.get('second')
        result = int(v1) + int(v2)
        return HttpResponse(str(result))
```

templates/add.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- 不要写在 form 表单中，否则会刷新页面 -->
    <input type="text" name="first" />+
    <input type="text" name="second" />=
    <input type="text" name="result" />
    <br/>
    <input type="submit" onclick='add()' value="submit" />

    <script>
        function add() {
            var v1 = document.getElementsByName('first')[0].value;
            var v2 = document.getElementsByName('second')[0].value;
            var link = '/app01/add/?first=' + v1 + '&second=' + v2;  // 拼接请求地址和参数
			// 生成一个对象
            var obj = new XMLHttpRequest();
            obj.open('GET', link)  // 打开链接
            obj.send();  // 因为是 GET 方式，所以 send() 是空的
            obj.onreadystatechange = function(){
                if(obj.readyState === 4){
                    document.getElementsByName('result')[0].value = obj.responseText;
                }
            }
        }

    </script>
</body>
</html>
```

> 解释一下上面用到的内容：
>
> 我们通过 `var obj = new XMLHttpRequest();` 来生成一个对象，它可以用来向后台发送数据。
>
> `obj.open('GET', link)` 可以用来连接后端，第一个参数是请求方式，第二个参数是请求的 url。
>
> `obj.send(); ` 发送信息
>
> `obj.onreadystatechange` 这个属性可以被赋值一个函数。这样当服务器后台处理完数据，将数据返回给前端时，会自动调用这个回调函数。
>
> `obj.readyState` 这个属性是服务器返回数据的状态：`4 ` 表示已经接收到全部响应数据；
>
> `obj.responseText` 这个属性用来获取后台返回的数据；

**POST 方式**

app01/urls.py

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('calculate/', views.calculate),
    path('add/', views.add)
]
```

app01/views.py

```python
from django.shortcuts import render, HttpResponse


def calculate(request):
    if request.method == 'GET':
        return render(request, 'add.html')


def add(request):
    if request.method == 'GET':
        v1 = request.GET.get('first')
        v2 = request.GET.get('second')
        result = int(v1) + int(v2)
        return HttpResponse(str(result))
    else:
        v1 = request.POST.get('first')
        v2 = request.POST.get('second')
        print(v1, v2)
        result = int(v1) + int(v2)
        return HttpResponse(result)
```

templates/add.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- 相比于上面的 GET 方式，这里加了一个 csrf_token，因为下面的 ajax 中会以 form 表单的形式 POST 数据，而django如果启用了 csrf中间件，在 form 表单中必须添加 csrf_token  -->
    {% csrf_token %}
    <input type="text" name="first" />+
    <input type="text" name="second" />=
    <input type="text" name="result" />
    <br/>
    <input type="submit" onclick='add()' value="submit" />

    <script>
        function add() {
            var v1 = document.getElementsByName('first')[0].value;
            var v2 = document.getElementsByName('second')[0].value;
            // 这里获取一下 csrf_token 的值
            var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value

            var obj = new XMLHttpRequest();
            obj.open('POST', '/app01/add/')
            // 设置头部信息，相当于 form 表单的 enctyped 的默认值
            obj.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
            // 发送的数据，因为是 form 表单，所以带上 csrf token
            obj.send('first=' + v1 + '&second=' + v2 + '&csrfmiddlewaretoken='+csrf);
            obj.onreadystatechange = function(){
                if(obj.readyState === 4){
                    document.getElementsByName('result')[0].value = obj.responseText;
                }
            }
        }

    </script>
</body>
</html>
```

> 所以相对于 get 方式。Post 方式需要稍微改动一下：
>
> `obj.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')` 设置 form 表单的形式。
>
> `obj.send("Your-Data")` 要将数据放置在 `send()` 函数中发送给后台，并且如果你启用了 `csrf` 这个中间件，需要需要带上 `csrf` 的信息。

### Iframe 模拟 ajax

`<iframe>` 标签可以将一个页面，内嵌到一个页面中。通过它的这种特性，我们也可以实现类似于 ajax 的无刷新提交数据。

app01/views.py

```python
from django.shortcuts import render, HttpResponse


def add(request):
    if request.method == "GET":
        return render(request, 'add.html')
    else:
        headers = {"X-Frame-Options": 'SAMEORIGIN'}  # 不加这个，Chrome 控制台可能会报错：in a frame because it set 'X-Frame-Options' to 'deny'.
        return HttpResponse("POST", headers=headers)

```

templates/add.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- form 表单的 target 属性，可以指定在哪里显示接收到的响应数据，这里指定在 iframe 中，实现页面的不刷新 -->
    <form method="post" action="/app01/add/" target="ifr">
        {% csrf_token %}
        <iframe name="ifr"></iframe>
        <input type="text" name="username"/>
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```

> 原理是：`<iframe>` 标签可以内嵌一个页面。因此当我们提交数据时，我们可以将响应的数据放到 iframe 中。这样我们外层的页面不会刷新，只会刷新 iframe 这个内嵌的页面。

---

上面这样做还有一点小问题：我们如何知道服务器后台何时返回了数据。

我们知道，当服务器返回响应时，会将数据放在 `iframe` 中，所以 `<iframe>` 这个内嵌页面会**刷新**。 因此我们可以给它绑定一个刷新时的事件：`onload`

只需要改动模板文件就行：

templates/add.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- form 表单的 target 属性，可以指定在哪里显示接收到的响应数据，这里指定在 iframe 中，实现页面的不刷新 -->
    <form id="form1" method="post" action="/app01/add/" target="ifr">
        {% csrf_token %}
        <iframe name="ifr"></iframe>
        <input type="text" name="username"/>
        <a onclick="clicked()">提交</a>
    </form>

    <script>
        function clicked(){
            document.getElementById('form1').submit();  // 使用Javascript提交表单
            document.getElementsByTagName('iframe')[0].onload = function (){
                alert('Recv data.')
            }
        }
    </script>
</body>
</html>
```

> 首先，我们想要监听 `iframe` 的来自服务器响应后的刷新事件，需要给它绑定一个 `onload` 事件。但是如果我们直接给他绑定事件, 如：`<iframe name="ifr" onload="func()"></iframe>`, 当我们第一个通过 `get` 方式获取当前页面时，也会刷新页面，从而触发 onload 事件，这样不太好，因为我们想要在 **`POST`方式** 提交数据后，再监听后台响应。
>
> 所以，我们需要在**提交**数据后，再监听这个事件。因此我们想当然的给 **提交** 按钮添加一个点击事件：点击提交按钮后再监听，就是它添加一个 `onclick` 事件，在这个事件里面，给 iframe 添加 onload 事件。但是还是不对，因为 `onclick` 事件是在 **提交** 数据之前触发的：默认的 `<input type="submit" onclick="func()" value="提交">`，它会先执行 `onclick` 绑定的事件，然后再触发默认的 `submit` 事件向服务器后台发送数据，因此顺序还是不对。
>
> 所以，我们直接替换掉默认的 `<input type="submit">` 这种标签，使用了 `<a>` 标签，给他绑定上点击事件，在 onclick 事件对应的函数中，先使用脚本进行 form 表单的提交，然后再给 ifame 绑定刷新事件，就能正确的监听服务器后台传递过来数据时的刷新了。

---

如何获取 iframe 标签的内容？

上面我们可以给 iframe 设置返回的数据，也能够监听后台数据传递的时间。接下来就是获取 iframe 中后台传递过来的数据了。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form id="form1" method="post" action="/app01/add/" target="ifr">
        {% csrf_token %}
        <iframe name="ifr" style="display: none"></iframe>
        <input type="text" name="username"/>
        <a onclick="clicked()">提交</a>
    </form>

    <script>
        function clicked(){
            document.getElementById('form1').submit();
            document.getElementsByTagName('iframe')[0].onload = function (){
                // iframe 是一个完整的页面。我们服务器后台返回的数据，默认放在了 <body> 标签中。
                var content = document.getElementsByName('ifr')[0].contentWindow.document.body.innerText;
                alert(content)
            }
        }
    </script>
</body>
</html>
```

> 通过 `document.getElementsByName('ifr')[0].contentWindow.document.body.innerText;` 这句代码，可以获取 iframe 中我们后台传递过来的内容。

## Cookies, Session

### cookie

#### 普通cookie

设置cookies

```python
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        if name == 'root' and pwd =='root':
            obj = redirect('/classes')  # HttpResponse('xxxx'), render() 都可以 set_cookie
            obj.set_cookie('aaa','bbbbbbbbbbbbbbbbbbb')  # 设置cookie键值对
            return obj
        else:
            return render(request,'login.html')
```

验证cookie

```python
def classes(request):
    if request.COOKIES.get('aaa'):         # 获取cookies值
        return render(request,'classes.html')
    else:
        return redirect('/login/')
```

> `set_cookie()` 的参数：
>
> key, 
> value='',   # key, value 就是给cookie设置的键值对
> max_age=None,  # 多久失效（秒）
> expires=None,  # 失效日期（可以是 datetime 类型，或者是有效的字符串类型）
> path='/',      # cookie 针对的 url path
> domain=None,   # 针对特定的 domain（域名系统，一级域名二级域名等等）
> secure=False,  # https 相关的安全设置
> httponly=False,  # 通过js脚本将无法读取到cookie信息，能有效的防止XSS攻击
> samesite=None  # 是否允许跨站携带cookie

#### 加盐的cookie

对cookie的值加上一段随机字符串，安全性更高。

设置cookies: `set_signed_cookie(key,value,salt)`

```python
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        if name == 'root' and pwd =='root':
            obj = redirect('/classes')  # HttpResponse('xxxx'), render() 都可以 set_cookie
            obj.set_signed_cookie('aaa','bbbbbbbbbbbbbbbbbbb', salt="lsjofelase")  # 设置cookie键值
            return obj
        else:
            return render(request,'login.html')
```

验证cookie: `get_signed_cookie(key='', salt='')`

```python
def classes(request):
    if request.get_signed_cookie(key='aaa', salt='lsjofelase'):   # 获取cookies值
        return render(request,'classes.html')
    else:
        return redirect('/login/')
```



### session

cookie 是服务端发送给客户端的，保存在浏览器中的数据。但是这个数据有可能会被篡改，而且也不应该存放很重要的数据，否则被别人获取后，很不安全，因此 session 出现了。

session 是保存在服务器上的数据，而不是保存在客户端浏览器上，因此很安全。它的原理就是，生成一个随机字符串，将这个随机字符串作为 cookie 发送给客户端，因为它只是一个随机字符串（不携带重要数据），所以很安全。session 将这个随机字符串以及一些重要数据，作为键值对（随机字符串为键，重要数据为值）保存在服务器，这样当客户端携带着 cookie 发送来请求时，服务器可以验证某个 session 中是否有这个随机字符串。

示例：

```python
"""
session 原理：
1. 给用户先设置一个cookie，这个cookie包含一个无意义的随机字符串
2. 用户发来请求，获取这个无意义的随机字符串，然后去服务器的 session 里面查找这个随机字符串（这个字符串作为键，用户的信息作为值）
3. 根据这个随机字符串，获取用户的信息

也就是说，session其实就是对cookie的优化封装，而且将重要数据存放在了服务器上。
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse


def login(request):
    # 用户 GET 方式发送请求，返回 登陆页面
    if request.method == 'GET':
        return render(request, 'login.html')
    
    # 用户提交数据，则验证用户名和密码，成功后设置 session，并重定向到首页
    else:
        # POST 提交的数据
        user = request.POST.get('username')
        password = request.POST.get('password')
        if user == 'root' and password == 'root':
            """
            下面的 session 做了三件事：
            1. 生成了一个随机字符串
            2. 将随机字符串通过 cookie 发送给客户端
            3. 服务端保存了一个session:
                { 随机字符串：{"username": ..., "other": 'other info'} }
            """
            request.session['username'] = user  # session 中可以设置键值对信息
            request.session['other'] = 'other info'
            return redirect('/app01/index/')
        else:
            return render(request, 'login.html', {"error": "用户名或密码错误"})


def index(request):
    """
    下面的 request.session.get("username"), 也做了几件事：
    1. 获取客户端发来的 cookie 中的随机字符串
    2. 在 session 中尝试查找这个随机字符串
    3. 查找随机字符串对应的值中，是否有 username 这个值
    """
    if v := request.session.get('username'):
        return render(request, 'index.html', {"user": v})
    else:
        return redirect('/app01/login/')

```

### session 配置

本节来源：https://www.cnblogs.com/wupeiqi/aiticles/5246483.html

#### 配置

session 在 `settings.py` 中可以配置如下：

**session 存放位置**

session 可以以不同的方式存放在服务器上，如默认的存放在数据库中，也可以自己配置，放置在缓存或文件中：

```python
# 1. 存放在数据中库(默认方式)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 2. 放在缓存中
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'      # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置

# 3. 放在文件中
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = None         # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir()

# 4. 缓存+数据库中
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'        # 在存储数据的时候，会将数据先存到缓存中，再存到数据库中。这样就可以保证万一缓存系统出现问题，session数据也不会丢失。在获取数据的时候，会先从缓存中获取，如果缓存中没有，那么就会从数据库中获取。

# 5. 将 session 加密后放到 cookie 中
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
```

**session 配置**

```python
SESSION_COOKIE_NAME ＝ "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_PATH ＝ "/"                               # Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）
```



#### session 常用的方法

```python
def index(request):
    # 获取、设置、删除Session中数据,字典的形式
    request.session['k1']
    request.session.get('k1',None)
    request.session['k1'] = 123
    request.session.setdefault('k1',123) # 存在则不设置
    del request.session['k1']

    # 所有 键、值、键值对
    request.session.keys()
    request.session.values()
    request.session.items()
    request.session.iterkeys()
    request.session.itervalues()
    request.session.iteritems()


    # 用户session的随机字符串
    session_key = request.session.session_key

    # 将所有Session失效日期小于当前日期的数据删除
    request.session.clear_expired()

    # 检查 用户session的随机字符串 在数据库中是否
    request.session.exists(session_key)

    # 删除当前用户的所有Session数据
    request.session.delete(session_key)
    
    # 清除当前用户的 session
    request.session.clear()

    request.session.set_expiry(value)
    """
    * 如果value是个整数，session会在些秒数后失效。
    * 如果value是个datatime或timedelta，session就会在这个时间后失效。
    * 如果value是0,用户关闭浏览器session就会失效。
    * 如果value是None,session会依赖全局session失效策略。
    """

```







## 中间件

### csrf_token

我们之前提到过，csrf 是跨站请求伪造，它的原理就是在用户提交信息之前，会在 form 表单中给用户提供一个隐藏的随机字符串，然后用户携带着这个字符串进行提交。

确保 `settings.py` 中 `MIDDLEWARE` 变量中启用了： `'django.middleware.csrf.CsrfViewMiddleware',`

之后在提交 form 表单时，需要加上 `{% csrf_token %}`:

```html
    <form>
        {% csrf_token %}
        <input type="text" name="username" />
        <input type="submit" value="submit" />
    </form>
```

> 这样的话，django 会自动给 form 表单添加一个隐藏的 input 标签，value 属性是一个随机字符串。

在启用了 csrf 中间件之后，django 项目中所有的 `form` 表单中，都需要加上 `{% csrf_token %}` ，否则会报错。

**临时启用，禁用csrf**

但是如果想要针对某个 url 的请求进行**禁用**，需要加一个装饰器就行：

views.py

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt  # 针对下面的视图，禁用 csrf。所以模板 form 表单中不要加 {% csrf_token %}
def hello(request):
    return render(request, 'hello.html')
```

> 如果 form 表单中依然加了 {% csrf_token %}, 禁用失败。

如果在 `settings.py` 的中间件中注释掉了 `django.middleware.csrf.CsrfViewMiddleware`， 而又想要针对某个 url 添加 csrf_token 验证，可以添加装饰器：

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_protect  # 针对下面的视图，启用 csrf。模板 form 表单中要加上 {% csrf_token %}
def hello(request):
    return render(request, 'hello.html')
```

**CBV**

针对基于类的视图，上面说的装饰器需要改一下：

```python
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
 
@method_decorator(csrf_exempt, name='dispatch')
class MyCsrfExemptView(View):
 
    def post(self, request):
        return HttpResponse('OK')
```

> 不管是给整个类加装饰器，还是想要给类里面的某个方法（譬如 post) 加装饰器，都只能包裹在 `@method_decorator()` 里面。这个装饰器的可选参数 `name` 可以指定给某个方法加上装饰器。上面例子中的 `name=dispatch` 是给 dispatch 方法加上装饰器， 因为不管是 get，post，put等方法，都是从 dispatch 转发过来的，所以给它加上装饰器，相当于给类里面所有的请求方法都加上了装饰器。

### 自定义中间件

**process_request, process_response**

我们视图函数接受处理的 `request` 和返回的 `respone(HttpResponse)` ,都要经过中间件的处理，才会到达视图函数或者从视图函数发送出去。在 `settings.py` 中，有个 `MIDDLEWARE` 变量，它是一个列表，里面按照**顺序**存放了放多中间件。所有的请求到达视图函数之前，要先按照顺序(列表中从前往后的顺序)经过每个中间件的`process_request()` 方法，传递给下一个中间件，然后到达视图函数，视图函数返回`response`，又会逆着列表中中间件的顺序，经过每个中间件的 `process_response` 方法，一层层逆向传递给中间件，最终发送给用户。

![django_middleware](Django.assets/django_middleware.png)

> 如上图所示：有三个箭头，当用户发起请求是，会依次经过每个中间件的 `process_request()` ，然后达到视图函数。从视图函数返回的 `response` ，有逆着中间件的顺序，依次经过每个中间件的 `process_response()` 达到用户端。
>
> 需要注意的是：一旦某个中间件的 `process_request` 返回了不是 `None` 的返回值，则不会继续传递给其他中间件，而是会直接执行当前中间件的 `process_response` 函数，然后从当前中间件**逆着顺序**，向上传递给其他中间件，最终返回给用户（上图横着的那个箭头代表了这个过程，没有经过视图函数，直接返回）
>
> 因此：`process_request` 不应主动设置返回值（默认返回None)，而 `process_response` 则应该**必须**返回 `response`

下面举个例子：

在 `mysite` 中创建一个 `Middle.py`文件，内容如下：

```python
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddle(MiddlewareMixin):
    def process_response(self, request, response):
        print("Start process response of MyMiddle")
        return response

    def process_request(self, request):
        print("Start process request of MyMiddle.")
        # return HttpResponse("Stop here")  # process_request() 如果有返回值，会直接从此处传递给response，返回给用户，而不会经过视图函数

```

在 `settings.py` 中加入上面创建的自定义中间件：

```python
import mysite

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "mysite.Middle.MyMiddle",  # 这里是自定义的中间件
]
```

然后我们自定义的中间件就起作用了，每次请求发送过来时，都会经过我们的中间件。

**process_view**

针对上面的自定义中间件，我们改成如下：

`Middle.py`

```python
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddle(MiddlewareMixin):
    def process_response(self, request, response):
        print("process response of middle 2")
        return response
	
    # 多写了一个 process_view 函数
    def process_view(self, request, callback, args, kwargs):
        print('view of middle 1')

    def process_request(self, request):
        print("process request of middle 2.")


class MyMiddle2(MiddlewareMixin):
    def process_response(self, request, response):
        print("process response of middle 2")
        return response
	
    # 多写了一个 process_view 函数
    def process_view(self, request, callback, args, kwargs):
        print('view of middle 2')

    def process_request(self, request):
        print("process request of middle 2.")
```

`settings.py` 将两个中间件都注册上

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "mysite.Middle.MyMiddle",
    "mysite.Middle.MyMiddle2",
]
```

随便访问一个url，控制台打印如下：

> 控制台打印的结果：
>
> ```
> process request of middle 1.
> process request of middle 2.
> view of middle 1
> view of middle 2
> view function.					# 视图函数打印的log
> process response of middle 2
> process response of middle 1
> ```
>
> 从上面的log可以看出，中间件先按照顺序执行了 `process_request` 函数，然后转而又从头开始执行了一遍 `process_view` 函数，最后到达视图函数，然后按照逆向的顺序，返回给中间件。



将上面的第一个中间件改动一下，让它的 `process_view` 有个返回值：

```python
class MyMiddle(MiddlewareMixin):
	# 略

    def process_view(self, request, callback, args, kwargs):
        print('view of middle 1')
        # 仅仅改动了这里。callback 就是我们当前请求的"视图函数","args","kwargs"是视图函数的参数。这里调用了视图函数，然后直接返回了 response
        response = callback(request, *args, **kwargs)
        return response
    # 略
```

> 结果如下：
>
> ```
> process request of middle 1.
> process request of middle 2.
> view of middle 1
> view function.		# 在第一个中间件的 process_view 中调用了视图函数，产生的log
> process response of middle 2
> process response of middle 1
> ```
>
> 可以看出，如果某个中间件的`process_view` 有了有效的返回值，则会直接跳转到**最后一个中间件**的 `process_response` 函数，然后逆向传递给它之前的所有中间件。

**process_exception(request,exception)**

```python
def process_exception(self, request, exception):
    print('process_exception')
    return HttpResponse('Error is handled.')
```

这个方法，只有在**视图函数出现异常**时，才会执行。

第一，先执行所有的 process_request

第二，第一步完成后，回头又执行所有的 process_view

第三，如果视图函数出现错误，则逆向执行所有的 process_exception

第四，假如第三步中某个 process_exception 处理了异常，则停止执行下一个 exception，而是直接回到最后一个中间件，逆向执行所有的 process_response

**process_template_response(request, response)**

只有当视图函数返回的对象拥有`.render()` 方法时，才会执行这个函数。

Middle.py:

```python
class MyMiddle(MiddlewareMixin):
	# ...
    
    def process_template_response(self, request, response):
        print('process_template_response')
        return response  # response 代表了视图函数返回的值。
```

views.py

```python
class t:
    def __init__(self, request):
        self.request = request
    def render(self):
        return HttpResponse('This is from render.')

# 视图函数，返回一个对象，它拥有 render()
def test(request):
    print('view function.')
    return t(request)
```

> 结果如下：
>
> ```
> process request of middle 1.
> process request of middle 2.
> view of middle 1
> view function.
> process_template_response
> process response of middle 2
> process response of middle 1
> ```



## Form 组件

### 简单介绍

通常针对 form 表单提交的数据，我们需要自己后台进行数据的校验，譬如针对密码会检验长度，是否为空等，针对form的校验，django提供了一个form组件，可以直接对 form 表单进行约束和校验。

首先，创建一个 `forms.py` ：

```python
from django import forms


class LoginForm(forms.Form):
    # username, password 应该和 html 模板中的 input 标签的 name 属性的值一一对应。
    username = forms.CharField(max_length=15, min_length=8, required=True)  # required 代表是否可以为空
    password = forms.CharField(max_length=15, min_length=8, required=True, error_messages={
        "required": "不能为空",     # 自定义错误信息，键应该和参数名字一致
        "min_length": "最少长度为8",
        "max_length": "最大长度为15",
    })
```

> 首先，这个类要继承自 `forms.Form`。
>
> 其次，我们要定义一些字段：username, password。每一个字段都对应着我们前端页面将要验证的数据。
>
> 这些字段可以设置一些校验规则：`max_length` 校验最大长度，`required ` 校验是否是必填项； `error_messages` 可以自定义不满足条件时的错误提示信息(默认的错误提示是英文的）。

views.py

```python
from django.shortcuts import render, redirect, HttpResponse
from app01.forms import LoginForm  # 导入上面写的form组件


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        f = LoginForm(request.POST)  # 将数据放到表单类里
        if f.is_valid():           # 所有字段是否都校验成功
            print(f.cleaned_data)  # 字典：{"username": 'xxx', "password": 'xxx'}
            return HttpResponse("OK.")
        else:
            print(f.errors)  # f.errors 可以获取校验错误的信息
            print(f.errors['username'][0])  # f.errors[''] 可以获取某个标签字段校验失败的信息
            return render(request, 'login.html', {"f": f})
```

> 我们想要自动进行 form 表单数据的校验，需要将数据传递给 form 组件：`LoginForm(request.POST)` 这样就会将数据和 form **绑定**起来。
>
> form 组件的实例化对象，有几个方法：
>
> `f.is_bound` 是否已经和数据绑定。
>
> `f.is_valid()` 对绑定的数据进行验证，只有当所有的字段都校验成功，才会返回 True
>
> `f.cleaned_data` 针对校验成功的表单，这个属性可以获取提交的数据（字典类型）
>
> `f.errors` 可以获取校验不成功的错误信息。（`f.errors[字段名]` 可以获取某个字段的**所有**错误信息：如：`f.errors['username'][0]` 可以获取 username 字段所有错误的第一条错误信息）

login.html:

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form action="/app01/login/" method="post">
        {% csrf_token %}
        <p>用户名：<input type="text" name="username"> {{ f.errors.username }} </p>
        <p>密码：<input type="password" name="password"> {{ f.errors.password }}  </p>
        <input type="submit" value="submit">
    </form>
</body>
</html>
```

### 自定义校验函数

#### 校验单个字段

上面我们使用了简单的校验方式，可以校验一个字段的长度，是否必填等项目，但是这远远不够，实际项目中我们可能要校验的规则比较复杂，为了能更灵活的自定义校验，我们可以自定义一个 `clean_字段` 函数。

如果我们自定义了一个 `clean_字段` 函数，那么 django 在对基础的数据验证后(也就是自带的那些 `required, max_length, ...` 方法），就会**自动**运行这个方法，额外的对这个字段的数据进行校验。

```python
from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
    # 单选
    choice = forms.ChoiceField(
        choices=((1,'aaa'), (2,'bbb')),
        widget=widgets.Select(attrs={'class': 'class_a'}))

    # 多选
    multi_choices = forms.MultipleChoiceField(choices=((1,"aaa"), (2, "bbb")),
                                              widget=widgets.SelectMultiple)
	# 固定格式：clean_字段名
    def clean_choice(self):
        if self.cleaned_data['choice'] == '1':
            self.cleaned_data['choice'] = 'aaa'
        return self.cleaned_data['choice']  # 要返回当前字段的值
```

> 需要注意的时，当执行 `clean_字段` 函数时，`self.cleaned_data['字段名']` 已经有值了，因为此时数据已经完成了第一步的校验：自带规则的校验。如果数据连自带的规则都不能满足，那根本不会执行这个 `clean_字段` 方法。

#### 额外信息

上面介绍了如何自动额外校验某个字段，下面来介绍在**所有字段都完成校验后**，如何进行一次整体的数据清洗。

```python
from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
    # 单选
    choice = forms.ChoiceField(
        choices=((1,'aaa'), (2,'bbb')),
        widget=widgets.Select(attrs={'class': 'class_a'}))

    # 多选
    multi_choices = forms.MultipleChoiceField(choices=((1,"aaa"), (2, "bbb")),
                                              widget=widgets.SelectMultiple)

    def clean_choice(self):
        if self.cleaned_data['choice'] == '1':
            self.cleaned_data['choice'] = 'aaa'
        return self.cleaned_data['choice']

    # clean 方法是在所有字段都完成校验后，会主动运行的方法。你可以在这里进行额外的设置
    def clean(self):
        self.cleaned_data['new'] = 'new data'
        return self.cleaned_data
```

> clean() 方法会在所有的字段完成校验后，自动执行的方法。有了它，可以让你进行一些额外的操作，校验。上面的例子中，我们添加了一个额外的数据。发挥你的想象力，你可以在这里做任何事情。



### 自动生成 html 标签

 其实只要我们建立一个 from 组件的类，譬如 `forms.py` 中我们定义的 `class LoginForm(forms.Form)`，这个类的对象，本身就可以**转换成简单的 html 标签**

下面我们依然使用上文中的创建的 `forms.py` ，使用 `python manage.py shell` 进入交互命令行：

```python
>>> from app01.forms import LoginForm

# 手动给 form 组件绑定数据，键是字段名，值相当于用户输入的用户名和密码
>>> f = LoginForm({"username": "asdbjallfa", "password": "ppppppppps"})
>>> f
<LoginForm bound=True, valid=Unknown, fields=(username;password)>


# 尽管 f 是一个对象，但是我们打印它，会调用它的 __str__() 方法，可以看出，它的内容是 html 类型的 
>>> print(f)
<tr>
    <th><label for="id_username">Username:</label></th>
    <td>
      <input type="text" name="username" value="asdbjallfa" maxlength="15" minlength="8" required id="id_username">
    </td>
  </tr>
  <tr>
    <th><label for="id_password">Password:</label></th>
    <td>
      <input type="text" name="password" value="ppppppppps" maxlength="15" minlength="8" required id="id_password">
    </td>
  </tr>


# 还可以单独打印某个字段的 html 内容
>>> print(f['username'])
<input type="text" name="username" value="asdbjallfa" maxlength="15" minlength="8" required id="id_username">


# as_p() 可以将 f 对象的内容，转换成 <p> 标签
>>> f.as_p()
'<p>\n    <label for="id_username">Username:</label>\n    <input type="text" name="username" value="asdbjallfa" maxlength="15" minlength="8" required id="id_userna
me">\n    \n    \n  </p>\n\n  \n  <p>\n    <label for="id_password">Password:</label>\n    <input type="text" name="password" value="ppppppppps" maxlength="15" min
length="8" required id="id_password">\n    \n    \n      \n    \n  </p>'
```

> 我们可以直接给 form 组件绑定值：`LoginForm({'字段'："value"})`
>
> 一个 form 表单的对象，本身就可以转换成 html 标签。并且还可以通过 `f['字段名']` 来获取某个字段的标签，这样我们在模板中可以使用 `{{ f.字段名 }}` 来生成某个标签。

> 可以看出 form 组件的对象，有个 `as_p()` 方法，可以直接将此组件转换成 `<p>` 标签。不仅如此，它还有其他两个类似的方法：`as_table()`, `as_ul()` 可以将组件转换成 `<table>` ，`<li>` 标签

有了上面的知识，我们前端页面可以少些两个标签了：

login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form action="/app01/login/" method="post">
        {% csrf_token %}
        {{ f.as_p }}     		<!-- 使用 form 组件自动转换的标签 -->
        <input type="submit" value="submit">
    </form>
</body>
</html>
```

views.py 中要传递 form 组件给前端

```python
def login(request):
    if request.method == "GET":
        f = LoginForm()                                  # 创建一个 form 组件对象
        return render(request, 'login.html', {"f": f})   # 传递给前端，自动生成标签
    else:
        f = LoginForm(request.POST)  # 将数据放到表单类里
        if f.is_valid():           # 所有字段是否都校验成功
            return HttpResponse("OK.")
        else:
            return render(request, 'login.html', {"f": f})  # 传递给前端
```



**小贴士：**

在我们手动给 form 绑定值时，有两个不同的参数可以使用：

```python
>>> f = LoginForm(data={"phone":'1293', 'choice': 1})  # 使用了 data 参数
>>> f.is_bound
True												   # True 说明真的绑定了值


>>> f = LoginForm(initial={"phone":'1293', 'choice': 1})  # 使用了 initial 参数
>>> f.is_bound
False												   # 没绑定上

```

可以看出，使用了 `data` 参数，会真的将数据和 form 绑定上，并且 form 会校验这个数据。而使用了 `initial` 参数的数据，仅仅起到**初始化 form 组件**的作用，它并不会真的和 form 绑定上，也不会去校验这个数据。



### 常用的 Field

我们在 Form 组件的类里面，要定义不同的字段，每个字段的类型可能都不同，django 有几种常用的 field：

```python
EmailField
IntegerField
CharField
DateField
RegexField
ChoiceField           # 单选
MultipleChoiceField   # 多选
```

值得一提的是 `RegexField` ，它允许用户自定义正则表达式类型，来进行数据验证：

```python
class LoginForm(forms.Form):
    phone = forms.RegexField('188\d{8}', required=True, label='电话')
```

> 它的第一个参数是正则表达式。会根据这个表达式，来对用户输入的数据进行验证。这样的话，我们就可以自己定义一些特殊的规则了。

### Field 参数

**field 常用的参数**

之前我们已经用过了几种不同的参数：

```python
CharField(
    max_length=15, 
    min_length=8, 
    required=True, 
    error_messages={
        "required": "不能为空",     # 自定义错误信息，键应该和参数名字一致
        "min_length": "最少长度为8",
        "max_length": "最大长度为15"}
)
```

我们再说两个参数:

```python
phone = forms.RegexField('188\d{8}', initial='188xxx', label='电话')
```

> 当我们使用 Form 组件自动生成 html 标签时：
>
> initial 可以指定当前 Field 的初始默认值。
>
> label 可以指定当前标签的 label 名（譬如当前的 `phone` 字段，默认的 label 是：`Phone` , 指定 label 后，label 就是 ”电话“

**非常重要的参数：widget**

widget 参数，可以设置标签的类型。

上面我们提到的几个 `Field` ，在前端的页面上，显示的都是 `<input type="text" />` ，也就是全是 text 类型，所以如果你想要设置：单选框，多选框，下拉菜单等样式的输入框，就需要设置 widget 这个参数。

譬如：

```python
class LoginForm(forms.Form):
    phone = forms.RegexField('188\d{8}',  initial='188xxx')
    choice = forms.CharField(widget=widgets.RadioSelect(choices=((1,'上海'),(2,'北京'),)))
```

下面的例子，摘抄自：https://www.cnblogs.com/wupeiqi/aiticles/6144178.html

```python
# 单radio，值为字符串
# user = fields.CharField(
#     initial=2,
#     widget=widgets.RadioSelect(choices=((1,'上海'),(2,'北京'),))
# )
 
# 单radio，值为字符串
# user = fields.ChoiceField(
#     choices=((1, '上海'), (2, '北京'),),
#     initial=2,
#     widget=widgets.RadioSelect
# )
 
# 单select，值为字符串
# user = fields.CharField(
#     initial=2,
#     widget=widgets.Select(choices=((1,'上海'),(2,'北京'),))
# )
 
# 单select，值为字符串
# user = fields.ChoiceField(
#     choices=((1, '上海'), (2, '北京'),),
#     initial=2,
#     widget=widgets.Select
# )
 
# 多选select，值为列表
# user = fields.MultipleChoiceField(
#     choices=((1,'上海'),(2,'北京'),),
#     initial=[1,],
#     widget=widgets.SelectMultiple
# )
 
 
# 单checkbox
# user = fields.CharField(
#     widget=widgets.CheckboxInput()
# )
 
 
# 多选checkbox,值为列表
# user = fields.MultipleChoiceField(
#     initial=[2, ],
#     choices=((1, '上海'), (2, '北京'),),
#     widget=widgets.CheckboxSelectMultiple
# )
```

**widget 设置标签属性**

widget 中，还可以自定义一些标签的属性.

forms.py

```python
from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
    phone = forms.RegexField('188\d{8}',
                             initial='188xxx',
                             widget=widgets.TextInput(attrs={'id': "1111111111", 'class': 'aaaaaaa'})
                             )
```

> widgets 中有很多的小组件，每个小组件都有一个 `attrs` 参数，可以接受字典类型的数据。通过它，我们可以设置生成的标签的属性。



## 通用视图

### 老方式

对于一些视图函数，有些人可能还觉得说太麻烦了，譬如一些详情页：用户发来请求，我就想从数据库中取个值，然后返回给用户就行，可是还是要这样写：

视图：views.py

```python
from django.shortcuts import render
from . import models

def book(request):
    books = models.Books.objects.all()  # 查询 Books 模型中的所有书籍信息
    return render(request, 'app01/books_list.html', {"object_list": books})
```

> 说明一下：django 可以自动识别到 `项目名/APP名/templates/` 这个目录，我们的模板存放在：`项目名/APP名/templates/App名/xxx.html` 
>
> 之所以要在 `templates` 下再次创建一个 `app名` 的文件夹，是为了防止多个app之间使用了重名的模板，因为 app名是不可重复的，所以这样类似于起到了唯一标识的作用。

当然，模型层和 url 路由还是必不可少的：

models.py

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=10)


class Books(models.Model):
    title = models.CharField(max_length=10)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
```

urls.py

```python
from django.urls import path, include
from . import views

urlpatterns = [
    path('detail/', views.book),
]
```

books_list.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <ul>
        {% for book in object_list %}
            <li>{{ book.title }}</li>
        {% endfor %}
    </ul>

</body>
</html>
```

### 新方式

**基础使用**

使用新方式，我们直接修改上文中的视图函数就行：

views.py

```python
from django.views.generic import ListView  # 导入 ListView
from . import models

class Book(ListView):  # 写个类，继承 ListView
    model = models.Books  # model = 模型层中的 Books 模型
```

> ListView 故名思意，就是用来展示一个 List 的所有内容。它的原理和我们上面写的老方式一样：它会自动给你查询 Books 模型中的数据，然后返回给用户。在这个过程中，它会自动绑定 `request`,  自动查找到 `app01` 这个应用下的模板html，自动给模板填充一个 `object_list`  上下文，自动将渲染后的数据返回给用户。
>
> 模板查找规则：自动去： `项目名/应用名/templates/应用名/` 下查找 `模型名_list.html`
>
> 自动生成的上下文规则：`object_list`
>
> 这两个规则就是定死的，记住就行了。

**自定义模板名和上下文名**

当然，如果你不想使用默认的模板和上下文的名字：`模型名_list.html` 和 `object_list` ，你也可以自己指定这两个变量的名字：

```python
class Book(ListView):
    model = models.Books
    template_name = 'app01/books.html'    # 需要将模板名改成 books.html
    context_object_name = 'my_books'  # 模板中的 object_list 也要改成这个
```

**添加额外的 context 上下文**

```python
class Book(ListView):
    model = models.Books
    template_name = 'books.html'
   
    def get_context_data(self, **kwargs): 
         # 调用基类的方法
        context = super(Book, self).get_context_data(**kwargs)
        # 添加一个额外的 context
        context['book_list'] = Book.objects.all() 
        return context 
```

### 对象的子集: queryset

上面我们使用了 `model` 参数来指定某个模型，并使用了 `Listview` 来查询一些数据。但其实我们还可以使用 `queryset` 参数来查询一些数据。

依然是上面用到的模型, views.py 改动了一下：

```python
from django.views.generic import ListView
from . import models


class Book(ListView):
    queryset = models.Books.objects.order_by('-title')  # 可以写 ORM 查询语句，更灵活了
    context_object_name = 'my_books'
    template_name = 'app01/books.html'
```

> 提升点：queryset 参数可以直接使用 ORM 查询语句

上面的 queryset 参数后面只能跟一句话，如果你想要执行多个查询语句，或者需要对查询出来的数据进行二次查询，可以使用 `get_queryset()` 方法:

```python
from django.views.generic import DetailView, ListView
from . import models


class Book(ListView):
    template_name = 'app01/books.html'
    context_object_name = 'my_books'
    def get_queryset(self):
        """
        这个方法会自动调用。
        我们在这个函数里面查询了所有的书籍，并将它的结果，存到了 self.book 属性中。
        """
        self.book = models.Books.objects.all()
        self.book = self.book.filter(id__gt=3)
        return self.book

    def get_context_data(self, **kwargs):
        # 调用父类方法，先获取默认的 context 对象
        context = super(Book, self).get_context_data(**kwargs)

        # 添加额外的上下文，传递给前端页面
        context['books'] = self.book
        context['args'] = self.args  # self.args 是自带的属性，里面是 url 的正则匹配到的结果（假如你的这个 url 使用了正则的话）
        return context
```

> get_queryset() 会自动执行。你可以在这里面查询一些数据，它返回一个 `queryset`，默认返回的是：`self.model._default_manager.all()`，可以看出，这个方法默认返回的是一个下模型的 `.all()` 



## 模板引擎

可以参考《Mastering Django》这本书的第三章：Templates。也可以查看中文翻译版：http://djangobook.py3k.cn/2.0/chapter04/。（链接用的版本有点太老了，但是模板部分还行）

这里还是简单说一下吧。

模板中，有两种类型可以构造我们的网页：

1. 变量。可以将一个变量的值嵌套在网页中，形如：`{{ varibale }}`
2. 标签(Tag)，可以对数据进行简单的逻辑处理，形如：`{% if  %}  ....  {% endif %}`

### 简单的变量

我们通过 `render()` 函数，可以传递给模板一个 `context` 对象，这个对象包含了我们想要给前端模板传递的变量，通常我们会直接传递一个字典类型的数据，它会自动转换成 `context` ，譬如：

```python
def login(request):
    #...
    return render(request, 'xxx.html', {"name": "Wztshine"})  # 最后一个字典类型的参数
```

相应的前端：`xxx.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ name }}   <!-- name 是传递过来的字典的键 -->
</body>
</html>
```

不仅是常规的数据类型，我们还可以传递**字典，列表，对象**等数据类型：

```python
class Person():
    name = "name123"
    def get_name(self):
        return self.name

def login(request):
    #...
    context = {
        "name": "Wztshine",
        "age": 20,
        "addr": ["Beijing", "FengTai"],
        "obj": Person(),
        "dict": {"key1": 1, "key2": 2}
              }
    return render(request, 'xxx.html', context)  # 最后一个字典类型的参数
```

前端页面：`xxx.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ name }}   <!-- name 是传递过来的字典的键 -->
    {{ age }}
    {{ addr.0 }}  <!-- 通过'.' 获取索引为 0 的列表的值 -->
    {{ obj.name }}  <!-- 调用对象的属性 -->
    {{ obj.get_name }}  <!-- 调用对象的方法，不用加 () -->
    {{ dict.key1 }}  <!-- 通过 '.' 获取字典的 key1 的值 -->
</body>
</html>
```

> 我们可以看出，无论是列表，字典还是对象，都是通过 '.' 来获取它们的索引或键或属性。需要注意的是，针对一个对象，我们只能调用其**不带参数**的方法。

### 标签

标签可以处理数据，进行一些逻辑判断等操作：

```python
class Person():
    name = "name123"
    def get_name(self):
        return self.name

def login(request):
    #...
    context = {
        "addr": ["Beijing", "FengTai"],
        "dict": {"key1": 1, "key2": 2}
              }
    return render(request, 'xxx.html', context)  # 最后一个字典类型的参数
```

前端 `xxx.html` :

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
	{% for item in  addr %}   <!-- for 循环 -->
    <p>
        {{ forloop.counter }}  <!-- for 循环中特殊的用来计数的变量，从1开始 -->
        {{ item }}
    </p>
    {% endfor %}  <!-- 别忘了闭合 -->
</body>
</html>
```

除了 `{% for ... %} {% endfor %}`, 还有其他如：

```html
{% if xx %}
	...
{% else %}
	...
{% endif %}

```

#### 过滤

我们用管道符 `|` 来进行数据的过滤，简单来说将管道符前面的变量作为参数，传递给管道符后面的函数，从而对变量进行一些设置，如大小写转换：

```python
def login(request):
    #...
    return render(request, 'xxx.html', {"name": "Wztshine"})  # 最后一个字典类型的参数
```

html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ name|lower }}   <!-- name 转换成小写 -->
    {{ name|truncatewords:"30" }}  <!-- 显示 name 的前30个字符 -->
</body>
</html>
```

> 在过滤时，我们可以通过 `:"arg"` 来对过滤函数进行传递参数。

传递标签：

```python
def login(request):
    #...
    context = {
        "tag": "<script> alert(123) </script>",
              }
    return render(request, 'xxx.html', context)
```

html：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ tag|safe }}   <!-- 加上 safe，可以让传递过来的tag变成真实的 html 标签，而不是解析成字符串。因此这里会执行一个 script 脚本，弹出 123. -->
</body>
</html>
```



### 母版

为了减少冗余，django 可以将一个模板拆分开，分成多个模块，在使用的时候，可以将多个模块拼接在一起，这样可以实现 html 代码的重用。

 layout.html：使用 `{% block <blockName> %}{% endblock %}` 来预留空间，给子模板使用。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/plugins/bootstrap-3.3.7-dist/css/bootstrap.css" />
    <link rel="stylesheet" href="/static/plugins/font-awesome-4.7.0/css/font-awesome.css" />
    <link rel="stylesheet" href="/static/css/common.css" />
    {% block css %}{% endblock %}  <!-- 预留了一个名为 css 的block -->

</head>
<body>
    <div class="pg-header">
        <div class="logo left">XX用户管理</div>
        <div class="avatar right" style="position:relative;">
            <img style="width:40px;height:40px" src="/static/images/avatar.jpg">
            <div class="user-info">
                <a>个人信息</a>
                <a>注销</a>
            </div>
        </div>
        <div class="rmenus right">
            <a><i class="fa fa-commenting-o fa-lg"></i> 消息</a>
            <a><i class="fa fa-envelope fa-lg"></i> 邮件</a>
        </div>
    </div>
    <div class="pg-body">
        <div class="menus">
            <a href="/student/"><i class="fa fa-gg fa-lg"></i>学生管理</a>
            <a href="/classes/"><i class="fa fa-gg fa-lg"></i>班级管理</a>
            <a href="/teacher/"><i class="fa fa-gg fa-lg"></i>老师管理</a>
        </div>
        <div class="content">
			<!-- 预留了一个名为 content 的block -->
            {% block content %}{% endblock %}

        </div>
    </div>

    {% block js %}{% endblock %}
</body>
</html>
```

子版使用：`{% extends 'layout.html' %}`

```html
{% extends 'layout.html' %}  <!-- 要写在 block 的上方,意思是继承自 layout.html -->

{% block content %}  <!-- 使用此 content block 覆盖母版的 content block -->
       <form method="post" action="/add_class/" style="padding-top:20px;padding-left:20px;">
        <p>班级名称：<input type="text" name="title"/></p>
        <input type="submit" value="提交" />
    	</form>
{% endblock %}
```

> 子模板会将 content block 替换到母版的 content block，然后将替换后的母版内容显示出来（类似于编程语言的继承，然后重写父类的某个方法，从而实现既拥有父类的其他方法，还拥有了重写后的自身的方法）

### include

include 和母版的功能类似，但是原理不同。母版有点像是继承的关系，而 include 则是直接包含的关系。也就是说，在一个母版里面，我们可以使用 `{% include 'xxx.html' %}` 来将 `xxx.html` 包含进来。

譬如：

hello.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>

</head>
<body>
    {% include 'pub.html' %}  <!-- 将 pub.html 包含进来 -->
</body>
</html>
```

在 `templates` 文件夹下创建一个新的 `pub.html`:

```html
<p>This is a p</p>
<p>{{ name }}</p>   <!-- 包含了一个 name 变量 -->
```

views.py

```python
def users(request):
    return render(request, 'hello.html', {'name': 'wang'})
```

> 我们在 views.py 中，给 hello.html 模板传递了一个包含了 name 变量的上下文。在 hello.html 中，又包含了 pub.html 模板。我们传递的 name 变量，也会传递给 pub.html 中定义的 {{ name }}



### 自定义标签

#### filter

在django中，我们可以自定义一些标签，从而可以在模板中使用自己定义的标签函数等。譬如下面的例子创建一个自定义的过滤器：实现字符串的首字母大写。

第一，要在 App 文件夹中创建一个 `templatetags` 模块（这个App要在 `settings.py` 中注册上，否则肯定无法访问）

第二，在 `templatetags` 模块中，随意创建一个 `.py` 文件，如 `my_tag.py`

第三，在 `my_tag.py` 中，写入：

```python
from django import template

register = template.Library()  # 固定写法，不能改动。

@register.filter   # 装饰器，将下面的函数装饰成一个 filter
def str_title(s1, s2):  # 自定义函数
    return s1.title() + s2.title()
```

> 注意：一个 filter 装饰的函数，最多只能接受两个参数！

第四，在模板中，就可以这样使用：

我们的 views.py：

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def users(request):
    return render(request, 'hello.html', {'name': 'wang'})
```

hello.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>

</head>
<body>
    {% load my_tag %}  <!-- 先加载我们创建的 my_tag.py  -->
    {{ name|str_title:"good" }}  <!-- str_title 就是我们自定义的函数 -->
</body>
</html>
```

> 注意：`str_title` 后面紧跟了一个冒号和一个字符串。这个字符串将作为 `str_title` 的第二个参数。

#### simple_tag

在上面 `filter` 部分，我们创建了一个 `filter` 类型的函数，可以使用管道符 `|` 进行函数的使用。这里还有另一种类型的标签：

`my_tag.py`:

```python
from django import template

register = template.Library()

@register.filter
def str_title(s1, s2):
    return s1.title() + s2.title()


@register.simple_tag  # simple_tag 类型
def str_tag(s1, s2, s3):   # 这种类型的变量可以很多，不限制在2个以内
    return f"{s1} {s2} {s3}"
```

使用：

views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def users(request):
    return render(request, 'hello.html', {'name': 'wang', "addr": 'Beijing'})
```

hello.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>

</head>
<body>
    {% load my_tag %}
    {{ name|str_title:"good" }}  <!-- 这里是 {{ }} 标签 -->

    {% str_tag addr 'DaXing' 'Qu' %}  <!-- 这里使用了 {% %} 标签 -->
</body>
</html>
```

> 注意：这里使用的是 {% 类型的标签，而且变量直接放置在函数的后面，用**空格**隔开，作为参数传递给我们自定义的 `str_tag` 函数。

---

#### 不同之处

总结一下：filter 和 simple_tag 类型的不同之处：

第一，filter 装饰器装饰的函数，只能接受两个参数。simple_tag 装饰的函数，不限制参数个数

第二，filter 装饰的函数，可以用在逻辑判断语句中，而 simple_tag 装饰的函数，不能用在逻辑判断语句，示例如下：

新建一个filter函数，它总是返回 True or False

```python
from django import template

register = template.Library()

@register.filter
def return_true(s1):
    return True
```

在模板中使用：

```html
    {% if name|return_true %}  <!-- 注意：return_true 这个 filter 函数，可以用在逻辑判断 if 语句等里面！ -->
        <b>{{ name }}</b>
    {% endif %}
```





## 配置mysql

首先，需要在 `settings.py` 中配置一下：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'school',  # 要连接的数据库名
        'USER': 'root',    # 用户名
        'PASSWORD': '123456',  # 密码
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```

找到 `settings.py` 同目录下的 `__init__.py` ，写入以下内容：

```python
import pymysql
pymysql.install_as_MySQLdb()
```

然后就可以在视图中使用mysql了。

譬如：

```python
def students(request):
    if request.method == 'GET':
        conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='school', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select * from student;')
        students = cursor.fetchall()
        return render(request, 'students.html', {'students': students})
```

封装的mysql：

```python
import pymysql


class SQL(object):
    def __init__(self, user, passwd, database, host, port, charset):
        self.__user = user
        self.__passwd = passwd
        self.__database = database
        self.__host = host
        self.__port = port
        self.__charset = charset

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__passwd, database=self.__database, charset=self.__charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 游标，用来执行sql语言，查询结果使用字典 {字段：value, ...}

    def select_one(self, string, args=None):
        """select one data from the query result.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.(optional)
        :return:
        """
        self.cursor.execute(string, args)
        return self.cursor.fetchone()  # 获取一条查询结果

    def select_all(self, string, args=None):
        """select all data from a query result.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.(optional)
        :return:
        """
        self.cursor.execute(string, args)
        return self.cursor.fetchall()

    def __modify(self, string, args=None):
        """modify a query, like to insert into a table, or update some data.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.(optional)
        :return:
        """
        lines = self.cursor.execute(string, args)
        self.conn.commit()  # commit changes to the database.
        return lines  # return affected lines' number.

    def insert_one(self, string, args):
        """insert one data to a table.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.
        :return:
        """
        line = self.__modify(string, args)
        return self.cursor.lastrowid  # 返回最新的 id

    def insert_many(self, string, args):
        """insert many datas to a table.

        :param string:  query to execute on server
        :param args: Sequence of sequences or mappings.  It is used as parameter.
        :return:
        """
        self.cursor.executemany(string, args)
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, string, args):
        """update some data.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.
        :return:
        """
        line = self.__modify(string, args)
        return line

    def delete(self, string, args=None):
        """delete some data.

        :param string:  query to execute on server
        :param args: tuple, list or dict.  It is used as parameter.
        :return:
        """
        line = self.__modify(string, args)
        return line

    def close(self):
        self.cursor.close()
        self.conn.close()

        
if __name__ == "__main__":
    # database: school; table: student; table columns: id int, name varchar, score int;
    sql = SQL('root', '123456', 'school', '127.0.0.1', 3306, 'utf8')
    sql.insert_many('insert into student(id,name,score) values(%s,%s,%s)',
                    [(1,'zhang',30), (2,'wang',50), (8, 'zhang', 50), (9, 'wnag', 100)])
    sql.select_one('select * from student where id=%s', (1,))
    sql.select_all('select * from student;')
    sql.insert_one("insert into student(id, name, score) values(%s, %s, %s)", (7, 'wang', 80))
    sql.insert_many('insert into student(id,name,score) values(%s,%s,%s)', [(8,'zhang',50), (9,'wnag',100)])
    sql.delete('delete from student where id=%s', (9,))
    sql.update('update student set name=%s where id=%s', ('llllllll', 8))
```



## 附录

### 获取前端列表

当前端有多选框等信息时，后端可以通过 `request.POST.getlist()` 获取列表：

`request.POST` , `request.GET` 都只是一个类字典对象，但并不是真正的字典，所以它还有一些其他方法。

前端：text.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form method="post">
        {% csrf_token %}
        <p>please select: </p>
        <!-- 一个多选下拉菜单，会给后台发送列表类型的数据 -->
        <select multiple size="5" name="choices">
            <option>1111</option>
            <option>2222</option>
            <option>3333</option>
            <option>4444</option>
            <option>5555</option>
        </select>
        <br>
        <input type="submit" value="submit">
    </form>
    {{ value }}
</body>
</html>
```

视图：

```python
def test(request):
    if request.method == 'GET':
        return render(request, 'test.html')
    else:
        choices = request.POST.getlist('choices')  # getlist 可以获取传递的列表
        return render(request, 'test.html', {"value": choices})
```



### Model模型操作

参考自 : https://www.cnblogs.com/wupeiqi/aiticles/6216618.html

#### 字段类型

```
AutoField(Field)
        - int自增列，必须填入参数 primary_key=True

BigAutoField(AutoField)
    - bigint自增列，必须填入参数 primary_key=True

    注：当model中如果没有自增列，则自动会创建一个列名为id的列
    from django.db import models

    class UserInfo(models.Model):
        # 自动创建一个列名为id的且为自增的整数列
        username = models.CharField(max_length=32)

    class Group(models.Model):
        # 自定义自增列
        nid = models.AutoField(primary_key=True)
        name = models.CharField(max_length=32)

SmallIntegerField(IntegerField):
    - 小整数 -32768 ～ 32767

PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
    - 正小整数 0 ～ 32767
IntegerField(Field)
    - 整数列(有符号的) -2147483648 ～ 2147483647

PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
    - 正整数 0 ～ 2147483647

BigIntegerField(IntegerField):
    - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

BooleanField(Field)
    - 布尔值类型

NullBooleanField(Field):
    - 可以为空的布尔值

CharField(Field)
    - 字符类型
    - 必须提供max_length参数， max_length表示字符长度

TextField(Field)
    - 文本类型

EmailField(CharField)：
    - 字符串类型，Django Admin以及ModelForm中提供验证机制

IPAddressField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供验证 IPV4 机制

GenericIPAddressField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供验证 Ipv4和Ipv6
    - 参数：
        protocol，用于指定Ipv4或Ipv6， 'both',"ipv4","ipv6"
        unpack_ipv4， 如果指定为True，则输入::ffff:192.0.2.1时候，可解析为192.0.2.1，开启刺功能，需要protocol="both"

URLField(CharField)
    - 字符串类型，Django Admin以及ModelForm中提供验证 URL

SlugField(CharField)
    - 字符串类型，Django Admin以及ModelForm中提供验证支持 字母、数字、下划线、连接符（减号）

CommaSeparatedIntegerField(CharField)
    - 字符串类型，格式必须为逗号分割的数字

UUIDField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供对UUID格式的验证

FilePathField(Field)
    - 字符串，Django Admin以及ModelForm中提供读取文件夹下文件的功能
    - 参数：
            path,                      文件夹路径
            match=None,                正则匹配
            recursive=False,           递归下面的文件夹
            allow_files=True,          允许文件
            allow_folders=False,       允许文件夹

FileField(Field)
    - 字符串，路径保存在数据库，文件上传到指定目录
    - 参数：
        upload_to = ""      上传文件的保存路径
        storage = None      存储组件，默认django.core.files.storage.FileSystemStorage

ImageField(FileField)
    - 字符串，路径保存在数据库，文件上传到指定目录
    - 参数：
        upload_to = ""      上传文件的保存路径
        storage = None      存储组件，默认django.core.files.storage.FileSystemStorage
        width_field=None,   上传图片的高度保存的数据库字段名（字符串）
        height_field=None   上传图片的宽度保存的数据库字段名（字符串）

DateTimeField(DateField)
    - 日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]

DateField(DateTimeCheckMixin, Field)
    - 日期格式      YYYY-MM-DD

TimeField(DateTimeCheckMixin, Field)
    - 时间格式      HH:MM[:ss[.uuuuuu]]

DurationField(Field)
    - 长整数，时间间隔，数据库中按照bigint存储，ORM中获取的值为datetime.timedelta类型

FloatField(Field)
    - 浮点型

DecimalField(Field)
    - 10进制小数
    - 参数：
        max_digits，小数总长度
        decimal_places，小数位长度

BinaryField(Field)
    - 二进制类型




Django字段默认值对应的 sql类型：
    'AutoField': 'integer AUTO_INCREMENT',
    'BigAutoField': 'bigint AUTO_INCREMENT',
    'BinaryField': 'longblob',
    'BooleanField': 'bool',
    'CharField': 'varchar(%(max_length)s)',
    'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
    'DateField': 'date',
    'DateTimeField': 'datetime',
    'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
    'DurationField': 'bigint',
    'FileField': 'varchar(%(max_length)s)',
    'FilePathField': 'varchar(%(max_length)s)',
    'FloatField': 'double precision',
    'IntegerField': 'integer',
    'BigIntegerField': 'bigint',
    'IPAddressField': 'char(15)',
    'GenericIPAddressField': 'char(39)',
    'NullBooleanField': 'bool',
    'OneToOneField': 'integer',
    'PositiveIntegerField': 'integer UNSIGNED',
    'PositiveSmallIntegerField': 'smallint UNSIGNED',
    'SlugField': 'varchar(%(max_length)s)',
    'SmallIntegerField': 'smallint',
    'TextField': 'longtext',
    'TimeField': 'time',
    'UUIDField': 'char(32)',
```

**字段的参数**

```
# ------------ 针对数据库约束 ---------------
null                数据库中字段是否可以为空
db_column           数据库中字段的列名
default             数据库中字段的默认值
primary_key         数据库中字段是否为主键
db_index            数据库中字段是否可以建立索引
unique              数据库中字段是否可以建立唯一索引
unique_for_date     数据库中字段【日期】部分是否可以建立唯一索引
unique_for_month    数据库中字段【月】部分是否可以建立唯一索引
unique_for_year     数据库中字段【年】部分是否可以建立唯一索引

#------------- 针对 admin 后台 -------------
verbose_name        Admin中显示的字段名称
blank               Admin中是否允许用户输入为空
editable            Admin中是否可以编辑
help_text           Admin中该字段的提示信息
choices             Admin中显示选择框的内容，用不变动的数据放在内存中从而避免跨表操作
                    如：gf = models.IntegerField(choices=[(0, '何穗'),(1, '大表姐'),],default=1)

error_messages      自定义错误信息（字典类型），从而定制想要显示的错误信息；
                    字典健：null, blank, invalid, invalid_choice, unique, and unique_for_date
                    如：{'null': "不能为空.", 'invalid': '格式错误'}

validators          自定义错误验证（列表类型），从而定制想要的验证规则
                    from django.core.validators import RegexValidator
                    from django.core.validators import EmailValidator,URLValidator,DecimalValidator,\
                    MaxLengthValidator,MinLengthValidator,MaxValueValidator,MinValueValidator
                    如：
                        test = models.CharField(
                            max_length=32,
                            error_messages={
                                'c1': '优先错信息1',
                                'c2': '优先错信息2',
                                'c3': '优先错信息3',
                            },
                            validators=[
                                RegexValidator(regex='root_\d+', message='错误了', code='c1'),
                                RegexValidator(regex='root_112233\d+', message='又错误了', code='c2'),
                                EmailValidator(message='又错误了', code='c3'), ]
                        )
```

#### 元信息

在一个模型里面，定义一个类：`Meta` ，里面可以设置一些数据库表信息

```python
class UserInfo(models.Model):
        nid = models.AutoField(primary_key=True)
        username = models.CharField(max_length=32)
        class Meta:
            # 自定义数据库中生成的表名称 默认 app名称 + 下划线 + 类名
            db_table = "table_name"

            # 联合索引
            index_together = [
                ("pub_date", "deadline"),
            ]

            # 联合唯一索引
            unique_together = (("driver", "restaurant"),)

            # admin中显示的表名称
            verbose_name

            # verbose_name加s
            verbose_name_plural
```

#### 多表关系和参数

```python
# -------------------------- 一对多 ------------------------------
ForeignKey(ForeignObject) # ForeignObject(RelatedField)
        to,                         # 要进行关联的表名
        to_field=None,              # 要关联的表中的字段名称
        on_delete=None,             # 当删除关联表中的数据时，当前表与其关联的行的行为
                                        - models.CASCADE，删除关联数据，与之关联也删除
                                        - models.DO_NOTHING，删除关联数据，引发错误IntegrityError
                                        - models.PROTECT，删除关联数据，引发错误ProtectedError
                                        - models.SET_NULL，删除关联数据，与之关联的值设置为null（前提FK字段需要设置为可空）
                                        - models.SET_DEFAULT，删除关联数据，与之关联的值设置为默认值（前提FK字段需要设置默认值）
                                        - models.SET，删除关联数据，
                                                      a. 与之关联的值设置为指定值，设置：models.SET(值)
                                                      b. 与之关联的值设置为可执行对象的返回值，设置：models.SET(可执行对象)

                                                        def func():
                                                            return 10

                                                        class MyModel(models.Model):
                                                            user = models.ForeignKey(
                                                                to="User",
                                                                to_field="id"
                                                                on_delete=models.SET(func),)
        related_name=None,          # 反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
        related_query_name=None,    # 反向操作时，使用的连接前缀，用于替换【表名】     如： models.UserGroup.objects.filter(表名__字段名=1).values('表名__字段名')
        limit_choices_to=None,      # 在Admin或ModelForm中显示关联数据时，提供的条件：
                                    # 如：
                                            - limit_choices_to={'nid__gt': 5}
                                            - limit_choices_to=lambda : {'nid__gt': 5}

                                            from django.db.models import Q
                                            - limit_choices_to=Q(nid__gt=10)
                                            - limit_choices_to=Q(nid=8) | Q(nid__gt=10)
                                            - limit_choices_to=lambda : Q(Q(nid=8) | Q(nid__gt=10)) & Q(caption='root')
        db_constraint=True          # 是否在数据库中创建外键约束
        parent_link=False           # 在Admin中是否显示关联数据


# -------------------------- 一对一 ------------------------------


OneToOneField(ForeignKey)
    to,                         # 要进行关联的表名
    to_field=None               # 要关联的表中的字段名称
    on_delete=None,             # 当删除关联表中的数据时，当前表与其关联的行的行为

                                ###### 对于一对一 ######
                                # 1. 一对一其实就是 一对多 + 唯一索引
                                # 2.当两个类之间有继承关系时，默认会创建一个一对一字段
                                # 如下会在A表中额外增加一个c_ptr_id列且唯一：
                                        class C(models.Model):
                                            nid = models.AutoField(primary_key=True)
                                            part = models.CharField(max_length=12)

                                        class A(C):
                                            id = models.AutoField(primary_key=True)
                                            code = models.CharField(max_length=1)


# -------------------------- 多对多 ------------------------------


ManyToManyField(RelatedField)
    to,                         # 要进行关联的表名
    related_name=None,          # 反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
    related_query_name=None,    # 反向操作时，使用的连接前缀，用于替换【表名】     如： models.UserGroup.objects.filter(表名__字段名=1).values('表名__字段名')
    limit_choices_to=None,      # 在Admin或ModelForm中显示关联数据时，提供的条件：
                                # 如：
                                        - limit_choices_to={'nid__gt': 5}
                                        - limit_choices_to=lambda : {'nid__gt': 5}

                                        from django.db.models import Q
                                        - limit_choices_to=Q(nid__gt=10)
                                        - limit_choices_to=Q(nid=8) | Q(nid__gt=10)
                                        - limit_choices_to=lambda : Q(Q(nid=8) | Q(nid__gt=10)) & Q(caption='root')
    symmetrical=None,           # 仅用于多对多自关联时，symmetrical用于指定内部是否创建反向操作的字段
                                # 做如下操作时，不同的symmetrical会有不同的可选字段
                                    models.BB.objects.filter(...)

                                    # 可选字段有：code, id, m1
                                        class BB(models.Model):

                                        code = models.CharField(max_length=12)
                                        m1 = models.ManyToManyField('self',symmetrical=True)

                                    # 可选字段有: bb, code, id, m1
                                        class BB(models.Model):

                                        code = models.CharField(max_length=12)
                                        m1 = models.ManyToManyField('self',symmetrical=False)

    through=None,               # 自定义第三张表时，使用字段用于指定关系表
    through_fields=None,        # 自定义第三张表时，使用字段用于指定关系表中那些字段做多对多关系表
                                    from django.db import models

                                    class Person(models.Model):
                                        name = models.CharField(max_length=50)

                                    class Group(models.Model):
                                        name = models.CharField(max_length=128)
                                        members = models.ManyToManyField(
                                            Person,
                                            through='Membership',
                                            through_fields=('group', 'person'),
                                        )

                                    class Membership(models.Model):
                                        group = models.ForeignKey(Group, on_delete=models.CASCADE)
                                        person = models.ForeignKey(Person, on_delete=models.CASCADE)
                                        inviter = models.ForeignKey(
                                            Person,
                                            on_delete=models.CASCADE,
                                            related_name="membership_invites",
                                        )
                                        invite_reason = models.CharField(max_length=64)
    db_constraint=True,         # 是否在数据库中创建外键约束
    db_table=None,              # 默认创建第三张表时，数据库中表的名称
```

#### 数据表操作

```python
# 获取个数
#
# models.Tb1.objects.filter(name='seven').count()

# 大于，小于
#
# models.Tb1.objects.filter(id__gt=1)              # 获取id大于1的值
# models.Tb1.objects.filter(id__gte=1)              # 获取id大于等于1的值
# models.Tb1.objects.filter(id__lt=10)             # 获取id小于10的值
# models.Tb1.objects.filter(id__lte=10)             # 获取id小于10的值
# models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值

# in
#
# models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
# models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in

# isnull
# Entry.objects.filter(pub_date__isnull=True)

# contains
#
# models.Tb1.objects.filter(name__contains="ven")
# models.Tb1.objects.filter(name__icontains="ven") # icontains大小写不敏感
# models.Tb1.objects.exclude(name__icontains="ven")

# range
#
# models.Tb1.objects.filter(id__range=[1, 2])   # 范围bettwen and

# 其他类似
#
# startswith，istartswith, endswith, iendswith,

# order by
#
# models.Tb1.objects.filter(name='seven').order_by('id')    # asc
# models.Tb1.objects.filter(name='seven').order_by('-id')   # desc

# group by
#
# from django.db.models import Count, Min, Max, Sum
# models.Tb1.objects.filter(c1=1).values('id').annotate(c=Count('num'))
# SELECT "app01_tb1"."id", COUNT("app01_tb1"."num") AS "c" FROM "app01_tb1" WHERE "app01_tb1"."c1" = 1 GROUP BY "app01_tb1"."id"

# limit 、offset
#
# models.Tb1.objects.all()[10:20]

# regex正则匹配，iregex 不区分大小写
#
# Entry.objects.get(title__regex=r'^(An?|The) +')
# Entry.objects.get(title__iregex=r'^(an?|the) +')

# date
#
# Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))
# Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))

# year
#
# Entry.objects.filter(pub_date__year=2005)
# Entry.objects.filter(pub_date__year__gte=2005)

# month
#
# Entry.objects.filter(pub_date__month=12)
# Entry.objects.filter(pub_date__month__gte=6)

# day
#
# Entry.objects.filter(pub_date__day=3)
# Entry.objects.filter(pub_date__day__gte=3)

# week_day
#
# Entry.objects.filter(pub_date__week_day=2)
# Entry.objects.filter(pub_date__week_day__gte=2)

# hour
#
# Event.objects.filter(timestamp__hour=23)
# Event.objects.filter(time__hour=5)
# Event.objects.filter(timestamp__hour__gte=12)

# minute
#
# Event.objects.filter(timestamp__minute=29)
# Event.objects.filter(time__minute=46)
# Event.objects.filter(timestamp__minute__gte=29)

# second
#
# Event.objects.filter(timestamp__second=31)
# Event.objects.filter(time__second=2)
# Event.objects.filter(timestamp__second__gte=31)


        
        
        
        
        ##################################################################
# PUBLIC METHODS THAT ALTER ATTRIBUTES AND RETURN A NEW QUERYSET #
##################################################################

def all(self)
    # 获取所有的数据对象

def filter(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q

def exclude(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q

def select_related(self, *fields)
     性能相关：表之间进行join连表操作，一次性获取关联的数据。
     model.tb.objects.all().select_related()
     model.tb.objects.all().select_related('外键字段')
     model.tb.objects.all().select_related('外键字段__外键字段')

def prefetch_related(self, *lookups)
    性能相关：多表连表操作时速度会慢，使用其执行多次SQL查询在Python代码中实现连表操作。
            # 获取所有用户表
            # 获取用户类型表where id in (用户表中的查到的所有用户ID)
            models.UserInfo.objects.prefetch_related('外键字段')



            from django.db.models import Count, Case, When, IntegerField
            Article.objects.annotate(
                numviews=Count(Case(
                    When(readership__what_time__lt=treshold, then=1),
                    output_field=CharField(),
                ))
            )

            students = Student.objects.all().annotate(num_excused_absences=models.Sum(
                models.Case(
                    models.When(absence__type='Excused', then=1),
                default=0,
                output_field=models.IntegerField()
            )))

def annotate(self, *args, **kwargs)
    # 用于实现聚合group by查询

    from django.db.models import Count, Avg, Max, Min, Sum

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id'))
    # SELECT u_id, COUNT(ui) AS `uid` FROM UserInfo GROUP BY u_id

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id')).filter(uid__gt=1)
    # SELECT u_id, COUNT(ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id',distinct=True)).filter(uid__gt=1)
    # SELECT u_id, COUNT( DISTINCT ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

def distinct(self, *field_names)
    # 用于distinct去重
    models.UserInfo.objects.values('nid').distinct()
    # select distinct nid from userinfo

    注：只有在PostgreSQL中才能使用distinct进行去重

def order_by(self, *field_names)
    # 用于排序
    models.UserInfo.objects.all().order_by('-id','age')

def extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
    # 构造额外的查询条件或者映射，如：子查询

    Entry.objects.extra(select={'new_id': "select col from sometable where othercol > %s"}, select_params=(1,))
    Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
    Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
    Entry.objects.extra(select={'new_id': "select id from tb where id > %s"}, select_params=(1,), order_by=['-nid'])

 def reverse(self):
    # 倒序
    models.UserInfo.objects.all().order_by('-nid').reverse()
    # 注：如果存在order_by，reverse则是倒序，如果多个排序则一一倒序


 def defer(self, *fields):
    models.UserInfo.objects.defer('username','id')
    或
    models.UserInfo.objects.filter(...).defer('username','id')
    #映射中排除某列数据

 def only(self, *fields):
    #仅取某个表中的数据
     models.UserInfo.objects.only('username','id')
     或
     models.UserInfo.objects.filter(...).only('username','id')

 def using(self, alias):
     指定使用的数据库，参数为别名（setting中的设置）


##################################################
# PUBLIC METHODS THAT RETURN A QUERYSET SUBCLASS #
##################################################

def raw(self, raw_query, params=None, translations=None, using=None):
    # 执行原生SQL
    models.UserInfo.objects.raw('select * from userinfo')

    # 如果SQL是其他表时，必须将名字设置为当前UserInfo对象的主键列名
    models.UserInfo.objects.raw('select id as nid from 其他表')

    # 为原生SQL设置参数
    models.UserInfo.objects.raw('select id as nid from userinfo where nid>%s', params=[12,])

    # 将获取的到列名转换为指定列名
    name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
    Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)

    # 指定数据库
    models.UserInfo.objects.raw('select * from userinfo', using="default")

    ################### 原生SQL ###################
    from django.db import connection, connections
    cursor = connection.cursor()  # cursor = connections['default'].cursor()
    cursor.execute("""SELECT * from auth_user where id = %s""", [1])
    row = cursor.fetchone() # fetchall()/fetchmany(..)


def values(self, *fields):
    # 获取每行数据为字典格式

def values_list(self, *fields, **kwargs):
    # 获取每行数据为元祖

def dates(self, field_name, kind, order='ASC'):
    # 根据时间进行某一部分进行去重查找并截取指定内容
    # kind只能是："year"（年）, "month"（年-月）, "day"（年-月-日）
    # order只能是："ASC"  "DESC"
    # 并获取转换后的时间
        - year : 年-01-01
        - month: 年-月-01
        - day  : 年-月-日

    models.DatePlus.objects.dates('ctime','day','DESC')

def datetimes(self, field_name, kind, order='ASC', tzinfo=None):
    # 根据时间进行某一部分进行去重查找并截取指定内容，将时间转换为指定时区时间
    # kind只能是 "year", "month", "day", "hour", "minute", "second"
    # order只能是："ASC"  "DESC"
    # tzinfo时区对象
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.UTC)
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.timezone('Asia/Shanghai'))

    """
    pip3 install pytz
    import pytz
    pytz.all_timezones
    pytz.timezone(‘Asia/Shanghai’)
    """

def none(self):
    # 空QuerySet对象


####################################
# METHODS THAT DO DATABASE QUERIES #
####################################

def aggregate(self, *args, **kwargs):
   # 聚合函数，获取字典类型聚合结果
   from django.db.models import Count, Avg, Max, Min, Sum
   result = models.UserInfo.objects.aggregate(k=Count('u_id', distinct=True), n=Count('nid'))
   ===> {'k': 3, 'n': 4}

def count(self):
   # 获取个数

def get(self, *args, **kwargs):
   # 获取单个对象

def create(self, **kwargs):
   # 创建对象

def bulk_create(self, objs, batch_size=None):
    # 批量插入
    # batch_size表示一次插入的个数
    objs = [
        models.DDD(name='r11'),
        models.DDD(name='r22')
    ]
    models.DDD.objects.bulk_create(objs, 10)

def get_or_create(self, defaults=None, **kwargs):
    # 如果存在，则获取，否则，创建
    # defaults 指定创建时，其他字段的值
    obj, created = models.UserInfo.objects.get_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 2})

def update_or_create(self, defaults=None, **kwargs):
    # 如果存在，则更新，否则，创建
    # defaults 指定创建时或更新时的其他字段
    obj, created = models.UserInfo.objects.update_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 1})

def first(self):
   # 获取第一个

def last(self):
   # 获取最后一个

def in_bulk(self, id_list=None):
   # 根据主键ID进行查找
   id_list = [11,21,31]
   models.DDD.objects.in_bulk(id_list)

def delete(self):
   # 删除

def update(self, **kwargs):
    # 更新

def exists(self):
   # 是否有结果

```



### django 分页

views.py

```python
def test(request):
    from django.shortcuts import render
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    # 生成一些数据，作为前台展示
    L = []
    for i in range(999):
        L.append(i)

    current_page = request.GET.get('p')
    paginator = Paginator(L, 10)  # 针对 L 列表进行分页，每页 10 条数据
    """
    paginator 对象有如下属性：
        per_page: 每页显示条目数量
        count:    数据总个数
        num_pages:总页数
        page_range:总页数的索引范围，如: (1,10),(1,200)
        page:     page对象
    """

    try:
        posts = paginator.page(current_page)  # 获取当前页应该展示的数据
        """
        page 对象有如下属性：
            has_next              是否有下一页
            next_page_number      下一页页码
            has_previous          是否有上一页
            previous_page_number  上一页页码
            object_list           分页之后的数据列表
            number                当前页
            paginator             paginator对象
        """
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'posts': posts})
```

index.html:

```html
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<ul>
    {% for item in posts %}
        <li>{{ item }}</li>
    {% endfor %}
</ul>

<div>
      <span>
        {% if posts.has_previous %}
            <a href="?p={{ posts.previous_page_number }}">Previous</a>
        {% endif %}
          <span>
            Page {{ posts.number }} of {{ posts.paginator.num_pages }}.
          </span>
          {% if posts.has_next %}
              <a href="?p={{ posts.next_page_number }}">Next</a>
          {% endif %}
      </span>

</div>
</body>
</html>
```

### settings.py 设置

在 `settings.py` 中，有个 `TEMPLATES` 设置，这里介绍一下这个设置。

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- BACKEND: 指定了后端使用的模板语言：django 模板（因为其实还有其他模板语言，如 jinja2）
- DIRS：指定了模板的存放位置。这里的例子是项目的根目录的 `templates` 文件夹。
- APP_DIRS：设置是否也去每个已经安装的 App 的目录下寻找模板。因为我们每创建安装一个App，都可以在这个App 的目录下建立一个 `templates/` 的文件夹，你还可以在这里面继续创建文件夹：`this_app_name/template.html` 。这样的话，如果这个选项是 True，django 也能自动找到 `template.html` 
- OPTIONS：这里面又有一个参数：context_processors. 这里面注册了一些 processors。processor 的工作流程是这样的：我们知道，我们的视图函数必须有一个参数：譬如我们通常写的 `request`，这个 request 在传递给视图函数之前，会依次经过每个 processor 的处理。每个 processor 都会在 request 对象里面添加一些键值对信息，仅此而已。(详细信息，可以参考《Mastering Django: Core》这本书第八章)

### 文件上传

使用 `request.FILES["file_name"]` 可以查看上传的文件，返回一个文件对象。这个文件对象拥有几个重要的属性和方法：`name`, `size`, `chunks()`。前两个属性很好理解，就是文件名和文件大小。后一个 `chunks()` 方法可以获取文件的二进制内容。

**普通方式**

views.py

```python
import pathlib

from django.shortcuts import render, HttpResponse


def upload(request):
    if request.method == "GET":
        return render(request, 'upload.html')
    else:
        # 获取用户上传的文件
        file = request.FILES.get('user_file')
        # file 对象的属性：文件名和文件大小
        file_name = file.name
        file_size = file.size
        f = open(pathlib.PurePath('static') / file_name, 'wb')
        
        # file.chunks() 可以获取文件块，然后存储起来
        for c in file.chunks():
            f.write(c)
		f.close()
        return HttpResponse('ok')

```

upload.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
	<!-- 需要上传文件，form 表单要设置属性 enctype -->
    <form action="/app01/upload/" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="user_file">
        <br>
        <input type="submit" value="submit">
    </form>
</body>
</html>

```

**Form 组件形式**

views.py

```python
import pathlib

from django.shortcuts import render, HttpResponse
from app01.forms import Upload


def upload(request):
    if request.method == "GET":
        f = Upload()
        return render(request, 'upload.html', {'form': f})
    else:
        f = Upload(data=request.POST, files=request.FILES)  # 注意这里，files=request.FILES 
        if f.is_valid():
            file = f.cleaned_data['user_file']
            file_name = file.name
            fh = open(pathlib.PurePath('static') / file_name, 'wb')
            for c in file.chunks():
                fh.write(c)
            fh.close()
            return HttpResponse('ok')
        else:
            return HttpResponse("error")

```

forms.py

```python
from django import forms


class Upload(forms.Form):
    user_file = forms.FileField(required=True)
```

upload.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="/app01/upload/" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.user_file }}
        <br>
        <input type="submit" value="submit">
    </form>
</body>
</html>
```