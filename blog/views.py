from django.shortcuts import render

from django.http import HttpResponse

from . import models

def index(request):
    post_list = models.Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', {"post_list": post_list})
