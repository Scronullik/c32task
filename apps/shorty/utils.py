import string
import random

from django.core.cache import cache


def get_link(k=10):
    while True:
        link = ''.join(random.choices(string.letters + string.digits, k=k))
        if cache.get(link) is None:
            break
    return link
