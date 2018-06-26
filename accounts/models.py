# -*- coding: utf-8 -*-
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from django.utils.safestring import mark_safe

from django.db.models.signals import post_save, pre_save, pre_delete

from social_network.core.models import (cleaning_files_pre_save, cleaning_files_pre_delete,
                                        validate_image, make_upload_path)

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(verbose_name='Image',
                              validators=[validate_image],
                              upload_to=make_upload_path,
                              blank=True,
                              null=True)

    created_at = models.DateTimeField(verbose_name='Publication date', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name='Updated', auto_now=True, null=True)

    thumbnail = ImageSpecField([ResizeToFit(height=60, width=60, upscale=True)], source='image')
    middle = ImageSpecField([ResizeToFit(height=180, width=180, upscale=True)], source='image')

    def __str__(self):
        return self.user.username

    @property
    def upload_dir(self):
        return 'profile/images'

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def admin_thumbnail(self):
        if self.image:
            return mark_safe('<img src="{}" />'.format(self.thumbnail.url))
        else:
            return ''
    admin_thumbnail.short_description = 'Image'
    admin_thumbnail.allow_tags = True

    @property
    def username(self):
        return self.user.username


# Signals
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Create Profile
post_save.connect(create_user_profile, sender=User)
# Cleaning files
pre_save.connect(cleaning_files_pre_save, sender=Profile)
pre_delete.connect(cleaning_files_pre_delete, sender=Profile)
