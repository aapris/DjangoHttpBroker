from django.contrib import admin
from .models import Endpoint


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('path', 'handler', 'created', 'updated')
admin.site.register(Endpoint, EndpointAdmin)
