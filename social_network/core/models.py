# -*- coding: utf-8 -*-
import os
import re
import uuid
import shutil
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FileDescriptor, ImageFileDescriptor
from imagekit.models import ImageSpecField
from django.utils.translation import ugettext_lazy as _


def validate_image(instance):
    if instance is not None:
        extension_list = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
        size = int(instance.size)
        extension = instance.name.split('.')[-1]

        if not [ext for ext in extension_list if extension == ext]:
            raise ValidationError(_('Only JPG, PNG or GIF files.'))
        elif not size:
            raise ValidationError(_('Image can not be 0 MB.'))
        elif not size or size > 524288:
            raise ValidationError(_('The image size exceeds the limit of 0.5 MB.'))


def make_upload_path(instance, filename):
    """
    Create path for image.
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split('.')[-1]
    return os.path.join(instance.upload_dir, u'{0}.{1}'.format(uuid.uuid4(), extension))


def cleaning_files_pre_save(sender, instance, **kwargs):
    """
    Remove old files
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    old_status = sender.objects.filter(pk=instance.pk)
    dir_name_list = dir(sender)

    if old_status:
        for dir_name in dir_name_list:
            field = getattr(sender, dir_name, None)

            if field and (isinstance(field, FileDescriptor) or
               isinstance(field, ImageFileDescriptor) or
               isinstance(field, ImageSpecField)):

                old_field = getattr(old_status[0], dir_name)
                updated_field = getattr(instance, dir_name)

                if getattr(old_field, 'name', None) != getattr(updated_field, 'name', None):

                    try:
                        path = getattr(old_field, 'path')

                        if path and os.path.exists(path):
                            if isinstance(field, ImageSpecField):
                                pattern = re.compile(r'(/[-_\w\(\)]+\.[a-zA-Z]{3,4}$)')
                                shutil.rmtree(pattern.sub('', path))
                            else:
                                os.remove(path)
                    except (FileNotFoundError, ValueError):
                        pass


def cleaning_files_pre_delete(sender, instance, **kwargs):
    """
    Delete orphan files
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    dir_name_list = dir(sender)

    for dir_name in dir_name_list:
        field = getattr(sender, dir_name, None)

        if field and (isinstance(field, FileDescriptor) or
           isinstance(field, ImageFileDescriptor) or
           isinstance(field, ImageSpecField)):

            target_field = getattr(instance, dir_name)

            try:
                path = getattr(target_field, 'path', None)

                if path and os.path.exists(path):
                    if isinstance(field, ImageSpecField):
                        pattern = re.compile(r'(/[-_\w\(\)]+\.[a-zA-Z]{3,4}$)')
                        shutil.rmtree(pattern.sub('', path))
                    else:
                        os.remove(path)
            except (FileNotFoundError, ValueError):
                pass
