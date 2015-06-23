#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer
from menu.models import Menu
from menu.models import Category
from menu.models import Product


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product


class CategoryDetailSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products')


class MenuSerializer(ModelSerializer):

    class Meta:
        model = Menu


class MenuDetailSerializer(ModelSerializer):
    categories = CategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'categories')



