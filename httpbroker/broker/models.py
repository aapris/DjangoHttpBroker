import json

from django.core.exceptions import ValidationError
from django.db import models

from broker.setup import import_plugins
from .providers.decoder import DecoderProvider
from .providers.endpoint import EndpointProvider
from .providers.forward import ForwardProvider

import_plugins()


# TODO: reset all migrations
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

def get_handler_choices(Model):
    plugins = Model.get_plugins()
    return [(f'{p.app}.{p.name}', f'{p.app}.{p.name}') for p in plugins]


class JsonConfigModel(models.Model):
    name = models.CharField(max_length=256, blank=True)
    description = models.TextField(max_length=10000, blank=True)
    config = models.TextField(default='', help_text='All required configuration parameters in JSON format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)

    class Meta:
        abstract = True


class Endpoint(JsonConfigModel):
    path = models.CharField(db_index=True, max_length=256)
    handler = models.CharField(max_length=64, choices=get_handler_choices(EndpointProvider))

    def __str__(self):
        return '{} / {} ({})'.format(self.path, self.handler, self.name)


class Forward(JsonConfigModel):
    handler = models.CharField(max_length=64, choices=get_handler_choices(ForwardProvider))

    def __str__(self):
        return '{} ({})'.format(self.handler, self.name)


# TODO: check this, seems a bit obsolete
class Decoder(JsonConfigModel):
    handler = models.CharField(max_length=64, choices=get_handler_choices(DecoderProvider))

    def __str__(self):
        return '{} ({})'.format(self.handler, self.name)


class Application(JsonConfigModel):
    decoder = models.CharField(max_length=128, blank=True, choices=get_handler_choices(DecoderProvider))

    def __str__(self):
        return '{}'.format(self.name)


class Datalogger(models.Model):
    devid = models.CharField(db_index=True, unique=True, max_length=256)
    application = models.ForeignKey(Application, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataloggers')
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=10000, blank=True)
    decoder = models.CharField(max_length=128, blank=True, choices=get_handler_choices(DecoderProvider))
    forwards = models.ManyToManyField(Forward,
                                      blank=True,
                                      through="DataloggerForward",
                                      related_name="related_dataloggers",
                                      verbose_name="Data to forward")
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=256, blank=True)
    locality = models.CharField(max_length=256, blank=True)
    street = models.CharField(max_length=256, blank=True)
    activity_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.devid} ({self.decoder})'


class DataloggerForward(models.Model):
    datalogger = models.ForeignKey(Datalogger, on_delete=models.CASCADE, related_name='dataloggerforwards')
    forward = models.ForeignKey(Forward, on_delete=models.CASCADE, related_name='dataloggerforwards')
    config = models.TextField(default='{}', help_text='All required configuration parameters in JSON format')

    def __str__(self):
        return f'{self.datalogger} -> {self.forward}'

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)
