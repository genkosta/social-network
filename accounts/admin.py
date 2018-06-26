# -*- coding: utf-8 -*-
from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Profile


TokenAdmin.raw_id_fields = ('user',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'admin_thumbnail', 'created_at', 'updated_at')
    list_display_links = ('username', 'admin_thumbnail',)
    raw_id_fields = ('user',)
