from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
import hashlib
from functools import wraps
from dian.settings import MD5_SEED


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


def restaurant_required(func):
    @wraps(func)
    def decorated_view(request, *args, **kwargs):
        if not request.current_restaurant:
            return Response("No restaurant found", status=status.HTTP_400_BAD_REQUEST)
        if request.current_restaurant.owner != request.user:
            return Response("No authority to access this restaurant", status=status.HTTP_403_FORBIDDEN)

        return func(request, *args, **kwargs)

    return decorated_view


