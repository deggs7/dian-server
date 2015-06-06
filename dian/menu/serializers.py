#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from menu.models import Menu
from menu.models import Category
from menu.models import Product


class MenuSerializer(ModelSerializer):

    class Meta:
        model = Menu


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product

