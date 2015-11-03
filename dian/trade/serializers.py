#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem
from menu.serializers import ProductSerializer


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem


class CartSerializer(ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart


class CartDetailSerializer(ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    restaurant_name = SerializerMethodField('get_restaurant_name')
    table_name = SerializerMethodField('get_table_name')

    class Meta:
        model = Cart

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

    def get_table_name(self, obj):
        return obj.table.name


class OrderSerializer(ModelSerializer):
    restaurant_name = SerializerMethodField('get_restaurant_name')

    class Meta:
        model = Order
        # fields = ('id', 'restaurant', 'restaurant_name', 'create_time',
        #           'price', 'status', 'confirm_time', 'pay_time', 'table_name')

    def get_restaurant_name(self, obj):
        return obj.restaurant.name


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem


class OrderDetailSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    restaurant_name = SerializerMethodField('get_restaurant_name')

    class Meta:
        model = Order
        # fields = ('id', 'restaurant', 'restaurant_name', 'member',
        #           'create_time', 'confirm_time',  'pay_time', 'table_name',
        #           'status', 'price', 'order_items')

    def get_restaurant_name(self, obj):
        return obj.restaurant.name
