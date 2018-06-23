# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from . import views as main_views


urlpatterns = [
    path('robots\.txt', main_views.robots, name='robots'),
    path('admin/', admin.site.urls),
    path('', main_views.HomePageView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG and settings.STATUS_PROJECT == 'local':
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

