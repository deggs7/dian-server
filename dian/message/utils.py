# -*- encoding:utf-8 -*-

import random
import requests
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from django.core.cache import cache

from registration.models import Registration
from restaurant.models import Restaurant

# from message.models import MsgStatistics

from dian.settings import SMS_API_URL
from dian.settings import SMS_API_NAME
from dian.settings import SMS_API_PWD
from dian.settings import SMS_API_TYPE


# 取号时短信通知
def render_join(restaurant_name, queue_name, queue_number, to_wait):
    tpl = u"%(restaurant_name)s提醒您：您已取得%(queue_name)s%(queue_number)d号，您前面还有%(to_wait)d桌在等候。请注意叫号，以免过号。本信息仅供参考，以迎宾叫号为准。【点快】"
    content = tpl % {
        "restaurant_name": restaurant_name,
        "queue_name": queue_name,
        "queue_number": queue_number,
        "to_wait": to_wait
    }
    return content


def render_ready(restaurant_name, queue_name, current_number):
    tpl = u"%(restaurant)s提醒您：当前%(table_name)s已叫号至%(current_number)d号，您前面还有1桌。请注意叫号，以免过号。本信息仅供参考，以迎宾叫号为准。【点快】"
    content = tpl % {
        "restaurant": self.reg.restaurant.name,
        "table_name": self.reg.table_type.name,
        "current_number": self.reg.get_current_number()
    }
    return content


def render_reward(restaurant_name, time_wait, reward_type, reward_info):
    tpl = u"%(restaurant)s提醒您，您已等位超过了%(time_wait)d分钟，为表示本店的歉意，您本次就餐将获得%(reward_info)s，祝您用餐愉快！【点快】"

    # 如果strategy是折扣奖励，需优化文案
    if (reward_type == 'discount'):
        try:
            # reward_info = "%s折优惠" % str(reward_info / 10)
            reward_info = u"%s%s" % (str("%.1f" % (int(reward_info)/10)), u"折优惠")
        except Exception, e:
            pass
    content = tpl % {
        "restaurant": self.reg.restaurant.name,
        "time_wait": self.kwargs['strategy'].time_wait,
        "reward_info": reward_info
    }
    return content


def create_and_send_captcha(user):
    tpl = u"【点快】\
            %(captcha)s（点快验证码，5分钟内有效），您正在执行重置密码操作。"
    captcha_tmp = random.randint(1000, 999999)
    captcha = "%06d" % captcha_tmp

    key = 'captcha_refound_pw_%s' % user.username
    cache.set(key, captcha, 300)
    print cache.get(key)

    msg = tpl % {"captcha": captcha}
    print msg.encode('utf-8')
    if not settings.DEBUG:
        send_msg.delay(user, msg, user.username, 'MsgStatistics.MSG_TYPE[1][0]')


def send_registration_remind(registration, msg_type,\
msg_statistics_type='MsgStatistics.MSG_TYPE[0][0]', **kwargs):
    """
    发送用户取号的提示短信，以及提示用户到号的短信
    msg_type 可选"one_left", "next", "getting"
    """
    msg_obj = REGISTRATION_TEMPLATE[msg_type](registration, **kwargs)
    msg = msg_obj.render()
    print msg.encode('utf-8')
    if not settings.DEBUG:
        send_msg.delay(registration.table_type.restaurant.owner,
                       msg,
                       registration.phone,
                       msg_statistics_type)


# for period tasks
@periodic_task(run_every=crontab(minute="*/1"))
def registration_time_out_strategy():
    # 对于每一个restaurant，取其设置的strategy
    for restaurant in Restaurant.objects.all():
        # 对于其中的每一个strategy，搜索满足其策略的registration
        for strategy in restaurant.strategies.all():
            anchor_time = datetime.datetime.now() - datetime.timedelta(minutes=strategy.time_wait)
            regs = Registration.objects.filter(status__exact=Registration.STATUS[0][0],
                                               create_time__lt=anchor_time)
            # 获取还没有完成该策略的registration
            regs_post = []
            for reg in regs:
                strategy_ids = [strategy_dup.strategy_id for strategy_dup in reg.strategies.all()]
                if strategy.id not in strategy_ids:
                    regs_post.append(reg)

            # 对于满足策略条件的registration，应用该策略
            for reg in regs_post:
                if not settings.DEBUG:
                    send_registration_remind(reg, 'reward',\
                            'MsgStatistics.MSG_TYPE[2][0]', strategy=strategy)
                # strategy_dup = StrategyDup(strategy_id=strategy.id,
                #                            time_wait=strategy.time_wait,
                #                            reward_type=strategy.reward_type,
                #                            reward_info=strategy.reward_info,
                #                            registration=reg)
                # strategy_dup.save()



# REGISTRATION_TEMPLATE = {
#     "one_left": OneLeftMsg,
#     "next": NextMsg,
#     "getting": GettingMsg,
#     "reward": RewardMsg,
# }


# class NextMsg(RegistrationMsg):
#     MSG_TEMPLATE = u"%(restaurant)s提醒您：下一位到您就餐，请提前做好准备，祝您就餐愉快。本信息仅供参考，以迎宾叫号为准。【点快-自助取号】"
#     content = MSG_TEMPLATE % {
#         "restaurant": self.reg.restaurant.name
#     }


