# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import login, authenticate

# Views_Classes
from django.views.generic.base import TemplateView

# Web API
from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Forms
from .forms import SignUpForm


class HomePageView(TemplateView):
    """
    Home page
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['msg'] = "Hello World!"
        return context


def robots(request):
    """
    Robots file
    :param request:
    :return:
    """

    return render(request, 'robots.txt', {
        'host': request.get_host(),
        'scheme': request.scheme,
        'STATUS_PROJECT': settings.STATUS_PROJECT},
        content_type='text/plain')
