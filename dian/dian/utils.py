from django.core.cache import cache


def is_verified(captcha, phone):
    cached_captcha = cache.get(phone, None)
    if not cached_captcha or captcha != cached_captcha:
        return False
    return True

