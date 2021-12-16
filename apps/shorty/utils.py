import string
import random

from django.core.cache import cache


def get_link():
    while True:
        link = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
        if cache.get(link) is None:
            break
    return link
