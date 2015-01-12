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


class BaseV30(object):

    def __init__(self, client):
        self.client = client
        self.http = client.http
        self.auth_header = {}

    def minimal_dict(self, my_dict):
        return dict((k, v) for k, v in my_dict.items() if v is not None)

    def url(self, action):
        self.auth_header['Authorization'] = "A10 %s" % self.client.session.id
        return ("/axapi/v3" + action)

    def _request(self, method, action, params, retry_count=0):
        return self.client.http.request(method, self.url(action), params,
                                        self.auth_header)

    def _get(self, action, params={}):
        return self._request('GET', action, params)

    def _post(self, action, params={}):
        return self._request('POST', action, params)

    def _delete(self, action, params={}):
        return self._request('DELETE', action, params)