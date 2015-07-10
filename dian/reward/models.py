#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Reward(models.Model):
    """
    奖品
    """
    REWARD_TYPE = (
        (0, "discount"),      # 折扣
        (1, "gift"),          # 礼物
    )

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
        (0, "排队"),            # 排队超时
        (1, "游戏"),            # 游戏
        (2, "图片分享")         # 图片分享
    )
    OPERATOR_TYPE = (
        (0, "greater"),         # 大于
    )
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", related_name="strategies", null=True, blank=True)
    reward = models.ForeignKey(Reward, related_name="strategies", null=False)

    type = models.IntegerField(choices=STRATEGY_TYPE, default=STRATEGY_TYPE[0][0], null=False)
    operator = models.IntegerField(choices=OPERATOR_TYPE, default=OPERATOR_TYPE[0][0], null=False)
    # 条件-数量
    count = models.IntegerField(null=False)


