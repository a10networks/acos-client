# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

import httplib
import json
import logging
import re
import socket
import ssl

import errors as acos_errors
from version import VERSION

LOG = logging.getLogger(__name__)

import sys
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setLevel(logging.DEBUG)
LOG.addHandler(out_hdlr)

LOG.setLevel(logging.DEBUG)


# Monkey patch for ssl connect, for specific TLS version required by
# ACOS hardware.
def force_tlsv1_connect(self):
    sock = socket.create_connection((self.host, self.port), self.timeout)
    if self._tunnel_host:
        self.sock = sock
        self._tunnel()
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                ssl_version=ssl.PROTOCOL_TLSv1)

def extract_method(api_url):
    method = None
    m = re.search("method=([^&]+)", api_url)
    if m is not None:
        return m.group(1)
    return ""


class HttpClient(object):
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % VERSION
    }

    def __init__(self, host, port=None, protocol="https"):
        self.host = host
        self.port = port
        self.protocol = protocol
        if port is None:
            if protocol is 'http':
                port = 80
            else:
                port = 443

    def _http(self, method, api_url, payload):
        if self.protocol == 'https':
            http = httplib.HTTPSConnection(self.host, self.port)
            http.connect = lambda: force_tlsv1_connect(http)
        else:
            http = httplib.HTTPConnection(self.host, self.port)

        http.request(method, api_url, payload, self.HEADERS)
        return http.getresponse().read()

    def request(self, method, api_url, params={}):
        LOG.debug("axapi_http: url = %s", api_url)
        LOG.debug("axapi_http: params = %s", params)

        if params:
            payload = json.dumps(params, encoding='utf-8')
        else:
            payload = None

        data = self._http(method, api_url, payload)

        LOG.debug("axapi_http: data = %s", data)

        # Fixup some broken stuff in an earlier version of the axapi
        xmlok = ('<?xml version="1.0" encoding="utf-8" ?>'
                 '<response status="ok"></response>')
        if data == xmlok:
            return {'response': {'status': 'OK'}}

        r = json.loads(data, encoding='utf-8')

        if 'response' in r and 'status' in r['response']:
            if r['response']['status'] == 'fail':
                acos_errors.raise_axapi_ex(r, action=extract_method(api_url))

        return r

    def get(self, api_url, params={}):
        return self.request("GET", api_url, params)

    def post(self, api_url, params={}):
        return self.request("POST", api_url, params)


# socket.error: [Errno 54] Connection reset by peer


