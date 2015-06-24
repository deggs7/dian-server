#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem


class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem


class CartSerializer(ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'restaurant', 'member', 'cart_items')


class OrderSerializer(ModelSerializer):
    restaurant_name = SerializerMethodField('get_restaurant_name')

    class Meta:
        model = Order
        fields = ('id', 'restaurant', 'restaurant_name', 'create_time',
                  'price', 'status', 'confirm_time', 'pay_time')

    def get_restaurant_name(self, obj):
        return obj.restaurant.name


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem


class OrderDetailSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'restaurant', 'member', 'create_time', 'confirm_time', 'pay_time',
                  'status', 'price', 'order_items')
