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
from requests import ConnectionError
from requests.packages.urllib3.util.retry import Retry
from requests import Session
import six

import acos_client
from acos_client import logutils
from acos_client.v30 import responses as acos_responses

LOG = logging.getLogger(__name__)

broken_replies = {
    "": '{"response": {"status": "OK"}}'
}


class HttpClient(object):
    HEADERS = {
        "Content-type": "application/json",
        "User-Agent": "ACOS-Client-AGENT-%s" % acos_client.VERSION,
    }

    def __init__(self, host, port=None, protocol="https", max_retries=3, timeout=5, retry_wait=5, allow_retry=False):
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
        self.retry_wait = retry_wait
        self.allow_retry = allow_retry

    def request(self, method, api_url, params={}, headers=None,
                file_name=None, file_content=None, axapi_args=None, **kwargs):
        LOG.debug("axapi_http: full url = %s", self.url_base + api_url)
        LOG.debug("axapi_http: %s url = %s", method, api_url)
        LOG.debug("axapi_http: params = %s", json.dumps(logutils.clean(params), indent=4))

        valid_http_codes = [200, 204]

        # Update params with axapi_args for currently unsupported configuration of objects
        if axapi_args is not None:
            formatted_axapi_args = dict(
                [(k.replace('_', '-'), v) for k, v in six.iteritems(axapi_args)]
            )
            params = acos_client.v21.axapi_http.merge_dicts(params, formatted_axapi_args)

        # Set data" variable for the request
        if params:
            params_copy = params.copy()
            LOG.debug("axapi_http: params_all = %s", logutils.clean(params_copy))
            payload = json.dumps(params_copy)
        else:
            payload = None

        if (file_name is None and file_content is not None) or \
           (file_name is not None and file_content is None):
            raise ValueError("file_name and file_content must both be populated if one is")

        max_retries = kwargs.get('max_retries', self.max_retries)
        timeout = kwargs.get('timeout', self.timeout)

        # Set "headers" variable for the request
        request_headers = self.HEADERS.copy()
        if headers:
            request_headers.update(headers)
        LOG.debug("axapi_http: headers = %s", json.dumps(logutils.clean(request_headers), indent=4))

        # Process files if passed as a parameter
        if file_name is not None:
            files = {
                'file': (file_name, file_content, "application/octet-stream"),
                'json': ('blob', payload, "application/json")
            }
            request_headers.pop("Content-type", None)
            request_headers.pop("Content-Type", None)

        # Create session to set HTTPAdapter or SSLAdapter and set max_retries
        session = Session()
        session_protocol = "https" if self.port == 443 else "http"
        session = self.requests_retry_session(session, protocol=session_protocol)
        session_request = getattr(session, method.lower())

        # Make actual request and handle any errors
        try:
            if file_name is not None:
                device_response = session_request(
                    self.url_base + api_url, verify=False, files=files, headers=request_headers, timeout=timeout
                )
            else:
                device_response = session_request(
                    self.url_base + api_url, verify=False, data=payload, headers=request_headers, timeout=timeout
                )
        except (Exception) as e:
            LOG.error("acos_client failing with error %s after %s retries", e.__class__.__name__, max_retries)
            raise e
        finally:
            session.close()

        # Validate json response
        try:
            json_response = device_response.json()
            LOG.debug("axapi_http: data = %s", json.dumps(logutils.clean(json_response), indent=4))
        except ValueError as e:
            # The response is not JSON but it still succeeded.
            if device_response.status_code in valid_http_codes:
                return device_response.text
            else:
                raise e

        # Handle "fail" responses returned by AXAPI
        if 'response' in json_response and 'status' in json_response['response']:
            if json_response['response']['status'] == 'fail':
                    acos_responses.raise_axapi_ex(json_response, method, api_url)

        # Handle "authorizationschema" responses returned by AXAPI
        if 'authorizationschema' in json_response:
            acos_responses.raise_axapi_auth_error(json_response, method, api_url, headers)

        return json_response

    def get(self, api_url, params={}, headers=None, **kwargs):
        return self.request("GET", api_url, params, headers, **kwargs)

    def post(self, api_url, params={}, headers=None, **kwargs):
        return self.request("POST", api_url, params, headers, **kwargs)

    def put(self, api_url, params={}, headers=None, **kwargs):
        return self.request("PUT", api_url, params, headers, **kwargs)

    def delete(self, api_url, params={}, headers=None, **kwargs):
        return self.request("DELETE", api_url, params, headers, **kwargs)

    # Shamelessly cribbed from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    def requests_retry_session(self, session=None, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504),
                               protocol="https"):
        session = session or Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist
        )
        adapter = HTTPAdapter(max_retries=retry)
        session_prot = "{0}://".format(protocol)
        session.mount(session_prot, adapter)

        return session
