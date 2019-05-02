import datetime
import json
import msgpack
import os
import glob
from django.conf import settings
from django.core.management.base import BaseCommand


def list_dates(base_dir, path):
    dirs = os.listdir(base_dir)
    dirs.sort()
    print(f'Directory {path} does not exist.\nUse e.g. `--date {dirs[-1]}` parameter or some other listed below:\n')
    print('\n'.join(dirs))


def list_devids(path):
    files = glob.glob(f'{path}/*.msgpack')
    devids = [x.split('.')[-2] for x in files]
    devids.sort()
    print(f'Devid does not exist.\nUse e.g. `--devid {devids[-1]}` parameter or some other listed below:\n')
    print('\n'.join(devids))


def fix_body_encoding(req):
    if isinstance(req.get('request.body'), bytes):
        req['request.body'] = req['request.body'].decode('utf8')


def print_request(req, options):
    fix_body_encoding(req)
    if options['pretty']:
        print(json.dumps(req, indent=2))
    else:
        print(json.dumps(req))


def print_httpie(req, options):
    fix_body_encoding(req)
    headers = req['request.headers']
    headers_str = ' '.join({f'{k}:"{v}"' for (k, v) in headers.items()})
    body = req['request.body']
    method = req['request.META']['REQUEST_METHOD']
    query_string = req['request.META']['QUERY_STRING']
    path = req['request.META']['PATH_INFO']
    scheme = 'http'
    host = '127.0.0.1'
    port = '8000'
    httpie = f'echo -n \'{body}\' | http -v {method} "{scheme}://{host}:{port}{path}?{query_string}" {headers_str}'
    print(httpie)


class Command(BaseCommand):
    help = 'List all configured Endpoints'

    def add_arguments(self, parser):
        parser.add_argument('--devid', type=str)
        parser.add_argument('--date', type=str)
        parser.add_argument('-i', '--index', type=int, default=-1)
        parser.add_argument('-p', '--pretty', action='store_true')
        parser.add_argument('--httpie', action='store_true')

    def handle(self, *args, **options):
        devid = options['devid']
        base_dir = os.path.join(settings.VAR_DIR, 'httprequests')  # FIXME: this is in save_raw_http too
        if options['date'] is None:
            date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        else:
            date = options['date']
        path = os.path.join(base_dir, date)  # FIXME: this is in save_raw_http too
        if os.path.isdir(path) is False:
            list_dates(base_dir, path)
            exit()
        if devid is None:
            list_devids(path)
            exit()
        fnames = glob.glob(f'{path}/*{devid}.msgpack')
        if len(fnames) == 0:
            print('error')
            exit()
        with open(fnames[0], 'rb') as f:
            unpacker = msgpack.Unpacker(raw=False)
            unpacker.feed(f.read())
            requests = []
            for msg in unpacker:
                requests.append(msg)
            req = requests[options['index']]
            if options['httpie']:
                print_httpie(req, options)
            else:
                print_request(req, options)
