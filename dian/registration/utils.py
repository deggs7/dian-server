#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.db.models import Min

from .models import Regstration


def get_next_registration(table_type):
    """
    获取某一类型table type的一个号
    如果无号，则返回None
    return Regstration
    """
    if table_type.registrations.count() == 0:
        return None

    remain_registration = table_type.registrations.filter(table=None, expire=False)
    if not remain_registration:
        return None

    return Regstration.objects.get(
        queue_number=remain_registration.aggregate(Min('queue_number'))['queue_number__min'],
        table_type=table_type,
    )


