# -*- coding: utf-8 -*-

from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file_key = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    pass


class Post(models.Model):
    pass
