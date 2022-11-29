from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client.v30.router.bgp import Bgp

class TestRouterBgp(unittest.TestCase):

    def setUp(self) -> None:
        self.client = mock.MagicMock()
        self.bgp = Bgp(client=self.client)
        self.url_prefix = "/axapi/v3/router/bgp/"
        self.bgp_asn = 65123

    def test_bgp_get(self):
        self.bgp.get_list(asn=self.bgp_asn)
        _url = f"{self.url_prefix}{self.bgp_asn}/"
        self.client.http.request.assert_called_with("GET", _url, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
        self.bgp.get(asn=self.bgp_asn)
        self.client.http.request.assert_called_with("GET", _url, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_neighbor_peer_group_get(self):
        _url_prefix = f"{self.url_prefix}{self.bgp_asn}/neighbor/peer-group-neighbor/"
        self.bgp.neighbor.peer_group.get_list(asn=self.bgp_asn)
        self.client.http.request.assert_called_with("GET", _url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
        pg = "TEST"
        self.bgp.neighbor.peer_group.get(asn=self.bgp_asn, key=pg)
        self.client.http.request.assert_called_with("GET", f"{_url_prefix}{pg}", {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_neighbor_ipv4_get(self):
        _url_prefix = f"{self.url_prefix}{self.bgp_asn}/neighbor/ipv4-neighbor/"
        self.bgp.neighbor.ipv4_neighbor.get_list(asn=self.bgp_asn)
        self.client.http.request.assert_called_with("GET", _url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
        ipv4 = "1.1.1.1"
        self.bgp.neighbor.ipv4_neighbor.get(asn=self.bgp_asn, key=ipv4)
        self.client.http.request.assert_called_with("GET", f"{_url_prefix}{ipv4}", {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_af_peer_group_get(self):
        _url_prefix = f"{self.url_prefix}{self.bgp_asn}/address-family/ipv6/neighbor/peer-group-neighbor/"
        self.bgp.address_family.peer_group.get_list(asn=self.bgp_asn)
        self.client.http.request.assert_called_with("GET", _url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
        pg = "TEST"
        self.bgp.address_family.peer_group.get(asn=self.bgp_asn, key=pg)
        self.client.http.request.assert_called_with("GET", f"{_url_prefix}{pg}", {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_af_ipv6_get(self):
        _url_prefix = f"{self.url_prefix}{self.bgp_asn}/address-family/ipv6/neighbor/ipv6-neighbor/"
        self.bgp.address_family.ipv6_neighbor.get_list(asn=self.bgp_asn)
        self.client.http.request.assert_called_with("GET", _url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
        ipv6 = "6001:8080::1"
        self.bgp.address_family.ipv6_neighbor.get(asn=self.bgp_asn, key=ipv6)
        self.client.http.request.assert_called_with("GET", f"{_url_prefix}{ipv6}", {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)
