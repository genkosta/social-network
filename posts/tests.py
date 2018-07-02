# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from .models import Post
from .views import PostViewSet


PostViewSet.permission_classes.pop()

test_image_base64 = """
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
"""


class CreatePostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')

    def test_can_create_post(self):
        """
        Ensure we can create a new post object.
        """
        url = '/api/v1/integrations/posts/'
        data = {
            'user': self.superuser.id,
            'title': 'Test Post',
            'message': 'Hello world!',
            'image': test_image_base64
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadPostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_read_post_list(self):
        """
        Ensure we can read posts.
        """
        url = '/api/v1/integrations/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_post_detail(self):
        """
        Ensure we can read post.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdatePostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_update_post(self):
        """
        Ensure we can update post.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/'
        data = {
            'title': 'Changed Post',
            'message': 'Hello world!'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_delete_post(self):
        """
        Ensure we can delete post.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LikePostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_like_post(self):
        """
        Ensure we can add like.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_unlike_post(self):
        """
        Ensure we can add unlike.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/unlike/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserPostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_read_user_post_list(self):
        """
        Ensure we can read user posts.
        """
        url = '/api/v1/integrations/posts/owner/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_post_detail(self):
        """
        Ensure we can read user post.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/owner/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddCommentPostTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@site.net', '1234')
        self.client.login(username='admin', password='1234')
        data = {
            'user': self.superuser,
            'title': 'Test Post',
            'message': 'Hello world!'
        }
        self.post = Post.objects.create(**data)

    def test_can_add_comment(self):
        """
        Ensure we can add comment.
        """
        url = f'/api/v1/integrations/posts/{self.post.id}/comment/'
        data = {'text': 'Cool post !!!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
