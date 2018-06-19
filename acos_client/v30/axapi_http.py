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

    def __init__(self, host, port=None, protocol="https", timeout=None,
                 retry_errno_list=None):
        if port is None:
            if protocol is 'http':
                self.port = 80
            else:
                self.port = 443
        self.url_base = "%s://%s:%s" % (protocol, host, self.port)

    def request(self, method, api_url, params={}, headers=None,
                file_name=None, file_content=None, axapi_args=None, **kwargs):
        LOG.debug("axapi_http: full url = %s", self.url_base + api_url)
        LOG.debug("axapi_http: %s url = %s", method, api_url)
        LOG.debug("axapi_http: params = %s", json.dumps(logutils.clean(params), indent=4))

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
            raise ValueError("file_name and file_content must both be "
                             "populated if one is")

        # Set "headers" variable for the request
        request_headers = self.HEADERS.copy()
        if headers:
            request_headers.update(headers)
        LOG.debug("axapi_http: headers = %s", json.dumps(
            logutils.clean(request_headers), indent=4)
            )

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
        if self.port == 443:
            session.mount('https://', HTTPAdapter(max_retries=60))
        else:
            session.mount('http://', HTTPAdapter(max_retries=60))
        session_request = getattr(session, method.lower())

        # Make actual request and handle any errors
        try:
            if file_name is not None:
                device_response = session_request(
                    self.url_base + api_url, verify=False, files=files, headers=request_headers)
            else:
                device_response = session_request(
                    self.url_base + api_url, verify=False, data=payload, headers=request_headers)
        except (Exception) as e:
            LOG.error("acos_client failing with error %s after 60 retries",
                      e.__class__.__name__)
            raise e

        # Validate json response
        try:
            json_response = device_response.json()
            LOG.debug(
                "axapi_http: data = %s", json.dumps(logutils.clean(json_response), indent=4)
            )
        except ValueError as e:
            # The response is not JSON but it still succeeded.
            if device_response.status_code == 200:
                return {}
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
