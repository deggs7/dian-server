from django.core.cache import cache
import hashlib
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
