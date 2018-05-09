# Copyright 2016,  A10 Networks, All Rights Reserved.
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

from acos_client import errors as acos_errors
from acos_client.v30 import base


class SFlow(base.BaseV30):

    url_prefix = '/sflow/'

    @property
    def collector(self):
        return SFlowCollector(self.client)

    @property
    def setting(self):
        return SFlowSetting(self.client)

    @property
    def polling(self):
        return SFlowPolling(self.client)


class SFlowSetting(base.BaseV30):
    url_prefix = "/sflow/setting"

    def create(self, max_header, source_ip_use_mgmt,
               packet_sampling_rate, counter_polling_interval, **kwargs):
        params = {
            "setting": {
                # "max-header": max_header,
                # "source-ip-use-mgmt": int(source_ip_use_mgmt),
                # "packet-sampling-rate": packet_sampling_rate,
                "counter-polling-interval": counter_polling_interval
            }
        }

        return self._post(self.url_prefix, params, **kwargs)

    def get(self):
        return self._get(self.url_prefix)


class SFlowCollectorIP(base.BaseV30):
    url_prefix = "/sflow/collector/ip"

    def create(self, ip_address, port, **kwargs):
        params = {
            "ip":
                [{
                    "addr": ip_address,
                    "port": int(port)
                }]

        }

        return self._post(self.url_prefix, params, **kwargs)

    def get(self, ip_address, port, **kwargs):
        url = "{0}/{1}+{2}".format(self.url_prefix, ip_address, port)
        return self._get(url, **kwargs)


class SFlowCollector(base.BaseV30):
    @property
    def ip(self):
        return SFlowCollectorIP(self.client)


class SFlowPolling(base.BaseV30):
    url_prefix = "/sflow/polling"

    def create(self, http_counter=False, **kwargs):
        params = {
            "polling": {
                "http-counter": http_counter
            }
        }
        try:
            return self._post(self.url_prefix, params, **kwargs)
        except acos_errors.Exists:
            pass

    def get(self, **kwargs):
        return self._get(self.url_prefix, **kwargs)
