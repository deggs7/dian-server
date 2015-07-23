# -*- coding: utf-8 -*-

from django.db import models


TAG_TYPE_RESTAURANT = 0
TAG_TYPE_ACTIVITY = 1

TAG_TYPE = (
    (TAG_TYPE_RESTAURANT, "restaurant"),      # 餐厅标签
    (TAG_TYPE_ACTIVITY, "activity"),        # 活动标签
)

class Photo(models.Model):
    file_key = models.CharField(max_length=255)
    member = models.ForeignKey('account.Member', related_name="photos")
    likes = models.ManyToManyField('account.Member',\
            related_name='like_photos', null=True)
    tag = models.ForeignKey('photo.Tag', related_name='photos')
    create_time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=TAG_TYPE, default=TAG_TYPE[0][0])
    restaurant = models.ForeignKey('restaurant.Restaurant',
                                   related_name='tags', null=True, blank=True)

