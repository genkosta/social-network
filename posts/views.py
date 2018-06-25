# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.conf import settings

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

class AllPostsViewSet(viewsets.ModelViewSet):
    """
    View all posts - Viewing, like, unlike.
    Просмотр всех постов - Просмотр, лайк, дизлайк.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        default_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        PageNumberPagination.page_size = request.GET.get('per_page', default_page_size)
        queryset = Post.objects.filter(is_disable=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

    @staticmethod
    @action(methods=['post'], detail=True)
    def add_like(request, pk=None):
        queryset = get_object_or_404(Post, pk=pk)
        queryset.like += 1
        queryset.save()
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

    @staticmethod
    @action(methods=['post'], detail=True)
    def add_unlike(request, pk=None):
        queryset = get_object_or_404(Post, pk=pk)
        queryset.unlike += 1
        queryset.save()
        serializer = PostSerializer(queryset)
        return Response(serializer.data)


class UserPostsViewSet(viewsets.ModelViewSet):
    """
    Posts of user - Viewing, creation, updating.
    Сообщения пользователя - Просмотр, создание, обновление.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        user_pk = request.user.pk
        default_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        PageNumberPagination.page_size = request.GET.get('per_page', default_page_size)
        queryset = Post.objects.filter(user__pk=user_pk, is_disable=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

    @staticmethod
    def create(request):
        form = CreatePostForm(request.POST)

        if form.is_valid():
            user = request.user
            queryset = form.save(commit=False)
            queryset.user = user
            queryset.save()
            serializer = PostSerializer(queryset)
            return Response(serializer.data)
        else:
            response = {}
            for field, errors in form.errors.items():
                response[field] = '; '.join(errors)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

# End - Web API ------------------------------------------------------------------------------------
