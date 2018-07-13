# -*- coding: utf-8 -*-
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from django.utils import formats

from social_network.core.models import validate_image

from .models import Post, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer - Users posts """

    user = serializers.SerializerMethodField('get_user_data')
    comment_list = serializers.SerializerMethodField('get_comments')
    created_at = serializers.SerializerMethodField('get_date_created')

    image = Base64ImageField(required=False, allow_null=True, validators=[validate_image])
    title = serializers.CharField(max_length=50, required=True)
    message = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'user', 'image', 'title', 'message', 'like',
                  'unlike', 'created_at', 'comment_list')
        read_only_fields = ('id', 'user', 'like', 'unlike', 'created_at')

    def get_user_data(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        user = obj.user
        try:
            image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.image.url)
        except ValueError:
            image_url = None

        result = {
            'avatar': image_url,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return result

    def get_date_created(self, obj):
        return formats.date_format(obj.created_at, 'DATETIME_FORMAT')

    def get_comments(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        comments = obj.comments.all()
        result = []
        for comment in comments:
            user = comment.user
            try:
                image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.image.url)
            except ValueError:
                image_url = None
            result.append({
                'avatar': image_url,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'message': comment.text,
                'created_at': formats.date_format(comment.created_at, 'DATETIME_FORMAT')
            })
        return result

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user  # Add author
        return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer - Publish comments for posts """

    user = serializers.SerializerMethodField('get_user_data')
    text = serializers.CharField(max_length=200, required=True)
    created_at = serializers.SerializerMethodField('get_date_created')

    class Meta:
        model = Comment
        fields = ('user', 'text', 'created_at')

    def get_user_data(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        user = obj.user
        try:
            image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.image.url)
        except ValueError:
            image_url = None

        result = {
            'avatar': image_url,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return result

    def get_date_created(self, obj):
        return formats.date_format(obj.created_at, 'DATETIME_FORMAT')
