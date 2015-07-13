# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from post.models import Tag, Image, Post


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'create_time', 'member', 'tags', 'images', 'likes')
        depth = 1
