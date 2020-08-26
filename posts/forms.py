from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group", "image"]
        labels = {
            'text': _("Текст"),
            'group': _('Группа'),
            'image': _('Изображение')
        }
        help_text = {
            'text': _('Я не придумал текст, но он есть =)')
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        text = forms.CharField(widget=forms.Textarea)
