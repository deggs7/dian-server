# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from photo.models import Photo, Tag


class PhotoSerializer(ModelSerializer):

    class Meta:
        model = Photo


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag

