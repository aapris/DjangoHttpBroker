import json
from io import StringIO

from django.core import management
from django.test import Client
from django.test import TestCase

from broker.models import Endpoint

ENDPOINT_PATH = 'default'


class EndpointTestCase(TestCase):
    def setUp(self):
        Endpoint.objects.create(path=ENDPOINT_PATH, handler='broker.DefaultEndpoint')

    def test_endpoints(self):
        """Test default endpoint and how request data is stored to the filesystem"""
        c = Client()

        # Test endpoint
        response = c.get(f'/{ENDPOINT_PATH}')
        self.assertEqual(response.status_code, 200)

        # Test data which was dumped to the disk during request
        out = StringIO()
        devid = f'unknown-{ENDPOINT_PATH}'
        management.call_command('extract_message', '--devid', devid, stdout=out)
        request_data = json.loads(out.getvalue())
        self.assertEqual(request_data['devid'], devid)
