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

    @property
    def url_separator(self):
        return '/'

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
        validated_ip_address = ipaddress.ip_address(six.text_type(ip_address))
        return isinstance(validated_ip_address, ipaddress.IPv6Address)

    def _add_separator(self, prefix, *, preceding=False, trailing=False):
        if not isinstance(prefix, str):
            return prefix
        if preceding:
            prefix = prefix if prefix.startswith(self.url_separator) else f"{self.url_separator}{prefix}"
        if trailing:
            prefix = prefix if prefix.endswith(self.url_separator) else f"{prefix}{self.url_separator}"
        return prefix

    def _remove_separator(self, endpoint_url, *, preceding=False, trailing=False):
        if not isinstance(endpoint_url, str):
            return endpoint_url
        if preceding:
            endpoint_url = endpoint_url[1:] if endpoint_url.startswith(self.url_separator) else endpoint_url
        if trailing:
            endpoint_url = endpoint_url[:-1] if endpoint_url.endswith(self.url_separator) else endpoint_url
        return endpoint_url

    def _build_url(
        self, *args, prefix=None, middle=None, suffix=None, ends_with_separator=False, starts_with_separator=False,
    ):
        """
        Build url according to given parameters.

        :param args: If given, args is used to build url by separating with `self.url_separator`. If this parameter
            is provided, `middle` and `suffix` parameters are skipped.
        :param middle: If provided it will be the middle part of the url by following url prefix.
        :param suffix: If provided it will be the last part of the url by following url prefix.
        :param ends_with_separator: If provided, add `self.url_separator` to the end of the built url if not exists.
        :param starts_with_separator: If provided, add `self.url_separator` to the beginning of the built url if not exists.
        :param prefix: if provided, used as prefix of the built url, otherwise `self.url_prefix` is used as url prefix.
        :return: built url
        """
        prefix = self.url_prefix if not prefix and hasattr(self, "url_prefix") else prefix
        raw_parts = args if args else [e for e in [middle, suffix]]  # use args else middle and suffix
        url_parts = [self._remove_separator(prefix, trailing=True)]  # remove trailing separator if exists
        url_parts.extend([self._remove_separator(e, trailing=True, preceding=True) for e in raw_parts if e])
        url = self.url_separator.join([str(i) for i in url_parts])  # it can be int type, i.e.: asn number

        return self._add_separator(url, preceding=starts_with_separator, trailing=ends_with_separator)

    @staticmethod
    def convert_to_int(bool_val):
        """
        Converts `bool_val` parameter to int value. If and only if `bool_val` is boolean type and equals to True,
        this method returns 1, otherwise 0.
        :param bool_val: the parameter converted into int value, expected bool type but any type works also.
        :return: 1 only if `bool_val` is True. Otherwise, returns 0.
        """
        return int(bool_val is True)
