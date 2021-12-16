import string
import random

from django.core.cache import cache


def get_subpart():
    while True:
        subpart = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
        if cache.get(subpart) is None:
            break
    return subpart
