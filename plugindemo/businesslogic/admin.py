from django.contrib import admin
from .models import Endpoint, Forward, Datalogger, DataloggerForward


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('path', 'handler', 'created_at', 'updated_at')


admin.site.register(Endpoint, EndpointAdmin)


class ForwardAdmin(admin.ModelAdmin):
    list_display = ('handler', 'config', 'created_at', 'updated_at')


admin.site.register(Forward, ForwardAdmin)


class ForwardInline(admin.StackedInline):
    model = DataloggerForward
    extra = 1


class DataloggerAdmin(admin.ModelAdmin):
    inlines = [ForwardInline]
    list_display = ('devid', 'name', 'activity_at', 'created_at')


admin.site.register(Datalogger, DataloggerAdmin)
