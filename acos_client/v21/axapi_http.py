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
import socket
import ssl
import sys
import time
import urlparse

import responses as acos_responses

import acos_client
from acos_client import logutils

LOG = logging.getLogger(__name__)

out_hdlr = logging.StreamHandler(sys.stderr)
out_hdlr.setLevel(logging.ERROR)
LOG.addHandler(out_hdlr)
LOG.setLevel(logging.ERROR)


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
    q = urlparse.urlparse(api_url).query
    return urlparse.parse_qs(q).get('method', [u''])[0]


def merge_dicts(d1, d2):
    d = d1.copy()
    for k, v in d2.items():
        if k in d and isinstance(d[k], dict):
            d[k] = merge_dicts(d[k], d2[k])
        else:
            d[k] = d2[k]
    return d


broken_replies = {
    ('<?xml version="1.0" encoding="utf-8" ?><response status="ok">'
     '</response>'): (json.dumps({"response": {"status": "OK"}})),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" Partition does not exist. '
     '(internal error: 520749062)" /></response>'):
    (json.dumps({"response": {"status": "fail", "err": {"code": 999,
     "msg": " Partition does not exist."}}})),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" Failed to get partition. (internal error: '
     '402718800)" /></response>'):
    (json.dumps({"response": {"status": "fail", "err": {"code": 999,
     "msg": " Partition does not exist."}}})),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="1076" msg="Invalid partition parameter." /></response>'):
    (json.dumps({"response": {"status": "fail", "err": {"code": 1076,
     "msg": "Invalid partition parameter."}}})),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" No such aFleX. (internal error: '
     '17039361)" /></response>'):
    (json.dumps({"response": {"status": "fail", "err": {"code": 17039361,
     "msg": " No such aFleX."}}})),

    ('<?xml version="1.0" encoding="utf-8" ?><response status="fail">'
     '<error code="999" msg=" This aFleX is in use. (internal error: '
     '17039364)" /></response>'):
    (json.dumps({"response": {"status": "fail", "err": {"code": 17039364,
     "msg": " This aFleX is in use."}}})),

}


class EmptyHttpResponse(Exception):
    def __init__(self, response):
        self.response = response


class HttpClient(object):
    HEADERS = {
        "Content-type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % acos_client.VERSION,
    }

    headers = {}

    def __init__(self, host, port=None, protocol="https", client=None, timeout=None,
                 retry_errno_list=None):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        if port is None:
            if protocol is 'http':
                self.port = 80
            else:
                self.port = 443
        self.retry_errnos = [errno.ECONNRESET, errno.ECONNREFUSED]
        if retry_errno_list is not None:
            self.retry_errnos += retry_errno_list

    def _http(self, method, api_url, payload):
        if self.protocol == 'https':
            http = httplib.HTTPSConnection(self.host, self.port, timeout=self.timeout)
            http.connect = lambda: force_tlsv1_connect(http)
        else:
            http = httplib.HTTPConnection(self.host, self.port, timeout=self.timeout)

        LOG.debug("axapi_http: url:     %s", api_url)
        LOG.debug("axapi_http: method:  %s", method)
        LOG.debug("axapi_http: headers: %s", logutils.clean(self.HEADERS))
        LOG.debug("axapi_http: payload: %s", logutils.clean(payload))

        http.request(method, api_url, body=payload, headers=self.headers)

        r = http.getresponse()

        # Workaround for zero length response
        def handle_empty_response(data):
            if not data:
                raise EmptyHttpResponse(r)

            return data

        return handle_empty_response(r.read())

    def request(self, method, api_url, params={}, **kwargs):
        LOG.debug("axapi_http: url = %s", api_url)
        LOG.debug("axapi_http: params = %s", logutils.clean(params))

        self.headers = self.HEADERS

        if params:
            extra_params = kwargs.get('axapi_args', {})
            params_copy = merge_dicts(params, extra_params)
            LOG.debug("axapi_http: params_all = %s", logutils.clean(params_copy))

            payload = json.dumps(params_copy, encoding='utf-8')
        else:
            try:
                payload = kwargs.pop('payload', None)
                self.headers = dict(self.headers, **kwargs.pop('headers', {}))
                LOG.debug("axapi_http: headers_all = %s", logutils.clean(self.headers))
            except KeyError:
                payload = None

        last_e = None

        for i in xrange(0, 600):
            try:
                last_e = None
                data = self._http(method, api_url, payload)
                break
            except socket.error as e:
                # Workaround some bogosity in the API
                if e.errno in self.retry_errnos:
                    time.sleep(0.1)
                    last_e = e
                    continue
                raise e
            except httplib.BadStatusLine as e:
                time.sleep(0.1)
                last_e = e
                continue
            except EmptyHttpResponse as e:
                if e.response.status != httplib.OK:
                    msg = dict(e.response.msg.items())
                    data = json.dumps({"response": {'status': 'fail', 'err':
                                      {'code': e.response.status,
                                       'msg': msg}}})
                else:
                    data = json.dumps({"response": {"status": "OK"}})
                break

        if last_e is not None:
            raise e

        LOG.debug("axapi_http: data = %s", logutils.clean(data))

        # Fixup some broken stuff in an earlier version of the axapi
        # xmlok = ('<?xml version="1.0" encoding="utf-8" ?>'
        #          '<response status="ok"></response>')
        # if data == xmlok:
        #     return {'response': {'status': 'OK'}}
        # TODO()
        if data in broken_replies:
            data = broken_replies[data]
            LOG.debug("axapi_http: broken reply, new response: %s",
                      logutils.clean(data))

        try:
            r = json.loads(data, encoding='utf-8')
        except ValueError as e:
            # Handle non json response
            LOG.debug("axapi_http: json = %s", e)
            return data

        if 'response' in r and 'status' in r['response']:
            if r['response']['status'] == 'fail':
                    acos_responses.raise_axapi_ex(
                        r, action=extract_method(api_url))

        return r

    def get(self, api_url, params={}, **kwargs):
        return self.request("GET", api_url, params, **kwargs)

    def post(self, api_url, params={}, **kwargs):
        return self.request("POST", api_url, params, **kwargs)
