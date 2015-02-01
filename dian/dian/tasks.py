# -*- encoding:utf-8 -*-
import random
import requests

from celery import task
from django.conf import settings
from django.core.cache import cache

from account.models import MsgStatistics

MSG_SEND_API = "http://sms.1xinxi.cn/asmx/smsservice.aspx"
CAPTCHA_TEMPLATE = "尊敬的用户，您在点快系统上获取了验证码:%(captcha)s"
REGISTRATION_TEMPLATE = {
    "one_left": "尊敬的用户，您前面还有1人排队，请提前做好准备",
    "next": "尊敬的用户，下一位到您就餐，请提前做好准备"
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
    send_msg.delay(user, msg, user.username, MsgStatistics.MSG_TYPE[1][0])


def send_registration_remind(registration, msg_type):
    msg = REGISTRATION_TEMPLATE[msg_type]
    send_msg.delay(registration.table_type.restaurant.owner,
                   msg,
                   registration.phone,
                   MsgStatistics.MSG_TYPE[0][0])
