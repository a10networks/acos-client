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

import acos_client.v21.base as base


class HealthMonitor(base.BaseV21):

    # Valid types
    ICMP = 0
    TCP = 1
    HTTP = 3
    HTTPS = 4

    def get(self, name):
        return self.http.post(self.url("slb.hm.search"), {"name": name})

    def _set(self, action, mon_type, name, interval, timeout, max_retries,
             method=None, url=None, expect_code=None, port=None):
        defs = {
            self.HTTP: {
                'protocol': 'http',
                'port': 80
            },
            self.HTTPS: {
                'protocol': 'https',
                'port': 443
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
                'port': port or defs[mon_type]['port'],
                'url': "%s %s" % (method, url),
                'expect_code': expect_code,
            }
        self.http.post(self.url(action), params)

    def create(self, *args):
        self._set("slb.hm.create", *args)

    def update(self, *args):
        self._set("slb.hm.update", *args)

    def delete(self, name):
        self.http.post(self.url("slb.hm.delete"), {"name": name})
