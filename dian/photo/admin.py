#! -*- encoding:utf-8 -*-

from django.contrib import admin

from photo.models import Photo, Tag


admin.site.register(Photo)
admin.site.register(Tag)

