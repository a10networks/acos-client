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
from acos_client.v30.glm import license
from acos_client.v30.glm import proxy


class Flexpool(base.BaseV30):
    url_prefix = '/glm'

    @property
    def proxy_server(self):
        return proxy.ProxyServer(self.client)

    @property
    def create_license_request(self):
        return license.LicenseRequest(self.client)

    @property
    def new_licese(self):
        return license.NewLicense(self.client)

    @property
    def send(self):
        return Send(self.client)

    def _set(self, appliance_name=None, allocate_bandwidth=None, burst=None,
             check_expiration=None, enable_requests=None, enterpise=None,
             enterprise_request_type=None, host=None, interval=None,
             port=None, thunder_capacity_license=None, token=None,
             use_mgmt_port=None):

        params = {
            "glm": self.minimal_dict({
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
                "allocate-bandwidth": allocate_bandwidth,
                "enterprise-request-type": enterprise_request_type,
                "thunder-capacity-license": thunder_capacity_license,
            })
        }
        return params

    def create(self, appliance_name=None, allocate_bandwidth=None, burst=None,
               check_expiration=None, enable_requests=None, enterpise=None,
               enterprise_request_type=None, host=None, interval=None,
               port=None, thunder_capacity_license=None, token=None,
               use_mgmt_port=None, **kwargs):
        params = self._set(appliance_name=appliance_name,
                           allocate_bandwidth=allocate_bandwidth, burst=burst,
                           check_expiration=check_expiration, enable_requests=enable_requests,
                           enterpise=enterpise, enterprise_request_type=enterprise_request_type,
                           thunder_capacity_license=thunder_capacity_license,
                           token=token, use_mgmt_port=use_mgmt_port,
                           host=host, interval=interval, port=port)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def update(self, appliance_name=None, allocate_bandwidth=None, burst=None,
               check_expiration=None, enable_requests=None, enterpise=None,
               enterprise_request_type=None, host=None, interval=None,
               port=None, thunder_capacity_license=None, token=None,
               use_mgmt_port=None, **kwargs):
        params = self._set(appliance_name=appliance_name,
                           allocate_bandwidth=allocate_bandwidth, burst=burst,
                           check_expiration=check_expiration, enable_requests=enable_requests,
                           enterpise=enterpise, enterprise_request_type=enterprise_request_type,
                           thunder_capacity_license=thunder_capacity_license,
                           token=token, use_mgmt_port=use_mgmt_port,
                           host=host, interval=interval, port=port)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def replace(self, appliance_name=None, allocate_bandwidth=None, burst=None,
                check_expiration=None, enable_requests=None, enterpise=None,
                enterprise_request_type=None, host=None, interval=None,
                port=None, thunder_capacity_license=None, token=None,
                use_mgmt_port=None, **kwargs):
        params = self._set(appliance_name=appliance_name,
                           allocate_bandwidth=allocate_bandwidth, burst=burst,
                           check_expiration=check_expiration, enable_requests=enable_requests,
                           enterpise=enterpise,
                           enterprise_request_type=enterprise_request_type,
                           thunder_capacity_license=thunder_capacity_license,
                           token=token, use_mgmt_port=use_mgmt_port,
                           host=host, interval=interval, port=port)
        return self._put(self.url_prefix, params, axapi_args=kwargs)

    def delete(self):
        return self._delete(self.url_prefix)


class Send(base.BaseV30):
    url_prefix = '/glm/send'

    def create(self, license_request):
        params = {
            "send": self.minimal_dict({
                "license-request": license_request
            })
        }

        self._post(self.url_prefix, params)
