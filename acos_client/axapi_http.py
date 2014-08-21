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

import errno
import httplib
import json
import logging
import re
import socket
import ssl
import time

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
    m = re.search("method=([^&]+)", api_url)
    if m is not None:
        return m.group(1)
    return ""

broken_replies = {
    ('<?xml version="1.0" encoding="utf-8" ?><response status="ok">'
     '</response>'): '{"response": {"status": "OK"}}',

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" Partition does not exist. '
     '(internal error: 520749062)" /></response>'):
    ('{"response": {"status": "fail", "err": {"code": 999,'
     '"msg": " Partition does not exist."}}}'),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" Failed to get partition. (internal error: '
     '402718800)" /></response>'):
    ('{"response": {"status": "fail", "err": {"code": 999,'
     '"msg": " Partition does not exist."}}}'),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="1076" msg="Invalid partition parameter." /></response>'):
    ('{"response": {"status": "fail", "err": {"code": 1076,'
     '"msg": "Invalid partition parameter."}}}'),
}


class HttpClient(object):
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % VERSION
    }

    def __init__(self, host, port=None, protocol="https", client=None):
        self.host = host
        self.port = port
        self.protocol = protocol
        if port is None:
            if protocol is 'http':
                port = 80
            else:
                port = 443
        self.client = client

    def _http(self, method, api_url, payload):
        if self.protocol == 'https':
            http = httplib.HTTPSConnection(self.host, self.port)
            http.connect = lambda: force_tlsv1_connect(http)
        else:
            http = httplib.HTTPConnection(self.host, self.port)

        http.request(method, api_url, payload, self.HEADERS)
        return http.getresponse().read()

    # temporary brutal hack
    def _url(self, action):
        return ("/services/rest/v2.1/?format=json&method=%s&session_id=%s" %
                (action, self.client.session.id))

    def request(self, method, api_url, params={}):
        LOG.debug("axapi_http: url = %s", api_url)
        LOG.debug("axapi_http: params = %s", params)

        if params:
            payload = json.dumps(params, encoding='utf-8')
        else:
            payload = None

        for i in xrange(0, 600):
            try:
                last_e = None
                data = self._http(method, api_url, payload)
                break
            except socket.error as e:
                # Workaround some bogosity in the API
                if (e.errno == errno.ECONNRESET or
                   e.errno == errno.ECONNREFUSED):
                    time.sleep(0.1)
                    last_e = e
                    continue
                raise e
            except httplib.BadStatusLine as e:
                time.sleep(0.1)
                last_e = e
                continue

        if last_e is not None:
            raise e

        LOG.debug("axapi_http: data = %s", data)

        # Fixup some broken stuff in an earlier version of the axapi
        # xmlok = ('<?xml version="1.0" encoding="utf-8" ?>'
        #          '<response status="ok"></response>')
        # if data == xmlok:
        #     return {'response': {'status': 'OK'}}
        if data in broken_replies:
            data = broken_replies[data]

        r = json.loads(data, encoding='utf-8')

        if 'response' in r and 'status' in r['response']:
            if r['response']['status'] == 'fail':
                    acos_errors.raise_axapi_ex(r,
                                               action=extract_method(api_url))

        return r

    def get(self, api_url, params={}):
        return self.request("GET", api_url, params)

    def post(self, api_url, params={}):
        return self.request("POST", api_url, params)
