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

from __future__ import absolute_import
from __future__ import unicode_literals

import json
import logging
from requests.adapters import HTTPAdapter
from requests import Session
import six
import sys

import acos_client
from acos_client import logutils
from acos_client.v21 import responses as acos_responses
from acos_client.v21.ssl_adapter import SSLAdapter

LOG = logging.getLogger(__name__)

out_hdlr = logging.StreamHandler(sys.stderr)
out_hdlr.setLevel(logging.ERROR)
LOG.addHandler(out_hdlr)
LOG.setLevel(logging.ERROR)


def extract_method(api_url):
    q = six.moves.urllib_parse.urlparse(api_url).query
    return six.moves.urllib_parse.parse_qs(q).get('method', [''])[0]


def merge_dicts(d1, d2):
    d = d1.copy()
    # if isinstance(d1, dict) else {}
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


class HttpClient(object):
    HEADERS = {
        "Content-type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % acos_client.VERSION,
    }

    def __init__(self, host, port=None, protocol="https", max_retries=3, timeout=5):
        if port is None:
            if protocol is 'http':
                self.port = 80
            else:
                self.port = 443
        else:
            self.port = port
        self.url_base = "%s://%s:%s" % (protocol, host, self.port)
        self.max_retries = max_retries
        self.timeout = timeout

    def request(self, method, api_url, params={}, **kwargs):
        """Generate the API call to the device."""

        LOG.debug("axapi_http: full url = %s", self.url_base + api_url)
        LOG.debug("axapi_http: %s url = %s", method, api_url)
        LOG.debug("axapi_http: params = %s", json.dumps(logutils.clean(params), indent=4))

        # Set "data" variable for the request
        if params:
            extra_params = kwargs.get('axapi_args', {})
            params_copy = merge_dicts(params, extra_params)
            LOG.debug("axapi_http: params_all = %s", logutils.clean(params_copy))

            payload = json.dumps(params_copy)
        else:
            try:
                payload = kwargs.pop('payload', None)
                self.headers = dict(self.HEADERS, **kwargs.pop('headers', {}))
                LOG.debug("axapi_http: headers_all = %s", logutils.clean(self.headers))
            except KeyError:
                payload = None

        max_retries = kwargs.get('max_retries', self.max_retries)
        timeout = kwargs.get('timeout', self.timeout)

        # Create session to set HTTPAdapter or SSLAdapter
        session = Session()
        if self.port == 443:
            # Add adapter for any https session to force TLS1_0 connection for v21 of AXAPI
            session.mount('https://', SSLAdapter(max_retries=max_retries))
        else:
            session.mount('http://', HTTPAdapter(max_retries=max_retries))
        session_request = getattr(session, method.lower())

        # Make actual request and handle any errors
        try:
            device_response = session_request(
                self.url_base + api_url, verify=False, data=payload, headers=self.HEADERS, timeout=timeout
            )
        except (Exception) as e:
            LOG.error("acos_client failing with error %s after %s retries", e.__class__.__name__, max_retries)
            raise e
        finally:
            session.close()

        # Log if the reponse is one of the known broken response
        if device_response in broken_replies:
            device_response = broken_replies[device_response]
            LOG.debug("axapi_http: broken reply, new response: %s", logutils.clean(device_response))

        # Validate json response
        try:
            json_response = device_response.json()
            LOG.debug("axapi_http: data = %s", json.dumps(logutils.clean(json_response), indent=4))
        except ValueError as e:
            # The response is not JSON but it still succeeded.
            LOG.debug("axapi_http: json = %s", e)
            return device_response

        # Handle "fail" responses returned by AXAPI
        if 'response' in json_response and 'status' in json_response['response']:
            if json_response['response']['status'] == 'fail':
                    acos_responses.raise_axapi_ex(json_response, action=extract_method(api_url))

        # Return json portion of response
        return json_response

    def get(self, api_url, params={}, **kwargs):
        return self.request("GET", api_url, params, **kwargs)

    def post(self, api_url, params={}, **kwargs):
        return self.request("POST", api_url, params, **kwargs)
