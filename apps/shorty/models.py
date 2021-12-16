from django.db import models
from django.core.cache import cache
from django.contrib.sessions.models import Session

from .utils import get_link


class Shorty(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, db_column='session_key')
    link = models.CharField(max_length=10, null=False, blank=False, unique=True)
    url = models.URLField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subpart} - {self.url}'

    def save(self, *args, **kwargs):
        create = not self.pk
        if create:
            self.link = get_link()
        super().save(*args, *kwargs)
        if create:
            cache.set(self.link, self.url)
