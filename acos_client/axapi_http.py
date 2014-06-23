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
import socket
import ssl


# Monkey patch for ssl connect, for specific TLS version required by
# ACOS hardware.
def force_tlsv1_connect(self):
    sock = socket.create_connection((self.host, self.port), self.timeout)
    if self._tunnel_host:
        self.sock = sock
        self._tunnel()
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                ssl_version=ssl.PROTOCOL_TLSv1)


class HttpClient(object):
    def __init__(self, host, port=None, protocol="https"):
        self.host = host
        self.port = port
        self.protocol = protocol
        if port is None:
            if protocol is 'http':
                port = 80
            else:
                port = 443

    def request(self, method, api_url, params={}):
        if self.protocol == 'https':
            http = httplib.HTTPSConnection(self.host, self.port)
            http.connect = lambda: force_tlsv1_connect(http)
        else:
            http = httplib.HTTPConnection(self.host, self.port)

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OS-LBaaS-AGENT"
        }

        LOG.debug("axapi_http: start")
        LOG.debug("axapi_http: url = %s", api_url)
        LOG.debug("axapi_http: params = %s", params)

        if params:
            payload = json.dumps(params, encoding='utf-8')
        else:
            payload = None

        http.request(method, api_url, payload, headers)
        data = http.getresponse().read()

        LOG.debug("axapi_http: data = %s", data)

        # Fixup some broken stuff in an earlier version of the axapi
        xmlok = ('<?xml version="1.0" encoding="utf-8" ?>'
                 '<response status="ok"></response>')
        if data == xmlok:
            return {'response': {'status': 'OK'}}

        return json.loads(data)

