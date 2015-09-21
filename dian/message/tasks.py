# -*- encoding:utf-8 -*-

import requests
from celery import task

from dian.settings import SMS_API_URL
from dian.settings import SMS_API_NAME
from dian.settings import SMS_API_PWD
from dian.settings import SMS_API_TYPE

from dian.settings import DEBUG


from celery.utils.log import get_task_logger
logger = get_task_logger('dian')

@task
def send_sms(phone, content):
    logger.info(phone)
    logger.info(content)
    options = {
        'name': SMS_API_NAME,
        'pwd': SMS_API_PWD,
        'mobile': phone,
        'type': SMS_API_TYPE,
        'content': content,
    }
    
    if DEBUG:
        logger.debug(options)
        return

    res = requests.post(SMS_API_URL, options)
    if res.status_code == 200:
        rt = res.text.split(',')
        if rt[0] == "0":
            logger.info('OK')
            return

    # 发送不正常
    logger.error(options)
    logger.error(res)
    return
