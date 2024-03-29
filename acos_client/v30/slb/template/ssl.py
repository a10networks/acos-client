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
import acos_client.utils as utils


class BaseSSL(base.BaseV30):

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def exists(self, name):
        try:
            self.get(name)
            return True
        except acos_errors.NotFound:
            return False

    def get_acos_version(self):
        url = "/version/oper"
        return self._get(url)

    def _set(self, name, cert="", key="", passphrase="", update=False,
             cipher_template=None, **kwargs):
        # Unimplemented options:
        # encrypted, session_ticket_enable, version, forward_proxy_enable,
        # close_notify, session_cache_size, session_cache_timeout,
        # server_certificate_error, cipher_without_prio_list,

        version_summary = self.get_acos_version()
        acos_version = version_summary['version']['oper']['sw-version'].split(',')[0]
        params = {}

        if cipher_template:
            params = {
                "cipher": {
                    "name": name,
                    "cipher-cfg": cipher_template
                }
            }

        else:
            if utils.acos_version_cmp(acos_version, "5.2.0") >= 0:
                if not update:
                    obj_params = {
                        "name": name,
                        "certificate-list": [
                            {
                                "cert": cert,
                                "key": key,
                                "passphrase": passphrase
                            }
                        ]
                        # Unimplemented options:
                        # "encrypted": encrypted,
                        # "session-ticket-enable": session_ticket_enable,
                        # "version": version,
                        # "forward-proxy-enable": forward_proxy_enable,
                        # "close-notify": close_notify,
                        # "session-cache-size": session_cache_size,
                        # "session-cache-timeout": session_cache_timeout,
                        # "server-certificate-error": server_certificate_error,
                        # "cipher-without-prio-list": cipher_without_prio_list,
                        # "ca-certs": ca_certs,
                    }
                else:
                    if self.exists(name):
                        existing_template = self.get(name)
                        existing_cert_list = existing_template['client-ssl']['certificate-list'][0]
                        existing_cert = existing_cert_list['cert']
                        existing_key = existing_cert_list['key']
                        if "passphrase" in existing_cert_list:
                            existing_passphrase = existing_cert_list['passphrase']
                        else:
                            existing_passphrase = ""

                    obj_params = {
                        "name": name,
                        "certificate-list": [
                            {
                                "cert": existing_cert,
                                "key": existing_key,
                                "passphrase": existing_passphrase
                            },
                            {
                                "cert": cert,
                                "key": key,
                                "passphrase": passphrase
                            }
                        ]
                        # Unimplemented options:
                        # "encrypted": encrypted,
                        # "session-ticket-enable": session_ticket_enable,
                        # "version": version,
                        # "forward-proxy-enable": forward_proxy_enable,
                        # "close-notify": close_notify,
                        # "session-cache-size": session_cache_size,
                        # "session-cache-timeout": session_cache_timeout,
                        # "server-certificate-error": server_certificate_error,
                        # "cipher-without-prio-list": cipher_without_prio_list,
                        # "ca-certs": ca_certs,
                    }
            else:
                obj_params = {
                    "name": name,
                    "cert": cert,
                    "key": key,
                    self.passphrase: passphrase,
                    # Unimplemented options:
                    # "encrypted": encrypted,
                    # "session-ticket-enable": session_ticket_enable,
                    # "version": version,
                    # "forward-proxy-enable": forward_proxy_enable,
                    # "close-notify": close_notify,
                    # "session-cache-size": session_cache_size,
                    # "session-cache-timeout": session_cache_timeout,
                    # "server-certificate-error": server_certificate_error,
                    # "cipher-without-prio-list": cipher_without_prio_list,
                    # "ca-certs": ca_certs,
                }

            params = {'%s-ssl' % self.prefix: {}}
            for key, val in six.iteritems(obj_params):
                # Filter out invalid, or unset keys
                if val != "":
                    params['%s-ssl' % self.prefix][key] = val

            if not update:
                name = ''

        self._post(self.url_prefix + name, params, **kwargs)

    def create(self, name, cert="", key="", passphrase="", cipher_template=None, **kwargs):
        if self.exists(name):
            raise acos_errors.Exists

        self._set(name, cert, key, passphrase, cipher_template=cipher_template, **kwargs)

    def update(self, name, cert="", key="", passphrase="", **kwargs):
        self._set(name, cert, key, passphrase, update=True, **kwargs)

    def delete(self, name, **kwargs):
        self._delete(self.url_prefix + name, **kwargs)


class ClientSSL(BaseSSL):

    url_prefix = '/slb/template/client-ssl/'
    prefix = 'client'
    passphrase = 'key-passphrase'


class ServerSSL(BaseSSL):

    url_prefix = '/slb/template/server-ssl/'
    prefix = 'server'
    passphrase = 'passphrase'


class SSLCipher(BaseSSL):

    url_prefix = '/slb/template/cipher/'
    passphrase = None
    prefix = None
