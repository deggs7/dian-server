#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.db import models


REWARD_TYPE = (
    (0, "discount"),      # 折扣
    (1, "gift"),          # 礼物
)


class Reward(models.Model):
    """
    奖品
    """
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", related_name="rewards", null=True, blank=True)
    type = models.IntegerField(choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    # 如果type是0，则输入百分比
    # 如果type是1，则输入礼物名称
    content = models.CharField(max_length=512, blank=False, null=False)


class Strategy(models.Model):
    """
    奖励策略
    """
    STRATEGY_TYPE = (
        (0, "排队时间"),            # 排队超时
        (1, "游戏得分"),            # 游戏
        (2, "图片分享（点赞次数）")   # 图片分享
    )
    OPERATOR_TYPE = (
        (0, ">"),         # 大于
    )
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", related_name="strategies", null=True, blank=True)
    reward = models.ForeignKey(Reward, related_name="strategies", null=False)

    type = models.IntegerField(choices=STRATEGY_TYPE, default=STRATEGY_TYPE[0][0], null=False)
    operator = models.IntegerField(choices=OPERATOR_TYPE, default=OPERATOR_TYPE[0][0], null=False)
    # 条件-数量
    count = models.IntegerField(null=False)


class Coupon(models.Model):
    """
    优惠券
    """
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey("account.Member", related_name="coupons", null=False)
    restaurant = models.ForeignKey("restaurant.Restaurant", related_name="coupons", null=False)
    reward_type = models.IntegerField(choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    reward_content = models.CharField(max_length=512, blank=False, null=False)
    strategy_condition = models.CharField(max_length=512, blank=False, null=False)
    create_time = models.DateTimeField(default=datetime.datetime.now())
    invalid_time = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=512, null=True, blank=True)
    is_used = models.BooleanField(default=False)

