# -*- encoding:utf-8 -*-
import random
import requests

from celery import task
from django.conf import settings
from django.core.cache import cache

from account.models import MsgStatistics

MSG_SEND_API = "http://sms.1xinxi.cn/asmx/smsservice.aspx"
CAPTCHA_TEMPLATE = u"【点快-自助取号】%(captcha)s（点快验证码，5分钟内有效），您正在执行重置密码操作。"


class RegistrationMsg(object):

    def __init__(self, reg):
        self.reg = reg

    def render(self):
        raise Exception("Child class must be implemented")


class OneLeftMsg(RegistrationMsg):
    MSG_TEMPLATE = \
        u"%(restaurant)s提醒您：当前%(table_name)s已叫号至%(current_number)d号，您前面还有1桌。请注意叫号，以免过号。本信息仅供参考，以迎宾叫号为准。【点快-自助取号】"

    def render(self):
        return self.MSG_TEMPLATE % {
            "restaurant": self.reg.restaurant.name,
            "table_name": self.reg.table_type.name,
            "current_number": self.reg.get_current_number()
        }


class NextMsg(RegistrationMsg):
    MSG_TEMPLATE = u"%(restaurant)s提醒您：下一位到您就餐，请提前做好准备，祝您就餐愉快。本信息仅供参考，以迎宾叫号为准。【点快-自助取号】"

    def render(self):
        return self.MSG_TEMPLATE % {
            "restaurant": self.reg.restaurant.name
        }


class GettingMsg(RegistrationMsg):
    MSG_TEMPLATE = \
        u"%(restaurant)s提醒您：您已取得%(queue_number)d号，您前面还有%(registration_left)d桌在等候。请注意叫号，以免过号。本信息仅供参考，以迎宾叫号为准。【点快-自助取号】"

    def render(self):
        return self.MSG_TEMPLATE % {
            "restaurant": self.reg.restaurant.name,
            "queue_number": self.reg.queue_number,
            "registration_left": self.reg.get_registration_left() - 1
        }

REGISTRATION_TEMPLATE = {
    "one_left": OneLeftMsg,
    "next": NextMsg,
    "getting": GettingMsg
}


@task
def send_msg(user, msg, phone, type):
    data = {
        "name": settings.MSG_ACCOUNT,
        "pwd": settings.MSG_PASSWORD,
        "mobile": phone,
        "type": "pt",
        "content": msg,
    }
    r = requests.post(MSG_SEND_API, data)
    # 记录短信相关信息
    statistics, created = MsgStatistics.objects.get_or_create(owner=user,
                                                              type=type)
    if r.status_code == 200:
        ret = r.text.split(',')
        if ret[0] == "0":
            print 'msg send ok: %s' % msg
            statistics.success += 1
            statistics.save()
            return

    print 'msg send error(status=%d): %s' % (r.status_code, msg)
    statistics.fail += 1
    statistics.save()


def create_and_send_captcha(user):
    captcha_tmp = random.randint(1000, 999999)
    captcha = "%06d" % captcha_tmp

    cache.set(user.username, captcha, 300)
    print cache.get(user.username)

    msg = CAPTCHA_TEMPLATE % {"captcha": captcha}
    print msg.encode('utf-8')
    if not settings.DEBUG:
        send_msg.delay(user, msg, user.username, MsgStatistics.MSG_TYPE[1][0])


def send_registration_remind(registration, msg_type):
    """
    发送用户取号的提示短信，以及提示用户到号的短信
    msg_type 可选"one_left", "next", "getting"
    """
    msg_obj = REGISTRATION_TEMPLATE[msg_type](registration)
    msg = msg_obj.render()
    print msg.encode('utf-8')
    if not settings.DEBUG:
        send_msg.delay(registration.table_type.restaurant.owner,
                       msg,
                       registration.phone,
                       MsgStatistics.MSG_TYPE[0][0])
