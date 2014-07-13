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


class BaseV21(object):

    def __init__(self, client):
        self.client = client
        self.http = client.http

    def minimal_dict(self, my_dict):
        return dict((k, v) for k, v in my_dict.items() if v is not None)

    def url(self, action):
        return ("/services/rest/v2.1/?format=json&method=%s&session_id=%s" %
                (action, self.client.session.id))
