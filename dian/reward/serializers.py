#! -*- encoding: utf-8 -*-


from rest_framework.serializers import ModelSerializer

from reward.models import Strategy, Reward


class RewardSerializer(ModelSerializer):

    class Meta:
        model = Reward


class StrategyGetSerializer(ModelSerializer):
    reward = RewardSerializer()

    class Meta:
        model = Strategy


class StrategySerializer(ModelSerializer):

    class Meta:
        model = Strategy
