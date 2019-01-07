from businesslogic.endpoint import ForwardProvider
import requests


class DummyHttpForward(ForwardProvider):
    description = 'Forward data to some other HTTP endpoint, just for an example'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def forward_data(self, data):
        # Forward data to another location, here it means POSTing it to an endpoint
        response = requests.post(url='http://127.0.0.1:8000/dummy', json=data)
        print(f'{response.status_code} {response.text}')
        return True
