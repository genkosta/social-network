# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer -  Users posts.
    Сериализатор - Cообщения пользователей.
    """
    class Meta:
        model = Post
        fields = ('title', 'message', 'like')
