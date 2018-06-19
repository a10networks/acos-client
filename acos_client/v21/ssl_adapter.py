# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

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

import logging
from requests.adapters import HTTPAdapter
import ssl

FORCED_CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES'
)


class SSLAdapter(HTTPAdapter):
    """A TransportAdapter that re-enables 3DES support in Requests.

    """

    def create_ssl_context(self):
        ctx = ssl.create_default_context()
        # Disable all encryption protcols except TLS1_0
        ctx.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        # Try-Except here because OP_NO_TLSv1_3 not available in Python3 before 3.6
        try:
            ctx.options |= ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_1
        except(AttributeError):
            ctx.options |= ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_1
        ctx.set_ciphers(FORCED_CIPHERS)
        ctx.check_hostname = False
        return ctx

    def init_poolmanager(self, *args, **kwargs):
        logging.debug(' ----------- SSLAdapter.init_poolmanager -------------- ')
        kwargs['ssl_context'] = self.create_ssl_context()
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        logging.debug(' ----------- SSLAdapter.proxy_manager_for -------------- ')
        kwargs['ssl_context'] = self.create_ssl_context()
        return super(SSLAdapter, self).proxy_manager_for(*args, **kwargs)
