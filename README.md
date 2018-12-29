# Django Plugin Demo

This Django project aims to demonstrate as simple plugin system as possible.
The use case is to provide an endpoint to any IoT device or data logger 
(later "a node"),  which uses HTTP(S) to send its data at least in the last 
hop to the data storage.

In many cases it is not possible to configure a node to use some predefined 
endpoint and the data formats vary a lot, and creating new endpoints should
be as fast and easy as possible. 

## Key files

Most important files are listed below:

### [plugindemo/settings.py](plugindemo/plugindemo/settings.py)
`INSTALLED_APPS` contains zero or more apps which provide additional plugins.

### [businesslogic/urls.py](plugindemo/businesslogic/urls.py)
`urlpatterns` has one catch-all entry, which handles all requested URLs 
(except `/admin/`).

### [businesslogic/views.py](plugindemo/businesslogic/views.py)
View function `catchall(request, path)` finds the right handler for
requested URL or returns `HTTP 404 Not Found`, 
if requested URL is not defined.  

### [businesslogic/models.py](plugindemo/businesslogic/models.py)
`Endpoint` model stores paths (URLs) and their handlers. 
`HANDLER_CHOICES` is populated once, when Django process is started.

### [businesslogic/plugin.py](plugindemo/businesslogic/endpoint.py)
`PluginMount` and  `EndpointProvider` classes are introduced here.
Every valid plugin must extend `EndpointProvider` and implement 
`handle_request(request)` function which returns `HttpResponse`.

### [businesslogic/setup.py](plugindemo/businesslogic/setup.py)
`import_plugins()` is defined here and it loads all 
plugins which are found from `plugindemo/appname/endpoints/` directories.

### [businesslogic/admin.py](plugindemo/businesslogic/admin.py)
Registers `EndpointAdmin`.

### [plugindemo/wsgi.py](plugindemo/plugindemo/wsgi.py) and [manage.py](plugindemo/manage.py) 
Both start-up commands import `import_plugins` from `businesslogic.setup`
and then initialise plugins: `import_plugins()`

### [builtinplugin/endpoints/\_\_init\_\_.py](plugindemo/internalplugin/endpoints/__init__.py)
All `appname/endpoints/__init__.py` files contain the same code – which loads 
all plugins in the same directory

### [builtinplugin/endpoints/keyval.py](plugindemo/internalplugin/endpoints/keyval.py)
An example plugin, which handles the request, but doesn't save 
the data or pass it forward.

# Testing demo

Note: this project requires Python >=3.6

Try this:

```
git clone https://github.com/aapris/DjangoPluginDemo.git
cd DjangoPluginDemo/
virtualenv -p /usr/local/bin/python3.6 venv  # Check your python3 path!
source venv/bin/activate
pip install -r requirements.txt 
cd plugindemo/
python manage.py migrate
python manage.py loaddata fixtures/testdata.json 
python manage.py runserver
```

The open URLs 
http://127.0.0.1:8000/iotendpoint/v2 and  
http://127.0.0.1:8000/savedata.php  
http://127.0.0.1:8000/savedata.php?dev_id=3AFF42&temp=22.1&humidity=42&pressure=1013.4  
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
Content-Length: 4
Content-Type: text/plain
Date: Wed, 26 Dec 2018 21:17:00 GMT
Server: WSGIServer/0.2 CPython/3.6.6
X-Frame-Options: SAMEORIGIN

$OK$

```
You can manage endpoints in Django Admin, username and password are `admin` and `admin`.
http://127.0.0.1:8000/admin/businesslogic/endpoint/
