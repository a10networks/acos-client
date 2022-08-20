# Copyright 2014,  Jeff Buttars,  A10 Networks.
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

import ipaddress
import six
import time

from acos_client import errors as ae


class BaseV30(object):

    def __init__(self, client):
        self.client = client
        self.http = client.http
        self.auth_header = {}

    def minimal_dict(self, my_dict, exclude=[]):
        return dict((k, v) for k, v in my_dict.items() if v is not None or k in exclude)

    def url(self, action):
        self.auth_header['Authorization'] = "A10 %s" % self.client.session.id
        return ("/axapi/v3" + action)

    def _request(self, method, action, params, retry_count=0, max_retries=None,
                 timeout=None, axapi_args=None, **kwargs):
        if retry_count > 24:
            raise ae.ACOSUnknownError()

        try:
            return self.client.http.request(method, self.url(action), params, self.auth_header,
                                            max_retries=max_retries, timeout=timeout,
                                            axapi_args=axapi_args, **kwargs)
        except (ae.InvalidSessionID, ae.ConfigManagerNotReady) as e:
            if type(e) == ae.ConfigManagerNotReady:
                retry_limit = 24
                sleep_secs = 5
            else:
                retry_limit = 5
                sleep_secs = 1.0

            if retry_count < retry_limit:
                time.sleep(sleep_secs)
                try:
                    p = self.client.current_partition
                    self.client.session.close()
                    self.client.partition.active(p)
                except Exception:
                    pass
                return self._request(method, action, params, retry_count + 1, max_retries=max_retries,
                                     timeout=timeout, axapi_args=axapi_args, **kwargs)
            raise e

    def _get(self, action, params={}, max_retries=None, timeout=None, axapi_args=None, **kwargs):
        return self._request('GET', action, params, max_retries=max_retries, timeout=timeout,
                             axapi_args=axapi_args, **kwargs)

    def _post(self, action, params={}, max_retries=None, timeout=None, axapi_args=None, **kwargs):
        return self._request('POST', action, params, max_retries=max_retries, timeout=timeout,
                             axapi_args=axapi_args, **kwargs)

    def _put(self, action, params={}, max_retries=None, timeout=None, axapi_args=None, **kwargs):
        return self._request('PUT', action, params, max_retries=max_retries, timeout=timeout,
                             axapi_args=axapi_args, **kwargs)

    def _delete(self, action, params={}, max_retries=None, timeout=None, axapi_args=None, **kwargs):
        return self._request('DELETE', action, params, max_retries=max_retries, timeout=timeout,
                             axapi_args=axapi_args, **kwargs)

    def _is_ipv6(self, ip_address):
        ip_version = ipaddress.ip_address(ip_address).version
        if ip_version == 4:
            return False
        if ip_version == 6:
            return True
