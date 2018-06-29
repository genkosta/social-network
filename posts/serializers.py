# -*- coding: utf-8 -*-
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField

from django.utils.translation import ugettext_lazy as _
from social_network.core.models import validate_image

from django.contrib.auth.models import User
from .models import Post
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('image',)


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile')
        read_only_fields = ('first_name', 'last_name')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer - Users posts """

    user = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )

    comment_list = serializers.SerializerMethodField('get_comments')
    image = Base64ImageField(required=False, allow_null=True, validators=[validate_image])
    title = serializers.CharField(max_length=50, required=True)
    message = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'user', 'image', 'title', 'message', 'like',
                  'unlike', 'created_at', 'comment_list')
        read_only_fields = ('id', 'user', 'created_at')

    def get_comments(self, obj):
        request = self.context['request']
        scheme = request.scheme
        host = request.get_host()
        comments = obj.comments.all()
        result = []
        for comment in comments:
            user = comment.user
            try:
                image_url = '{0}://{1}{2}'.format(scheme, host, user.profile.thumbnail.url)
            except ValueError:
                image_url = None
            result.append({
                'avatar': image_url,
                'author': user.get_full_name(),
                'message': comment.text,
                'created_at': comment.created_at
            })
        return result

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user  # Add author
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        if instance.user.id == request.user.id:  # Check copyright
            instance.title = validated_data.get('title', instance.title)
            instance.message = validated_data.get('message', instance.message)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(_('Only the author can update the post.'))

    def partial_update(self, instance, validated_data):
        request = self.context['request']
        if not instance.user.id == request.user.id:  # Check copyright
            instance.title = validated_data.get('title', instance.title)
            instance.message = validated_data.get('message', instance.message)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(_('Only the author can update the post.'))
