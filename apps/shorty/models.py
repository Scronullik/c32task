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
        return f'{self.subpart} - {self.url}'

    def clean(self):
        if self.link == 'admin':
            raise ValidationError(message='Shorty with this Link already exists.', code='invalid', params={
                'value': self.link})
        super().clean()

    def save(self, *args, **kwargs):
        """
        К сожалёнию, плагин django-redis не реализует комманду редиса RENAME.
        Поэтому после изменения ссылки необходимо удалить старую ссылку из кэша,
        а затем добавить в кэш новую. В функции реализуются все работы по сохранению ссылок в кэше Redis.
        """
        created = self.pk is None
        super().save(*args, *kwargs)
        operation = 'created' if created else 'updated'
        logging.info(f'link: {self.link} - url: {self.url} was {operation}.')

        if not created and hasattr(self, '_old_values'):  # после изменения модели
            old_link = self._old_values['link']
            if self.link != old_link and cache.has_key(old_link):  # проверяем изменилась ли старая ссылка
                cache.delete(old_link)  # удаляем её
                logging.info(f'Old link {old_link} was deleted from Redis.')

        if not cache.has_key(self.link):  # проверяем существует ли ссылка в кэша
            cache.set(self.link, self.url)  # если нет, то сохраняем ссылки и юрлы в кэше
            logging.info(f'key [link: {self.link} - value [url: {self.url}] was cached in Redis.')

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._old_values = dict(zip(field_names, values))  # сохраним старые значения
        return instance
