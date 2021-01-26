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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as acos_errors
from acos_client.v30 import base


class HealthMonitor(base.BaseV30):

    # Valid method objects
    UDP = 'udp'
    ICMP = 'icmp'
    TCP = 'tcp'
    HTTP = 'http'
    HTTPS = 'https'
    url_prefix = "/health/monitor/"

    _method_objects = {
        ICMP: {
            "icmp": 1
        },
        UDP: {
            "udp": 1,
            "udp-port": 5550,
            "force-up-with-single-healthcheck": 0
        },
        HTTP: {
            "http": 1,
            "http-port": 80,
            "http-expect": 1,
            "http-response-code": "200",
            "http-url": 1,
            "url-type": "GET",
            "url-path": "/",
        },
        HTTPS: {
            "https": 1,
            "web-port": 443,
            "https-expect": 1,
            "https-response-code": "200",
            "https-url": 1,
            "url-type": "GET",
            "url-path": "/",
            "disable-sslv2hello": 0
        },
        TCP: {
            "method-tcp": 1,
            "tcp-port": 80
        },
    }

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def _set(self, name, mon_method, hm_interval, hm_timeout, hm_max_retries,
             method=None, url=None, expect_code=None, port=None, ipv4=None, post_data=None,
             **kwargs):
        params = {
            "monitor": {
                "name": name,
                "retry": int(hm_max_retries),
                "interval": int(hm_interval),
                "timeout": int(hm_timeout),
                "method": {
                    mon_method: self._method_objects[mon_method]
                },
                "override-ipv4": ipv4
            }
        }
        if method:
            params['monitor']['method'][mon_method]['url-type'] = method
        if url:
            params['monitor']['method'][mon_method]['url-path'] = url
        if expect_code:
            k = "%s-response-code" % mon_method
            params['monitor']['method'][mon_method][k] = str(expect_code)
        if port:
            if mon_method == self.HTTPS:
                k = 'web-port'
            else:
                k = '%s-port' % mon_method
            params['monitor']['method'][mon_method][k] = int(port)
            params['monitor']['override-port'] = int(port)
        # handle POST case for HTTP/HTTPS hm
        if ('url-type' in params['monitor']['method'][mon_method] and
                'url-path' in params['monitor']['method'][mon_method] and
                params['monitor']['method'][mon_method]['url-type'] == "POST"):
            if post_data:
                params['monitor']['method'][mon_method]['post-type'] = "postdata"
                if mon_method == self.HTTPS:
                    params['monitor']['method'][mon_method]['https-postdata'] = str(post_data)
                else:
                    params['monitor']['method'][mon_method]['http-postdata'] = str(post_data)
                postpath = params['monitor']['method'][mon_method]['url-path']
                params['monitor']['method'][mon_method]['post-path'] = postpath
                params['monitor']['method'][mon_method].pop('url-path', None)
        else:
            params['monitor']['method'][mon_method].pop('post-type', None)
            params['monitor']['method'][mon_method].pop('http-postdata', None)
            params['monitor']['method'][mon_method].pop('post-path', None)

        return params

    def create(self, name, mon_type, hm_interval, hm_timeout, hm_max_retries,
               method=None, url=None, expect_code=None, port=None, ipv4=None, post_data=None,
               max_retries=None, timeout=None, **kwargs):
        try:
            self.get(name)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists()

        params = self._set(name, mon_type, hm_interval, hm_timeout,
                           hm_max_retries, method, url, expect_code, port, ipv4,
                           post_data=post_data, **kwargs)
        return self._post(self.url_prefix, params, max_retries=max_retries, timeout=timeout,
                          axapi_args=kwargs)

    def update(self, name, mon_type, hm_interval, hm_timeout, hm_max_retries,
               method=None, url=None, expect_code=None, port=None, ipv4=None, post_data=None,
               max_retries=None, timeout=None, **kwargs):
        self.get(name)  # We want a NotFound if it does not exist
        params = self._set(name, mon_type, hm_interval, hm_timeout,
                           hm_max_retries, method, url, expect_code, port, ipv4,
                           post_data=post_data, **kwargs)
        return self._post(self.url_prefix + name, params, max_retries=max_retries, timeout=timeout,
                          axapi_args=kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)
