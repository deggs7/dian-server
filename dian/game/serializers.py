#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from game.models import Game


class GameSerializer(ModelSerializer):
    score = SerializerMethodField(method_name="get_score")

    class Meta:
        model = Game
        fields = ("name", "description", "url", "ratio", "logo_file_key",\
                "score")

    def get_score(self, obj):
        return obj.score
