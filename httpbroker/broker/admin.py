from django.contrib import admin
from .models import Endpoint, Forward, Decoder


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('path', 'handler', 'created_at', 'updated_at')


admin.site.register(Endpoint, EndpointAdmin)


class ForwardAdmin(admin.ModelAdmin):
    list_display = ('handler', 'config', 'created_at', 'updated_at')


admin.site.register(Forward, ForwardAdmin)


class DecoderAdmin(admin.ModelAdmin):
    list_display = ('handler', 'created_at', 'updated_at')


admin.site.register(Decoder, DecoderAdmin)
