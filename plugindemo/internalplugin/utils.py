import base64
from django.contrib.auth import authenticate
from django.utils import timezone


def basicauth(request):
    """Check for valid basic auth header."""
    uname, passwd, user = None, None, None
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                a = auth[1].encode('utf8')
                s = base64.b64decode(a)
                uname, passwd = s.decode('utf8').split(':')
                user = authenticate(username=uname, password=passwd)
    return uname, passwd, user


def get_datalogger(devid, name='', update_activity=False):
    # FIXME: Shit, this import can't be in the beginning of the file or we'll get:
    # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
    # It can be imported if you run django.setup() before import, but it messes up loading  
    # import django
    # django.setup()
    # from businesslogic.models import Datalogger
    from businesslogic.models import Datalogger

    datalogger, created = Datalogger.objects.get_or_create(devid=devid)
    changed = False
    if created:
        datalogger.name = name
        changed = True
    if update_activity:
        datalogger.activity_at = timezone.now()
        changed = True
    if changed:
        datalogger.save()
    return datalogger, created
