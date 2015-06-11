#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem


class CartSerializer(ModelSerializer):

    class Meta:
        model = Cart


class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem


