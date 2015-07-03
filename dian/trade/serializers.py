#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from trade.models import Cart


class CartSerializer(ModelSerializer):

    class Meta:
        model = Cart


