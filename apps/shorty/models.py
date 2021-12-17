import logging

from django.db import models
from django.core.cache import cache
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.sessions.models import Session

from .utils import get_link


class Shorty(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, db_column='session_key')
    link = models.CharField(max_length=10, null=False, blank=False, unique=True,
                            validators=[MinLengthValidator(5),
                                        RegexValidator('^[A-Za-z0-9]+$', message='Link must be letters and numbers.')])
    url = models.URLField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subpart} - {self.url}'

    def save(self, *args, **kwargs):

        created = self.pk is None
        if created:
            self.link = get_link()
        super().save(*args, *kwargs)

        operation = 'created' if created else 'updated'
        logging.info(f'{self.link} - url: {self.url}: link was {operation}.')

        if created:
            cache.set(self.link, self.url)
            logging.info(f'{self.link} - url: {self.url}: was cached in Redis.')
        elif hasattr(self, '_old_values'):
            old_link = self._old_values['link']
            if self.link != old_link and cache.has_key(old_link):
                cache.delete(old_link)
                cache.set(self.link, self.url)
                logging.info(f'Old link {old_link} was deleted from Redis.')
                logging.info(f'New link {self.link} with url [{self.url}] was cached in Redis.')

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._old_values = dict(zip(field_names, values))
        return instance
