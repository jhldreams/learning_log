# coding:utf-8

from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm


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


# 处理刚进入状态和提交表单后重定向到topics
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


def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据,创建空表单
        form = EntryForm()
    else:
        # POST提交数据
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    """编辑现有的文章"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    print('Here')

    if request.method != 'POST':
        # 第一次请求，用当前的条目填充表单
        form = EntryForm(instance=entry)
    else:
        # 修改后POST重新提交文章
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
