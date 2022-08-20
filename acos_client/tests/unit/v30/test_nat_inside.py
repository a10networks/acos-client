try:
    import unittest
except ImportError:
    import unittest2 as unittest

from acos_client import client
import json
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
    def test_get_all_nat_inside_source_acls(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.GET,
                      '{}/ip/nat/inside/source/list'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.nat.inside.source.all()
        self.assertEqual(resp, json_response)

    @responses.activate
    def test_get_specific_nat_inside_source_acl(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.GET,
                      '{}/ip/nat/inside/source/list/acl-id-list/9'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.nat.inside.source.get_id_list(acl_id=9)
        self.assertEqual(resp, json_response)

    @responses.activate
    def test_create_nat_inside_source_acl(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.POST,
                      '{}/ip/nat/inside/source/list/acl-id-list'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.nat.inside.source.create_id_list(acl_id=9, pool='hoge')
        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(json.loads(responses.calls[1].request.body), {
            "acl-id-list": {
                "acl-id": 9,
                "pool": "hoge"
            }
        })

    @responses.activate
    def test_delete_nat_inside_source_acl(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = [{'foo': 'bar'}]
        responses.add(responses.DELETE,
                      '{}/ip/nat/inside/source/list/acl-id-list/9'.format(BASE_URL),
                      json=json_response, status=200)

        resp = self.client.nat.inside.source.delete_id_list(acl_id=9)
        self.assertEqual(resp, json_response)
