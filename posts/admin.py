# -*- coding: utf-8 -*-
from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Post


TokenAdmin.raw_id_fields = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_thumbnail', 'like', 'created_at', 'updated_at')
    readonly_fields = ('slug', 'like')
    list_display_links = ('title', 'admin_thumbnail')
