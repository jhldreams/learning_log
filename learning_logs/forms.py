from django import forms

from .models import Topic


class TopicForm(forms.ModelForm):
    """Topic的表单"""

    # Meta类是告诉Django根据哪个模型创建表单，以及在表单中包含哪些字段
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
