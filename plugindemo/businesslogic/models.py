from django.db import models
from .endpoint import EndpointProvider, ForwardProvider

endpoints = EndpointProvider.get_plugins()
ENDPOINT_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in endpoints]
forwards = ForwardProvider.get_plugins()
FORWARD_HANDLER_CHOICES = [(f'{a.app}.{a.name}', f'{a.app}.{a.name}') for a in forwards]


class Endpoint(models.Model):
    path = models.CharField(db_index=True, max_length=256)
    handler = models.CharField(max_length=64, choices=ENDPOINT_HANDLER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.path)


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
    config = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.handler)


class DataloggerForward(models.Model):
    datalogger = models.ForeignKey(Datalogger, on_delete=models.CASCADE)
    dataforward = models.ForeignKey(Forward, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.datalogger} -> {self.dataforward}'
