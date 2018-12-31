from django.db import models
from .endpoint import EndpointProvider

endpoints = EndpointProvider.get_plugins()
ENDPOINT_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in endpoints]


class Endpoint(models.Model):
    path = models.CharField(db_index=True, max_length=256)
    handler = models.CharField(max_length=64, choices=ENDPOINT_HANDLER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.path)


class Datalogger(models.Model):
    devid = models.CharField(db_index=True, unique=True, max_length=256)
    name = models.CharField(max_length=256, blank=True)
    activity_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.devid)

