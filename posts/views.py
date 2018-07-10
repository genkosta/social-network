# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import Http404

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
    serializer_class = PostSerializer
    versioning_class = PostVersioning

    def get_custom_queryset(self, pk=None, user=None):
        rating = self.request.query_params.get('sort')
        order_by_fields = ['-pk']
        filter_fields = {'is_disable': False}

        if pk is not None:
            filter_fields['pk'] = pk

        if user is not None:
            filter_fields['user'] = user

        if rating == 'rating':
            order_by_fields.insert(0, '-rating')
        elif rating == 'last':  # unrequired
            pass

        queryset = Post.objects.filter(**filter_fields).prefetch_related(
            Prefetch('user', queryset=User.objects.only('first_name', 'last_name').prefetch_related(
                Prefetch('profile', queryset=Profile.objects.only('image'))
            )),
            Prefetch('comments', queryset=Comment.objects.filter(is_disable=False).prefetch_related(
                Prefetch('user',
                         queryset=User.objects.only('first_name', 'last_name').prefetch_related(
                             Prefetch('profile', queryset=Profile.objects.only('image'))
                         ))
            ))
        ).order_by(*order_by_fields)[:1000]

        if queryset.count() == 0:
            raise Http404

        if pk is not None:
            queryset = queryset.first()

        return queryset

    def list(self, request, version=None):
        queryset = self.get_custom_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, version=None):
        queryset = self.get_custom_queryset(pk=pk)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
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
        url_path='unlike'
    )
    def add_unlike(self, request, pk=None, version=None):
        """ Add unlike """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.unlike += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None, version=None):
        user = request.user
        instance = self.get_custom_queryset(pk=pk, user=user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    @action(
        methods=['get'],
        detail=False,
        url_path='owner'
    )
    def get_user_posts(self, request, version=None):
        """ Viewing user posts """
        user = request.user
        queryset = self.get_custom_queryset(user=user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        url_path='owner'
    )
    def get_user_post(self, request, pk=None, version=None):
        """ View user post """
        user = request.user
        queryset = self.get_custom_queryset(pk=pk, user=user)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
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

    def update(self, request, pk=None, version=None):
        user = request.user
        queryset = self.get_custom_queryset(pk=pk, user=user)
        serializer = PostSerializer(queryset, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None, version=None):
        user = request.user
        queryset = self.get_custom_queryset(pk=pk, user=user)
        serializer = PostSerializer(queryset, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# End - Web API ------------------------------------------------------------------------------------
