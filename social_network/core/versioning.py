# -*- coding: utf-8 -*-
from rest_framework.versioning import URLPathVersioning


class PostVersioning(URLPathVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'
