#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import qrcode


def generate_qr_code(url):
    """
    将一个链接，生成为一个二维码
    """
    img = qrcode.make(url)
    img.save('/Users/david/Desktop/test.png')


def store_qr_code(url)
    """
    存储二维码
    并返回二维码文件的key
    """
    pass
