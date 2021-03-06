# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import static

# Views
from . import views as main_views
from .core import views as core_views

# Web API
from rest_framework.authtoken import views as authtoken_views
from posts import views as posts_views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'(?P<version>(v1))/integrations/posts', posts_views.PostViewSet, base_name='post')


urlpatterns = [
    # Robots file
    path('robots\.txt', main_views.robots, name='robots'),
    # Admin panel
    path('admin/', admin.site.urls),
    # Web API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', authtoken_views.obtain_auth_token),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/', include(router.urls)),
    # Login, Sign up
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', core_views.signup, name='signup'),
    # Posts
    path('posts/', include('posts.urls', namespace='web_posts')),
    # Home page
    path('', main_views.HomePageView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG and settings.STATUS_PROJECT == 'local':
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
