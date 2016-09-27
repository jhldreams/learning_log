# coding:utf-8

from django.shortcuts import render
from .models import Topic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm


# Create your views here.

def index(request):
    """学习笔记的主页"""

    return render(request, 'learning_logs/index.html')


def topics(request):
    """显示所有的主题"""

    tps = Topic.objects.order_by('-date_added')

    context = {'topics': tps}

    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """显示特定主题的详细页面"""
    tp = Topic.objects.get(id=topic_id)
    entries = tp.entry_set.order_by('-date_added')
    context = {'topic': tp, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)


# 1、处理刚进入状态和提交表单后重定向到topics
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据；创建一个新表单
        form = TopicForm
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
