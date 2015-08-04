#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import qrcode
import qiniu
import os
import datetime
import hashlib

from django.core.cache import cache

from dian.settings import MD5_SEED
from dian.settings import APP_ID, APP_SECRET
from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import TEMP_DIR
from dian.settings import DEBUG


def is_verified(captcha, phone):
    cached_captcha = cache.get(phone, None)
    if not cached_captcha or captcha != cached_captcha:
        return False
    return True


def get_md5(s):
    if s:
        m = hashlib.md5(s)
        m.update(MD5_SEED)
        return m.hexdigest()
    else:
        return None


def generate_qr_code(url):
    """
    根据链接生成二维码，并返回二维码文件临时路径
    二维码上传后，应删除返回的临时文件，比如: os.remove(path)
    ref: https://pypi.python.org/pypi/qrcode
    """

    file_key = get_md5("%s%s" % (url,\
        datetime.datetime.now()))
    path = "%s%s" % (TEMP_DIR, file_key)

    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
            )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(path)

    return path


def upload_to_qiniu(localfile, clean_localfile=True):
    """
    上传一个本地文件到七牛，返回文件的file_key，同时默认删除本地文件
    ref: http://developer.qiniu.com/docs/v6/sdk/python-sdk.html#upload-do
    """

    auth = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    file_key = get_md5("%s%s" % ("web_auth-%d" % 1,\
        datetime.datetime.now()))
    uptoken = auth.upload_token(bucket=QINIU_BUCKET_PUBLIC)

    mime_type = "text/plain"    # 二进制流 "application/octet-stream"
    ret, info = qiniu.put_file(uptoken, file_key, localfile, mime_type=mime_type)

    if ret is not None:
        if clean_localfile:
            # 默认上传成功会删除本地文件
            os.remove(localfile)
        return file_key
    else:
        # print(info) # error message in info
        return None

