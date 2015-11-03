#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Menu(models.Model):
    """
    菜单
    
    目前默认一家餐厅只有一个菜单
    后期一家餐厅可以配置多个菜单，并可以设置菜单的有效时间范围
    """
    restaurant = models.ForeignKey('restaurant.Restaurant',
                                   related_name="menus", blank=True, null=True)
    name = models.CharField(max_length=255, blank=False, null=False,
                            default=u"默认菜单")
    

class Category(models.Model):
    """
    菜单分类
    """
    menu = models.ForeignKey('menu.Menu', related_name="categories",
                             null=True)
    name = models.CharField(max_length=255, blank=False, null=False,
                            default=u"默认分类")


class Product(models.Model):
    """
    商品
    """
    category = models.ForeignKey('menu.Category', related_name="products",
                                 null=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    img_key = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=255, blank=True, null=True,
                            default=u"份")
    description = models.CharField(max_length=2000, blank=True, null=True)

