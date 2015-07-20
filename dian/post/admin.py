#! -*- encoding:utf-8 -*-

from django.contrib import admin

from post.models import Image, Tag, Post


admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Post)
