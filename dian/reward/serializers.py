#! -*- encoding: utf-8 -*-


from rest_framework.serializers import ModelSerializer, SerializerMethodField

from reward.models import Strategy, Reward


class RewardSerializer(ModelSerializer):

    class Meta:
        model = Reward


class StrategySerializer(ModelSerializer):
    reward = RewardSerializer()

    class Meta:
        model = Strategy
