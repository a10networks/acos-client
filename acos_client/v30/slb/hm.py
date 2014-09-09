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

import acos_client.v30.base as base


class HealthMonitor(base.BaseV30):

    # Valid method objects
    ICMP = 'icmp'
    TCP = 'tcp'
    HTTP = 'http'
    HTTPS = 'https'
    url_prefix = "/health/monitor/"

    _method_objects = {
        ICMP: {
            'method-icmp': 1,
            'a10-url': '',
        },
        TCP: {
            'method-tcp': 1,
            'a10-url': '',
        },
        HTTP: {
            'method-http': 1,
            'a10-url': '',
            'http-port': 80,
        },
        HTTPS: {
            'method-https': 1,
            'a10-url': '',
            'https-port': 443,
        },
    }

    def get(self, name):
        return self._get(self.url_prefix + name)

    def _set(self, action, name, mon_method, interval, timeout, max_retries,
             method=None, url=None, expect_code=None, port=None):

        params = {
            'name': name,
            'retry': int(max_retries),
            'interval': int(interval),
            'timeout': int(timeout),
            # 'disable-after-down': 0,
            # 'passive': 0,
            # 'strict-retry-on-server-err-resp': 0
        }

        mon_obj = {
            mon_method: {
                mon_method: 1,
                'http-port': int(port),
                'http-expect': 1,
                'http-response-code': str(expect_code),
                'http-url': 1,
                'url-type': method,
                'url-path': url,
                #'http-kerberos-auth': 0
            }
        }

  #   {
  #     "name":"hm-http-1",
  #     "retry":5,
  #     "passive":0,
  #     "strict-retry-on-server-err-resp":0,
  #     "disable-after-down":0,
  #     "interval":5,
  #     "timeout":5,
  #     "method": {
  #       "http": {
  #         "http":1,
  #         "http-port":80,
  #         "http-expect":1,
  #         "http-response-code":"200",
  #         "http-url":1,
  #         "url-type":"GET",
  #         "url-path":"/",
  #         "http-kerberos-auth":0,
  #         "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1/method/http"
  #       },
  #       "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1/method"
  #     },
  #     "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1"
  #   }

        params = {
          "name": name,
          "retry":5,
          "passive":0,
          "strict-retry-on-server-err-resp":0,
          "disable-after-down":0,
          "interval":5,
          "timeout":5,
          "method": {
            "http": {
              "http":1,
              "http-port":80,
              "http-expect":1,
              "http-response-code":"200",
              "http-url":1,
              "url-type":"GET",
              "url-path":"/",
              "http-kerberos-auth":0,
              # "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1/method/http"
            },
            # "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1/method"
          },
          # "a10-url":"https://172.18.61.29/axapi/v3/health/monitor/hm-http-1"
        }

        params['method'] = mon_obj

        import json
        print "JSON args = \n%s", json.dumps(params, indent=4)

        self._post(action, params)

    def create(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None):
        self._set(self.url_prefix, name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port)

    def update(self, name, mon_type, interval, timeout, max_retries,
               method=None, url=None, expect_code=None, port=None):
        self._set(self.url_prefix, name, mon_type, interval, timeout,
                  max_retries, method, url, expect_code, port)

    def delete(self, name):
        self._delete(self.url_prefix + name)
