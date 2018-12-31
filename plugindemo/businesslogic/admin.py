from django.contrib import admin
from .models import Endpoint, Datalogger


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('path', 'handler', 'created', 'updated')


admin.site.register(Endpoint, EndpointAdmin)


class DataloggerAdmin(admin.ModelAdmin):
    list_display = ('devid', 'name', 'activity_at', 'created_at')


admin.site.register(Datalogger, DataloggerAdmin)
