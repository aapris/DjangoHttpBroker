from django.contrib import admin
from .models import Endpoint, Forward, Decoder
from .models import Application, Datalogger, DataloggerForward


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('path', 'handler', 'name', 'created_at', 'updated_at')


admin.site.register(Endpoint, EndpointAdmin)


class ForwardAdmin(admin.ModelAdmin):
    list_display = ('handler', 'name', 'config', 'created_at', 'updated_at')


admin.site.register(Forward, ForwardAdmin)


class DecoderAdmin(admin.ModelAdmin):
    list_display = ('handler', 'name', 'created_at', 'updated_at')


admin.site.register(Decoder, DecoderAdmin)


class ForwardInline(admin.StackedInline):
    model = DataloggerForward
    extra = 1


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'config')


admin.site.register(Application, ApplicationAdmin)


class DataloggerAdmin(admin.ModelAdmin):
    inlines = [ForwardInline]
    list_display = ('devid', 'name', 'activity_at', 'created_at')
    search_fields = ('devid', 'name', 'description', 'decoder')


admin.site.register(Datalogger, DataloggerAdmin)
