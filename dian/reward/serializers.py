#! -*- encoding: utf-8 -*-


from rest_framework.serializers import ModelSerializer, SerializerMethodField

from reward.models import Strategy, Reward, Coupon


class RewardSerializer(ModelSerializer):

    class Meta:
        model = Reward


class StrategyGetSerializer(ModelSerializer):
    reward = RewardSerializer()
    condition = SerializerMethodField('get_condition')

    class Meta:
        model = Strategy

    def get_condition(self, obj):
        return Strategy.STRATEGY_TYPE[obj.type][1] + " " + Strategy.OPERATOR_TYPE[obj.operator][1] + " " + str(obj.count)


class StrategySerializer(ModelSerializer):

    class Meta:
        model = Strategy


class CouponSerializer(ModelSerializer):

    class Meta:
        model = Coupon