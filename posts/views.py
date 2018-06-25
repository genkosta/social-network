# -*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic import DetailView

# Web API
from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Models
from .models import Post


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

# End - Web API ------------------------------------------------------------------------------------
