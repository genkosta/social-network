# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.translation import ugettext as _

# Views Classes
from django.views.generic import ListView
from django.views.generic import DetailView

# Web API
from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from .serializers import PostSerializer

# Models
from .models import Post

# Forms
from .forms import CreatePostForm


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

class PostsViewSet(viewsets.ModelViewSet):
    """
    User posts - Viewing, creation, updating, like, unlike.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        """ Viewing all posts """
        default_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        PageNumberPagination.page_size = request.GET.get('per_page', default_page_size)
        queryset = Post.objects.filter(is_disable=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None):
        """ View post """
        queryset = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @action(methods=['post'], detail=True)
    def add_like(request, pk=None):
        """ Add like """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.like += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @action(methods=['post'], detail=True)
    def add_unlike(request, pk=None):
        """ Add unlike """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.unlike += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_user_posts(self, request):
        """ Viewing user posts """
        user_pk = request.user.pk
        default_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        PageNumberPagination.page_size = request.GET.get('per_page', default_page_size)
        queryset = Post.objects.filter(user__pk=user_pk, is_disable=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @staticmethod
    @action(methods=['get'], detail=True)
    def get_user_post(request, pk=None):
        """ View user post """
        user_pk = request.user.pk
        queryset = get_object_or_404(Post, pk=pk, user__pk=user_pk)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class UserPostsViewSet(viewsets.ModelViewSet):
    """
    Posts of user - Viewing, creation, updating.
    Сообщения пользователя - Просмотр, создание, обновление.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @staticmethod
    def create(request):
        form = CreatePostForm(request.POST)

        if form.is_valid():
            user = request.user
            queryset = form.save(commit=False)
            queryset.user = user
            queryset.save()
            serializer = PostSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = {}
            for field, errors in form.errors.items():
                response[field] = '; '.join(errors)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update(request, pk=None):
        user_pk = request.user.pk
        post = Post.objects.filter(user__pk=user_pk, pk=pk).first()

        if post is None:
            response = {
                'error': _('Update error - Post does not belong to the current user')
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        form = CreatePostForm(request.POST, instance=post)

        if form.is_valid():
            queryset = form.save(commit=False)
            queryset.like = 0
            queryset.unlike = 0
            queryset.save()
            serializer = PostSerializer(queryset)
            return Response(serializer.data)
        else:
            response = {}
            for field, errors in form.errors.items():
                response[field] = '; '.join(errors)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

# End - Web API ------------------------------------------------------------------------------------
