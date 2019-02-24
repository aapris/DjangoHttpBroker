import json
from django.db import models
from .providers.endpoint import EndpointProvider
from .providers.forward import ForwardProvider
from .providers.decoder import DecoderProvider
from django.core.exceptions import ValidationError
from broker.setup import import_plugins

import_plugins()
endpoints = EndpointProvider.get_plugins()
ENDPOINT_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in endpoints]
forwards = ForwardProvider.get_plugins()
FORWARD_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in forwards]
decoders = DecoderProvider.get_plugins()
DECODER_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in forwards]


class Endpoint(models.Model):
    path = models.CharField(db_index=True, max_length=256)
    handler = models.CharField(max_length=64, choices=ENDPOINT_HANDLER_CHOICES)
    config = models.TextField(default='', help_text='All required configuration parameters in JSON format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.path)

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)


class Datalogger(models.Model):
    devid = models.CharField(db_index=True, unique=True, max_length=256)
    name = models.CharField(max_length=256, blank=True)
    forwards = models.ManyToManyField('Forward',
                                      blank=True,
                                      through="DataloggerForward",
                                      # related_name="related_dataloggers",
                                      verbose_name="Data to forward")
    activity_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.devid)


class Forward(models.Model):
    # datalogger = models.ForeignKey(Datalogger, on_delete=models.CASCADE)
    handler = models.CharField(max_length=64, choices=FORWARD_HANDLER_CHOICES)
    config = models.TextField(default='', help_text='All required configuration parameters in JSON format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.handler)

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)


class DataloggerForward(models.Model):
    datalogger = models.ForeignKey(Datalogger, on_delete=models.CASCADE)
    dataforward = models.ForeignKey(Forward, on_delete=models.CASCADE)
    config = models.TextField(default='', help_text='All required configuration parameters in JSON format')

    def __str__(self):
        return f'{self.datalogger} -> {self.dataforward}'

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)


class Decoder(models.Model):
    handler = models.CharField(max_length=64, choices=DECODER_HANDLER_CHOICES)
    config = models.TextField(default='', help_text='All required configuration parameters in JSON format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.handler)

    def clean(self, exclude=None):
        try:
            config = json.loads(self.config)
        except json.JSONDecodeError as err:
            raise ValidationError(f'JSON error in config: {err}')
        self.config = json.dumps(config, indent=1)
