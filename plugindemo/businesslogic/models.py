from django.db import models
from .plugin import EndpointProvider

actions = EndpointProvider.get_plugins()
HANDLER_CHOICES = [(a.title, a.description) for a in actions]


class Endpoint(models.Model):
    path = models.CharField(db_index=True, max_length=256)
    handler = models.CharField(max_length=64, choices=HANDLER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.path)
