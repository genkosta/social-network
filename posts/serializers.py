# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.sites.models import Site
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer -  Users posts.
    Сериализатор - Cообщения пользователей.
    """

    image = serializers.SerializerMethodField('get_url_image')
    current_site = Site.objects.get_current()

    class Meta:
        model = Post
        fields = ('id', 'image', 'title', 'message', 'like', 'unlike')

    def get_url_image(self, obj):
        try:
            image_url = obj.middle.url
            result = 'https://{0}{1}'.format(self.current_site.domain, image_url)
        except ValueError:
            result = ""
        return result
