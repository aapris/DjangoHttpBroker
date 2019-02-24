# Django HTTP Broker

This Django project aims to demonstrate as simple plugin system as possible.
The use case is to provide an endpoint to any IoT device or data logger 
(later "a node"),  which uses HTTP(S) to send its data at least in the last 
hop to the data storage.

In many cases it is not possible to configure a node to use some predefined 
endpoint and the data formats vary a lot, and creating new endpoints should
be as fast and easy as possible. 

# How to use

Create a Django app using command  
`python manage.py startapp yourpluginapp`  
and a directory called `endpoints` inside it.
Then add these two lines in `yourpluginapp/endpoints/__init__.py`:
```
from broker.endpoint import import_endpoints
import_endpoints(__file__, __name__)
```


See
[demoplugin/endpoints/keyval.py](httpbroker/demoplugin/endpoints/keyval.py) 
of how to implement your own endpoint plugin.

```
from django.http.response import HttpResponse
from broker.endpoint import EndpointProvider

class ExampleEndpoint(EndpointProvider):
    description = "Example endpoint's short description"

    def handle_request(self, request):
        # Do your stuff here for request data and return HttpResponse
        ...        
        return HttpResponse(f'$OK$ {self.name}', content_type='text/plain')

```

## Key files

Most important files are listed below:

### [httpbroker/settings.py](httpbroker/httpbroker/settings.py)
`INSTALLED_APPS` contains zero or more apps which provide additional plugins.

### [broker/urls.py](httpbroker/broker/urls.py)
`urlpatterns` has one catch-all entry, which handles all requested URLs 
(except `/admin/`):
`re_path(r'^(?P<path>.*)$', views.catchall),`

### [broker/views.py](httpbroker/broker/views.py)
View function `catchall(request, path)` finds the right handler for
requested URL or returns `HTTP 404 Not Found`, 
if requested URL is not defined.  

### [broker/models.py](httpbroker/broker/models.py)
`Endpoint` model stores paths (URLs) and their handlers. 
`HANDLER_CHOICES` is populated once, when Django process is started.

### [broker/plugin.py](httpbroker/broker/endpoint.py)
`PluginMount` and  `EndpointProvider` classes are introduced here.
Every valid plugin must extend `EndpointProvider` and implement 
`handle_request(request)` function which returns `HttpResponse`.

### [broker/setup.py](httpbroker/broker/setup.py)
`import_plugins()` is defined here and it loads all 
plugins which are found from `httpbroker/appname/endpoints/` directories.

### [broker/admin.py](httpbroker/broker/admin.py)
Registers `EndpointAdmin`.

### [httpbroker/wsgi.py](httpbroker/httpbroker/wsgi.py) and [manage.py](httpbroker/manage.py) 
Both start-up commands import `import_plugins` from `broker.setup`
and then initialise plugins: `import_plugins()`

### [demoplugin/endpoints/\_\_init\_\_.py](httpbroker/demoplugin/endpoints/__init__.py)
All `appname/endpoints/__init__.py` files contain the same code – which loads 
all plugins in the same directory

### [demoplugin/endpoints/keyval.py](httpbroker/demoplugin/endpoints/keyval.py)
An example plugin, which handles the request, but doesn't save 
the data or pass it forward.

# Testing demo

Note: this project requires Python >=3.6

Try this:

```
git clone https://github.com/aapris/DjangoHttpBroker.git
cd DjangoHttpBroker/
virtualenv -p /usr/local/bin/python3.6 venv  # Check your python3 path!
source venv/bin/activate
pip install -r requirements.txt 
cd httpbroker/
python manage.py migrate
python manage.py loaddata fixtures/testdata.json 
python manage.py runserver
```

The open URLs 
http://127.0.0.1:8000/iotendpoint/v2  
http://127.0.0.1:8000/savedata.php and  
http "http://dataloggeruser:very42hard66pass@127.0.0.1:8000/savedata.php?devid=3AFF42&temp=22.1&humidity=42&pressure=1013.4&foo=42"  
in your browser or use curl, HTTPie or similar:

```
(venv) $ http -v GET http://127.0.0.1:8000/iotendpoint/v2

GET /iotendpoint/v2 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: 127.0.0.1:8000
User-Agent: HTTPie/1.0.2



HTTP/1.1 200 OK
Content-Length: 23
Content-Type: text/plain
Date: Sat, 29 Dec 2018 14:51:01 GMT
Server: WSGIServer/0.2 CPython/3.6.6
X-Frame-Options: SAMEORIGIN

$OK$ ColumnDataEndpoint
```
You can manage endpoints in Django Admin, username and password are `admin` and `admin`.
http://127.0.0.1:8000/admin/broker/endpoint/

# Celery

[keyval.py](httpbroker/demoplugin/endpoints/keyval.py) endpoint uses
Celery task (defined in
[demoplugin/tasks.py](httpbroker/demoplugin/tasks.py))
to process the request data later. You need RabbitMQ or some other broker 
to deliver jobs from Django view to Celery.

Run celery in the same directory where `manage.py` lives like this:  
`celery -A httpbroker worker -l info`
