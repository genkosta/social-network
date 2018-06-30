# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.utils.translation import ugettext as _

# Views Classes
from django.views.generic import ListView
from django.views.generic import DetailView

# Web API
from rest_framework import viewsets, permissions, status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PostSerializer, CommentSerializer
from social_network.core.drf_versioning import PostVersioning

# Models
from .models import Post, Comment
from django.contrib.auth.models import User
from accounts.models import Profile


class PostList(ListView):
    """
    Get post list
    """
    model = Post
    allow_empty = False
    template_name = "posts/post_list.html"
    context_object_name = "posts"


class PostDetail(DetailView):
    """
    Get a post for viewing.
    """
    model = Post
    allow_empty = False
    template_name = "posts/view_post.html"
    context_object_name = 'post'

    def get_queryset(self):
        post = Post.objects.filter(slug=self.kwargs['slug'])
        return post


# Start - Web API ----------------------------------------------------------------------------------

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint: Users posts - Viewing, creation, updating, like, unlike.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    queryset = Post.objects.filter(is_disable=False).prefetch_related(
        Prefetch('user', queryset=User.objects.only('first_name', 'last_name').prefetch_related(
            Prefetch('profile', queryset=Profile.objects.only('image'))
        )),
        Prefetch('comments', queryset=Comment.objects.filter(is_disable=False).prefetch_related(
            Prefetch('user', queryset=User.objects.only('first_name', 'last_name').prefetch_related(
                Prefetch('profile', queryset=Profile.objects.only('image'))
            ))
        ))
    )[:1000]

    serializer_class = PostSerializer
    versioning_class = PostVersioning

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='like'
    )
    def add_like(self, request, pk=None, version=None):
        """ Add like """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.like += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='unlike'
    )
    def add_unlike(self, request, pk=None, version=None):
        """ Add unlike """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.unlike += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id != request.user.id:  # Check copyright
            msg = {'error': _('Only the author can delete the post.')}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='owner'
    )
    def get_user_posts(self, request, version=None):
        """ Viewing user posts """
        user_pk = request.user.pk
        queryset = Post.objects.filter(user__pk=user_pk, is_disable=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='owner'
    )
    def get_user_post(self, request, pk=None, version=None):
        """ View user post """
        user_pk = request.user.pk
        queryset = get_object_or_404(Post, pk=pk, user__pk=user_pk)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='comment'
    )
    def add_comment(self, request, pk=None, version=None):
        """ Add comment """
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post)
        return Response(serializer.data)

# End - Web API ------------------------------------------------------------------------------------
