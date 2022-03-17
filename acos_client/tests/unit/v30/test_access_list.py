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
GET_URL = '{}/access-list'.format(BASE_URL)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @responses.activate
    def test_list_access_list(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.GET, GET_URL, json=json_response, status=200)

        resp = self.client.access_list.list()
        self.assertEqual(resp, json_response)
