import logging

from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.sessions.models import Session

from .utils import get_link


class Shorty(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, db_column='session_key')
    link = models.CharField(default=get_link, max_length=10, null=False, blank=False, unique=True,
                            validators=[MinLengthValidator(5),
                                        RegexValidator('^[A-Za-z0-9]+$', message='Link must be letters and numbers.')])
    url = models.URLField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.link} - {self.url}'

    def clean(self):
        if self.link == 'admin':
            raise ValidationError(message='Shorty with this Link already exists.', code='invalid', params={
                'value': self.link})
        super().clean()

    def save(self, *args, **kwargs):
        """
        This function implements all the work on saving links in the Redis cache.
        """
        created = self.pk is None
        super().save(*args, **kwargs)
        operation = 'created' if created else 'updated'
        logging.info(f'link: {self.link} - url: {self.url} was {operation}.')

        if not created and hasattr(self, '_old_values'):  # after changed the model
            old_link = self._old_values['link']
            if self.link != old_link and cache.has_key(old_link):  # check if the old link has changed
                cache.delete(old_link)  # delete it
                logging.info(f'key [link: {old_link}] was deleted from cache of Redis.')

        if not cache.has_key(self.link):  # check if the link exists in the cache
            cache.set(self.link, self.url)  # if not, then saving links and urls in the cache
            logging.info(f'key [link: {self.link} - value [url: {self.url}] was cached in Redis.')

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._old_values = dict(zip(field_names, values))  # saving old values
        return instance
