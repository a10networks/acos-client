# Copyright 2015,  Tobit Raff,  A10 Networks.
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
import six


from acos_client import errors as acos_errors
from acos_client.v30 import base


class BaseL7(base.BaseV30):

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def exists(self, name):
        try:
            self.get(name)
            return True
        except acos_errors.NotFound:
            return False

    def _set(self, name, insert_client_ip=0, insert_client_ip_header_name="", client_ip_hdr_replace=0,
             request_header_insert_list=[], response_header_insert_list=[], update=False,
             **kwargs):
        # Unimplemented options:
        # Everything except for insert_client_ip and request header insert.

        obj_params = {
            "name": name,
            "insert-client-ip": insert_client_ip,
            "insert-client-ip-header-name": insert_client_ip_header_name,
            "client-ip-hdr-replace": client_ip_hdr_replace,
            "request-header-insert-list": request_header_insert_list,
            "response-header-insert-list": response_header_insert_list
        }

        params = {'%s' % self.prefix: {}}
        for key, val in six.iteritems(obj_params):
            # Filter out invalid, or unset keys
            if val != "":
                params['%s' % self.prefix][key] = val
        if not update:
            name = ''
        self._post(self.url_prefix + name, params, **kwargs)

    def create(self, name, insert_client_ip=False, insert_client_ip_header_name="",
               client_ip_hdr_replace=0, request_header_insert_list=[], response_header_insert_list=[],
               **kwargs):
        if self.exists(name):
            raise acos_errors.Exists

        self._set(name, insert_client_ip, insert_client_ip_header_name, client_ip_hdr_replace,
                  request_header_insert_list, response_header_insert_list, **kwargs)

    def update(self, name, insert_client_ip=False, insert_client_ip_header_name="",
               client_ip_hdr_replace=0, request_header_insert_list=[], response_header_insert_list=[],
               **kwargs):
        self._set(name, insert_client_ip, insert_client_ip_header_name, client_ip_hdr_replace,
                  request_header_insert_list, response_header_insert_list, update=True, **kwargs)

    def delete(self, name, **kwargs):
        self._delete(self.url_prefix + name, **kwargs)


class HTTPTemplate(BaseL7):

    url_prefix = '/slb/template/http/'
    prefix = 'http'
