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

import json
import acos_client.v30.base as base


class HealthMonitor(base.BaseV30):

    # Valid types
    ICMP = 0
    TCP = 1
    HTTP = 3
    HTTPS = 4
    url_prefix = "/health/monitor/"

    def get(self, name):
        return self.http.get(self.url(self.url_prefix + name))

    def _set(self, action, name, mon_type, interval, timeout, max_retries,
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

        params = {'monitor': {
            'retry': max_retries,
            'name': name,
            'consec_pass_reqd': max_retries,
            'interval': interval,
            'timeout': timeout,
            'disable_after_down': 0,
            'type': mon_type,
        }}
        if mon_type in defs:
            params[defs[mon_type]['protocol']] = {
                'port': port or defs[mon_type]['port'],
                'url': "%s %s" % (method, url),
                'expect_code': expect_code,
            }

        self.http.post(self.url(action), json.dumps(params))

    def create(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None):
        self._set(self.url_prefix, name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port)

    def update(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None):
        self._set(self.url_prefix, name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port)

    def delete(self, name):
        self.http.delete(self.url(self.url_prefix + "name"))
