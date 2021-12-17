import string
import random

from django.core.cache import cache


def get_link(k=10):
    while True:
        link = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=k))
        if not cache.has_key(link):
            break
    return link
