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
from acos_client.v30.glm.proxy import ProxyServer
from acos_client.v30.glm.license import LicenseRequest


class Flexpool(base.BaseV30):
    url_prefix = '/glm'

    @property
    def proxy_server(self):
        return ProxyServer(self.client)

    @property
    def create_license_request(self):
        return LicenseRequest(self.client)

    @property
    def new_licese(self):
        return NewLicense(self.client)

    @property
    def send(self):
        return Send(self.client)

    def _set(self, appliance_name=None, allocate_bandwith=None, burst=None,
             check_expiration=None, enable_requests=None, enterpise=None,
             enterprise_request_type=None, host=None, interval=None,
             port=None, thunder_capacity_license=None, token=None,
             use_mgmt_port=None, uuid=None, **kwargs):
        
        params = {
            "glm": self.minimal_dict({
                "uuid": uuid,
                "host": host,
                "port": port,
                "burst": burst,
                "token": token,
                "interval": interval,
                "enterpise": enterpise,
                "use-mgmt-port": use_mgmt_port,
                "appliance-name": appliance_name,
                "enable-requests": enable_requests,
                "check-expiration": check_expiration,
                "allocate-bandwidth": allocate_bandwith,
                "enterprise-request-type": enterprise_request_type,
                "thunder-capacity-license": thunder_capacity_license,
            })
        }

        return params, kwargs

    def create(self, *args, **kwargs):
        params, kwargs = self._set(*args, **kwargs)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def update(self, *args, **kwargs):
        params, kwargs = self._set(*args, **kwargs)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def replace(self, *args, **kwargs):
        params, kwargs = self._set(*args, **kwargs)
        return self._put(self.url_prefix, params, axapi_args=kwargs)

    def delete(self):
        return self._delete(self.url_prefix)


class Send(base.BaseV30):
    url_prefix = '/glm/send'

    def create(self, license_request=None):
        params = {
            "send": self.minimal_dict({
                "license-request": license_request
            })
        }

        self._post(self.url_prefix, params)


class NewLicense(base.BaseV30):
    url_prefix = '/glm/send'

    def create(self, license_request=None):
        params = {
            "send": self.minimal_dict({
                "license-request": license_request
            })
        }

        self._post(self.url_prefix, params)