# -*- coding: utf-8 -*-
from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    """ Create post """

    class Meta:
        model = Post
        fields = ('title', 'message')
