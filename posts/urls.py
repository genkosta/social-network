from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('post-list/', views.PostList.as_view(), name='post_list'),
    path('view-post/<slug:slug>/', views.PostDetail.as_view(), name='view_post')
]
