# DjangoPluginDemo

Try this:

```
git clone https://github.com/aapris/DjangoPluginDemo.git
cd DjangoPluginDemo/
virtualenv -p /usr/local/bin/python3.6 venv
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
