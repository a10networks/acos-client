# Copyright 2016, A10 Networks.
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
import acos_client.v30.base as base


class HttpTemplate(base.BaseV30):

    url_prefix = '/slb/template/http/'
    prefix = 'http'

    def _set(self, name, redirect_rewrite=[], host_switching=[],
             site_switching=[], update=False, *args, **kwargs):
        params = self._build_params(name, redirect_rewrite, host_switching, site_switching,
                                    *args, **kwargs)
        # Don't use url name in URL prefix for creates
        if not update:
            name = ''
        self._post(self.url_prefix + name, params, **kwargs)

    def _build_params(self, name, redirect_rewrite=[], host_switching=[],
                      site_switching=[], *args, **kwargs):
        obj_params = {
            "name": name,
            "redirect-rewrite": site_switching,
            "host-switching": host_switching,
            "site-switching": site_switching,
            # "compression-enable": 0,
            # "compression-keep-accept-encoding": 0,
            # "compression-level": 1,
            # "compression-minimum-content-length": 120,
            # "insert-client-ip": 0,
            # "insert-client-port": 0,
            # "log-retry": 0,
            # "non-http-bypass": 0,
            # "redirect": 0,
            # "redirect-rewrite": {
            #     "match-list": match_list,
            #     "redirect-secure": 0
            # },
            # "retry-on-5xx": 0,
            # "strict-transaction-switch": 0,
            # "term-11client-hdr-conn-close": 0,
            # "url-hash-persist": 0,
            # "req-hdr-wait-time": 0,
            # "request-line-case-insensitive": 0,
            # "keep-client-alive": 0
        }


        params = {self.prefix: {}}
        for key, val in obj_params.iteritems():
            # Filter out invalid, or unset keys
            if val != "":
                params[self.prefix][key] = val
        return params

    def create(self, name, redirect_rewrite=[], host_switching=[],
               site_switching=[], *args, **kwargs):
        if self.exists(name):
            raise acos_errors.Exists

        return self._set(name, redirect_rewrite, host_switching, site_switching, args, kwargs)

    def update(self, name, redirect_rewrite=[], host_switching=[],
               site_switching=[], *args, **kwargs):
        if not self.exists(name):
            raise acos_errors.NotFound

        return self._set(name=name, redirect_rewrite=redirect_rewrite,
                         host_switching=host_switching, site_switching=site_switching, update=True,
                         args=args, kwargs=kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)

    def get(self, name):
        return self._get(self.url_prefix + name)

    def exists(self, name):
        try:
            self.get(name)
            return True
        except acos_errors.NotFound:
            return False
