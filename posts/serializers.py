# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer - Comments """

    class Meta:
        model = Comment
        fields = ('url', 'id', 'text', 'created_at')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer - Users posts """

    user = serializers.SerializerMethodField('get_user_data')
    comment_list = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Post
        fields = ('url', 'id', 'user', 'image', 'title', 'message', 'like',
                  'unlike', 'created_at', 'comment_list')

    def get_user_data(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        user = obj.user
        try:
            image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.middle.url)
        except ValueError:
            image_url = ""

        result = {
            'avatar': image_url,
            'author': user.get_full_name()
        }
        return result

    def get_comments(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        comments = obj.comments.filter(is_disable=False).prefetch_related('user')
        result = []
        for comment in comments:
            user = comment.user
            try:
                image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.thumbnail.url)
            except ValueError:
                image_url = ""
            result.append({
                'avatar': image_url,
                'author': user.get_full_name(),
                'message': comment.text,
                'created_date': comment.created_at
            })
        return result
