# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from post.models import Tag, Like, Image, Post


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag


class LikeSerializer(ModelSerializer):

    class Meta:
        model = Like


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'create_time', 'member', 'tags', 'images')
        depth = 1
