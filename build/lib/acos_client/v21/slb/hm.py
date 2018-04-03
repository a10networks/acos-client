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

import acos_client.errors as acos_errors
import acos_client.v21.base as base


class HealthMonitor(base.BaseV21):

    # Valid types
    ICMP = 0
    TCP = 1
    HTTP = 3
    HTTPS = 4

    def get(self, name, **kwargs):
        return self._post("slb.hm.search", {"name": name}, **kwargs)

    def _set(self, action, name, mon_type, interval, timeout, max_retries,
             method=None, url=None, expect_code=None, port=None, **kwargs):
        defs = {
            self.HTTP: {
                'protocol': 'http',
                'port': 80
            },
            self.HTTPS: {
                'protocol': 'https',
                'port': 443
            },
            self.ICMP: {
                'protocol': 'icmp',
            },
            self.TCP: {
                'protocol': 'tcp',
                'port': 80
            }
        }
        params = {
            'retry': max_retries,
            'name': name,
            'consec_pass_reqd': max_retries,
            'interval': interval,
            'timeout': timeout,
            'disable_after_down': 0,
            'type': mon_type,
        }
        if mon_type in defs:
            params[defs[mon_type]['protocol']] = {
                'url': "%s %s" % (method, url),
                'expect_code': expect_code,
            }
            n = port or defs[mon_type].get('port')
            if n:
                params[defs[mon_type]['protocol']]['port'] = n
        try:
            self._post(action, params, **kwargs)
        except acos_errors.HMMissingHttpPassive:
            # Some version of AxAPI 2.1 require this arg
            params[defs[mon_type]['protocol']]['passive'] = 0
            self._post(action, params, **kwargs)

    def create(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None, **kwargs):
        self._set("slb.hm.create", name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port, **kwargs)

    def update(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None, **kwargs):
        self._set("slb.hm.update", name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port, **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.hm.delete", {"name": name}, **kwargs)
