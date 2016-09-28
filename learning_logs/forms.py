from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Topic的表单"""

    # Meta类是告诉Django根据哪个模型创建表单，以及在表单中包含哪些字段
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
