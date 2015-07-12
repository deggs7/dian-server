#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Game(models.Model):
    """
    游戏

    TODO: resturant - many to many
    """

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    url = models.CharField(max_length=255, blank=False, null=False)
    ratio = models.DecimalField(default=1, max_digits=8, decimal_places=2)
    logo_file_key = models.CharField(max_length=255, blank=True, null=True)

