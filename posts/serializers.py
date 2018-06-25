# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer -  Users posts.
    Сериализатор - Cообщения пользователей.
    """

    image = serializers.SlugRelatedField(
        read_only=True,
        slug_field='get_link_avatar',
        source='cover_and_avatar'
    )

    class Meta:
        model = Post
        fields = ('image', 'title', 'message', 'like', 'unlike')
