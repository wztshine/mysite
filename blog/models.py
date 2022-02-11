from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """文章类型"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    """博客"""

    # 博客的 标题，内容，摘要
    title = models.CharField(max_length=70)
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)

    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(default=timezone.now)

    # 外键一对多：一个类型可以对应多篇文章
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 多对多：一个标签可以对应多个文章，每个文章也可以有多个标签
    tags = models.ManyToManyField(Tag, blank=True)
    # 一对多外键：一个作者可以有多个文章
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

