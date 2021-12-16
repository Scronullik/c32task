from django.db import models
from django.contrib.sessions.models import Session


class Shorty(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, db_column='session_key')
    subpart = models.CharField(max_length=10, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subpart} - {self.url}'
