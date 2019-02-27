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
DECODER_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in decoders]


class JsonConfigModel(models.Model):
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
    handler = models.CharField(max_length=64, choices=ENDPOINT_HANDLER_CHOICES)

    def __str__(self):
        return '{}'.format(self.path)


class Forward(JsonConfigModel):
    handler = models.CharField(max_length=64, choices=FORWARD_HANDLER_CHOICES)

    def __str__(self):
        return '{}'.format(self.handler)


class Decoder(JsonConfigModel):
    handler = models.CharField(max_length=64, choices=DECODER_HANDLER_CHOICES)

    def __str__(self):
        return '{}'.format(self.handler)
