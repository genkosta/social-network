# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from slugify import slugify
from django.urls import reverse


class Post(models.Model):
    """
    Managing posts of users
    """

    user = models.ForeignKey(User,
                             verbose_name='User',
                             related_name='posts',
                             on_delete=models.CASCADE)

    title = models.CharField(verbose_name='Title',
                             max_length=50,
                             default='',
                             help_text='Title post.')

    message = models.TextField(verbose_name='Message',
                               max_length=1500,
                               help_text='Your new message.')

    like = models.IntegerField(verbose_name='Like', default=0)

    slug = models.SlugField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='Publication date', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated', auto_now=True)

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('posts:view-post', kwargs={'slug': self.slug})


# Signals
def post_add_slug(instance, **kwargs):
    new_slug = '{0}-{1}'.format(instance.pk, slugify(instance.title))
    if instance.slug != new_slug:
        instance.slug = new_slug
        instance.save()


models.signals.post_save.connect(post_add_slug,  sender=Post)
