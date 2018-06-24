# -*- coding: utf-8 -*-

from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill
from django.utils.safestring import mark_safe

from django.db.models.signals import post_save, pre_save, pre_delete
from social_network.core.utils import (cleaning_files_pre_save, cleaning_files_pre_delete,
                                       validate_image, make_upload_path)

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

    image = models.ImageField(verbose_name='Image',
                              validators=[validate_image],
                              upload_to=make_upload_path,
                              blank=True,
                              null=True)

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

    thumbnail = ImageSpecField([ResizeToFit(height=60, width=60, upscale=True)], source='image')
    middle = ImageSpecField([ResizeToFit(height=180, width=180, upscale=True)], source='image')

    @property
    def upload_dir(self):
        return 'posts/images'

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def admin_thumbnail(self):
        if self.image:
            return mark_safe('<img src="{}" />'.format(self.thumbnail.url))
        else:
            return ''
    admin_thumbnail.short_description = 'Image'
    admin_thumbnail.allow_tags = True

    def get_absolute_url(self):
        return reverse('posts:view-post', kwargs={'slug': self.slug})


# Signals
def post_add_slug(instance, **kwargs):
    new_slug = '{0}-{1}'.format(instance.pk, slugify(instance.title))
    if instance.slug != new_slug:
        instance.slug = new_slug
        instance.save()


post_save.connect(post_add_slug,  sender=Post)
pre_save.connect(cleaning_files_pre_save, sender=Post)
pre_delete.connect(cleaning_files_pre_delete, sender=Post)