#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.db import models


class Cart(models.Model):
    """
    购物车
    每个顾客访问每家餐厅，都会有一个对应的购物车实体
    """
    restaurant = models.ForeignKey("restaurant.Restaurant",\
            related_name="carts", null=True)
    member = models.ForeignKey("account.Member", related_name="carts",\
            null=True)
    # items = models.ManyToManyField("menu.Product", through="CartItem")


class CartItem(models.Model):
    """
    购物车item
    多对多关系实体
    """
    cart = models.ForeignKey("trade.Cart", related_name="cart_items", null=True)
    product = models.ForeignKey("menu.Product")
    count = models.IntegerField(default=0)


class Order(models.Model):
    """
    订单
    """

    STATUS = (
        (0, "placed"), # 已下单（或者追加菜后），待确认
        (1, "confirmed"), # 餐厅确认通过后，待付款
        (2, "paid"), # 已付款
    )

    restaurant = models.ForeignKey('restaurant.Restaurant',\
            related_name="orders", null=True)
    member = models.ForeignKey('account.Member', related_name="orders",\
            null=True)
    create_time = models.DateTimeField(default=datetime.datetime.now())
    price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    status = models.IntegerField(choices=STATUS, default=STATUS[0][0])


class OrderItem(models.Model):
    """
    订单项
    """

    order = models.ForeignKey('trade.Order', related_name="order_items",\
            null=True)

    # 商品分类
    category = models.CharField(max_length=255, blank=False, null=False,\
            default=u"默认分类")

    # 商品信息
    name = models.CharField(max_length=255, blank=False, null=False)
    img_key = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    unit = models.CharField(max_length=255, blank=True, null=True,\
            default=u"份")
    description = models.CharField(max_length=2000, blank=True, null=True)

    # CartItem的信息
    count = models.IntegerField(default=0)

