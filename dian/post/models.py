# -*- coding: utf-8 -*-

from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file_key = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("post.Post", related_name="images")


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField("Tag Type", default=1)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('post.Post', related_name="tags")


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('account.Member', related_name="member")
    post = models.ForeignKey('post.Post', related_name="likes")
    create_time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey('account.Member', related_name="posts")
