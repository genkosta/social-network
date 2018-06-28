# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import Http404
from django.utils.translation import ugettext as _

# Views Classes
from django.views.generic import ListView
from django.views.generic import DetailView

# Web API
from rest_framework import viewsets, permissions, status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PostSerializer
from social_network.core.versioning import PostVersioning

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

    queryset = Post.objects.filter(is_disable=False)\
        .prefetch_related(
        Prefetch('user', queryset=User.objects.only('first_name', 'last_name')
                 .prefetch_related(
            Prefetch('profile', queryset=Profile.objects.only('image'))
        )),
        Prefetch('comments', queryset=Comment.objects.filter(is_disable=False)
                 .prefetch_related(
            Prefetch('user', queryset=User.objects.only('first_name', 'last_name')
                     .prefetch_related(
                Prefetch('profile', queryset=Profile.objects.only('image'))
            ))
        ))
    )

    serializer_class = PostSerializer
    versioning_class = PostVersioning

    @staticmethod
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='like'
    )
    def add_like(request, pk=None):
        """ Add like """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.like += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope],
        url_path='unlike'
    )
    def add_unlike(request, pk=None):
        """ Add unlike """
        queryset = get_object_or_404(Post, pk=pk)
        queryset.unlike += 1
        queryset.save()
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.user.id != request.user.id:
                msg = {'error': _('Only the author can delete the post.')}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint: Users posts - Viewing, creation, updating, like, unlike.
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
'''
# End - Web API ------------------------------------------------------------------------------------
