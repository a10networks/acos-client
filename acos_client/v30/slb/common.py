# Copyright 2014-2016 A10 Networks.
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


class SLBCommon(base.BaseV30):

    url_prefix = "/slb/common"

    def _underscore_to_dash(self, val):
        rv = val.replace("_", "-")
        return rv

    def create(self, **kwargs):
        params = {"common": {}}
        for k, v in kwargs.items():
            params["common"][self._underscore_to_dash(k)] = v
            del kwargs[k]

        return self._post(self.url_prefix, params, **kwargs)
