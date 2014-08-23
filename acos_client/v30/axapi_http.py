# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# import errno
# import httplib
import json
import logging

# import re
# import socket
# import ssl
# import time
import requests

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1


import acos_client.responses as acos_responses
from acos_client.version import VERSION

LOG = logging.getLogger(__name__)

import sys
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setLevel(logging.DEBUG)
LOG.addHandler(out_hdlr)

LOG.setLevel(logging.DEBUG)


broken_replies = {
    "": '{"response": {"status": "OK"}}'
}


class HttpClient(object):
    HEADERS = {
        "Content-type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % VERSION,
        # 'Connection': 'keep-alive',
        # 'Accept': '*/*',
    }

    def __init__(self, host, port=None, protocol="https", version=None):
        self.axapi_version = version
        self.host = host
        self.port = port
        self.protocol = protocol
        if port is None:
            if protocol is 'http':
                port = 80
            else:
                port = 443
        self.url_base = "%s://%s:%s" % (protocol, host, port)

    # def _http(self, method, api_url, payload, headers=None):
    #     if self.protocol == 'https':
    #         http = httplib.HTTPSConnection(self.host, self.port)
    #         http.connect = lambda: force_tlsv1_connect(http)
    #     else:
    #         http = httplib.HTTPConnection(self.host, self.port)

        # hdrs = self.HEADERS.copy()
        # if headers:
        #     hdrs.update(headers)

        # LOG.debug("axapi_http: url:     %s", api_url)
        # LOG.debug("axapi_http: method:  %s", method)
        # LOG.debug("axapi_http: headers: %s", hdrs)
        # LOG.debug("axapi_http: payload: %s", payload)
        # http.request(method, api_url, payload, hdrs)

        # resp = http.getresponse()
        # # print "RESP ", dir(resp)
        # # print "RESP HEADERS", resp.getheaders()
        # # LOG.debug("http response status %s", resp.status)
        # return resp.read()

    def request(self, method, api_url, params={}, headers=None):
        LOG.debug("axapi_http: full url = %s", self.url_base + api_url)
        LOG.debug("axapi_http: %s url = %s", method, api_url)
        LOG.debug("axapi_http: params = %s", params)

        if params:
            payload = json.dumps(params)
        else:
            payload = None

        hdrs = self.HEADERS.copy()
        if headers:
            hdrs.update(headers)

        LOG.debug("axapi_http: headers = %s", hdrs)

        z = requests.request(method, self.url_base + api_url,
                             verify=False,
                             data=payload,
                             headers=hdrs)
        # data = z.text

        # LOG.debug("axapi_http: data = %s", data)

        # # Fixup some broken stuff in an earlier version of the axapi
        # # xmlok = ('<?xml version="1.0" encoding="utf-8" ?>'
        # #          '<response status="ok"></response>')
        # # if data == xmlok:
        # #     return {'response': {'status': 'OK'}}
        # if data in broken_replies:
        #     data = broken_replies[data]
        #     LOG.debug("axapi_http: broken reply, new response: %s", data)

        # r = json.loads(data, encoding='utf-8')
        r = z.json()

        LOG.debug("axapi_http: data = %s", json.dumps(r, indent=4))

        if 'response' in r and 'status' in r['response']:
            if r['response']['status'] == 'fail':
                    acos_responses.raise_axapi_ex(
                        self.axapi_version, r,
                        action=api_url, method=method)

        if 'authorizationschema' in r:
            acos_responses.raise_axapi_auth_error(
                r, action=api_url, headers=headers)

        return r

    def get(self, api_url, params={}, headers=None):
        return self.request("GET", api_url, params, headers=headers)

    def post(self, api_url, params={}, headers=None):
        return self.request("POST", api_url, params, headers=headers)

    def put(self, api_url, params={}, headers=None):
        return self.request("PUT", api_url, params, headers=headers)

    def delete(self, api_url, params={}, headers=None):
        return self.request("DELETE", api_url, params, headers=headers)
