# Copyright (C) 2021, A10 Networks Inc. All rights reserved.

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

from acos_client.v30 import base


class SecretStringUndefinedException(Exception):

    def __init__(self):
        self.message = ("The secret_string argument must "
                        "be defined if password is specified.")
        super(SecretStringUndefinedException, self).__init__(self.message)
        

class ProxyServer(base.BaseV30):
    url_prefix = '/glm/proxy-server'

    def _set(self, host=None, port=None, username=None,
             password=None, secret_string=None):
        params = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'secret_string': secret_string
        }

        if password and not secret_string:
            raise SecretStringUndefinedException()

        return params

    def create(self, host=None, port=None, username=None,
               password=None, secret_string=None, **kwargs):
        params = self._set(host=host, port=port, username=username,
                           password=password, secret_string=secret_string)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def update(self, host=None, port=None, username=None,
               password=None, secret_string=None, **kwargs):
        params = self._set(host=host, port=port, username=username,
                           password=password, secret_string=secret_string)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def put(self, host=None, port=None, username=None,
            password=None, secret_string=None, **kwargs):
        params = self._set(host=host, port=port, username=username,
                           password=password, secret_string=secret_string)
        return self._put(self.url_prefix, params, axapi_args=kwargs)

    def delete(self):
        return self._delete(self.url_prefix)