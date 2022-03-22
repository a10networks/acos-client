try:
    import unittest
except ImportError:
    import unittest2 as unittest

from acos_client import client
import responses


HOSTNAME = 'fake_a10'
BASE_URL = "https://{}:443/axapi/v3".format(HOSTNAME)
AUTH_URL = "{}/auth".format(BASE_URL)
VSERVER_NAME = 'test'
OK_RESP = {'response': {'status': 'OK'}}


class TestAccessList(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @responses.activate
    def test_list_access_list(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.GET, '{}/access-list'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.access_list.list()
        self.assertEqual(resp, json_response)

    @responses.activate
    def test_get_access_list(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.GET, '{}/access-list/standard/123'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.access_list.get(123)
        self.assertEqual(resp, json_response)

    @responses.activate
    def test_post_access_list(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        responses.add(responses.POST, '{}/access-list/standard'.format(BASE_URL),
                      json=OK_RESP, status=200)
        request_params = {
            'std': 1,
            'stdrules': [{
                'action': 'permit',
                'host': '192.168.0.1'
            }]
        }

        resp = self.client.access_list.create(**request_params)
        self.assertEqual(resp, OK_RESP)
