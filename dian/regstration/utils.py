#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.db.models import Min

from .models import Regstration


def get_next_regstration(table_type):
    """
    获取某一类型table type的一个号
    如果无号，则返回None
    return Regstration
    """
    if table_type.regstrations.count() == 0:
        return None

    remain_regstration = table_type.regstrations.filter(table=None, expire=False)
    if not remain_regstration:
        return None

    return Regstration.objects.get(
        queue_number=remain_regstration.aggregate(Min('queue_number'))['queue_number__min'],
    )


